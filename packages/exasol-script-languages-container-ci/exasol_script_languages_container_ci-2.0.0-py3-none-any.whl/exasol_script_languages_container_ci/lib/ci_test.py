import logging
from typing import Protocol, Tuple

from exasol.slc.api.run_db_tests import run_db_test
from exasol.slc.models.test_result import AllTestsResult

from exasol_script_languages_container_ci.lib.ci_step_output_printer import (
    CIStepOutputPrinter,
    CIStepOutputPrinterProtocol,
)


class DBTestRunnerProtocol(Protocol):
    def run(
        self,
        flavor_path: Tuple[str, ...],
        release_goal: Tuple[str, ...],
        test_folder: Tuple[str, ...],
        test_container_folder: str,
        workers: int,
        docker_username: str,
        docker_password: str,
    ) -> AllTestsResult:
        raise NotImplementedError()


class DBTestRunner(DBTestRunnerProtocol):
    def run(
        self,
        flavor_path: Tuple[str, ...],
        release_goal: Tuple[str, ...],
        test_folder: Tuple[str, ...],
        test_container_folder: str,
        workers: int,
        docker_username: str,
        docker_password: str,
    ) -> AllTestsResult:
        return run_db_test(
            flavor_path=flavor_path,
            release_goal=release_goal,
            test_folder=test_folder,
            test_container_folder=test_container_folder,
            workers=workers,
            source_docker_username=docker_username,
            source_docker_password=docker_password,
            log_level="WARNING",
            use_job_specific_log_file=True,
        )


class CIExecuteTest:

    def __init__(
        self,
        db_test_runner: DBTestRunnerProtocol = DBTestRunner(),
        printer: CIStepOutputPrinterProtocol = CIStepOutputPrinter(logging.info),
    ):
        self._db_test_runner = db_test_runner
        self._printer = printer

    def execute_tests(
        self,
        flavor_path: Tuple[str, ...],
        docker_user: str,
        docker_password: str,
        test_container_folder: str,
    ):
        """
        Run db tests
        """
        db_tests_are_ok = self.run_db_tests(
            flavor_path=flavor_path,
            docker_user=docker_user,
            docker_password=docker_password,
            test_container_folder=test_container_folder,
        )
        linker_namespace_tests_are_ok = self.run_linker_namespace_tests(
            flavor_path=flavor_path,
            docker_user=docker_user,
            docker_password=docker_password,
            test_container_folder=test_container_folder,
        )
        self._printer.print_exasol_docker_images()
        tests_are_ok = db_tests_are_ok and linker_namespace_tests_are_ok
        if not tests_are_ok:
            raise AssertionError("Not all tests are ok!")

    def run_db_tests(
        self,
        flavor_path: Tuple[str, ...],
        docker_user: str,
        docker_password: str,
        test_container_folder: str,
    ) -> bool:
        logging.info(f"Running command 'run_db_test' for flavor-path {flavor_path}")
        db_test_result = self._db_test_runner.run(
            flavor_path=flavor_path,
            test_folder=tuple(),
            release_goal=("release",),
            workers=7,
            docker_username=docker_user,
            docker_password=docker_password,
            test_container_folder=test_container_folder,
        )
        self._printer.print_file(db_test_result.command_line_output_path)
        return db_test_result.tests_are_ok

    def run_linker_namespace_tests(
        self,
        flavor_path: Tuple[str, ...],
        docker_user: str,
        docker_password: str,
        test_container_folder: str,
    ) -> bool:
        logging.info(
            f"Running command 'run_db_test' for linker_namespace_sanity for flavor-path {flavor_path}"
        )
        linker_namespace_test_result = self._db_test_runner.run(
            flavor_path=flavor_path,
            workers=7,
            test_folder=("test/linker_namespace_sanity",),
            release_goal=("base_test_build_run",),
            docker_username=docker_user,
            docker_password=docker_password,
            test_container_folder=test_container_folder,
        )
        self._printer.print_file(linker_namespace_test_result.command_line_output_path)
        return linker_namespace_test_result.tests_are_ok
