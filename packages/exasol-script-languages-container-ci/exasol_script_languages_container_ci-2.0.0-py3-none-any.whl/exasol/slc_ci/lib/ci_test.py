import logging
from pathlib import Path
from typing import Optional, Protocol, Tuple

from exasol.slc.api.run_db_tests import run_db_test
from exasol.slc.models.accelerator import Accelerator
from exasol.slc.models.test_result import AllTestsResult

from exasol.slc_ci.lib.ci_step_output_printer import (
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
        generic_language_tests: Tuple[str, ...],
        accelerator: Accelerator,
        workers: int,
        docker_username: Optional[str],
        docker_password: Optional[str],
        use_existing_container: Optional[str],
    ) -> AllTestsResult:
        raise NotImplementedError()


class DBTestRunner(DBTestRunnerProtocol):
    def run(
        self,
        flavor_path: Tuple[str, ...],
        release_goal: Tuple[str, ...],
        test_folder: Tuple[str, ...],
        test_container_folder: str,
        generic_language_tests: Tuple[str, ...],
        accelerator: Accelerator,
        workers: int,
        docker_username: Optional[str],
        docker_password: Optional[str],
        use_existing_container: Optional[str],
    ) -> AllTestsResult:
        return run_db_test(
            flavor_path=flavor_path,
            release_goal=release_goal,
            test_folder=test_folder,
            test_container_folder=test_container_folder,
            generic_language_test=generic_language_tests,
            accelerator=accelerator,
            workers=workers,
            source_docker_username=docker_username,
            source_docker_password=docker_password,
            log_level="WARNING",
            use_job_specific_log_file=True,
            use_existing_container=use_existing_container,
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
        slc_path: Path,
        goal: str,
        test_folder: str,
        generic_language_tests: Tuple[str, ...],
        accelerator: Accelerator,
        docker_user: str,
        docker_password: str,
        test_container_folder: str,
    ):
        """
        Run db tests
        """
        db_tests_are_ok = self._run_db_tests(
            flavor_path=flavor_path,
            goal=goal,
            slc_path=slc_path,
            test_folder=test_folder,
            generic_language_tests=generic_language_tests,
            accelerator=accelerator,
            docker_user=docker_user,
            docker_password=docker_password,
            test_container_folder=test_container_folder,
        )
        self._printer.print_exasol_docker_images()
        if not db_tests_are_ok:
            raise AssertionError("Not all tests are ok!")

    def _run_db_tests(
        self,
        flavor_path: Tuple[str, ...],
        slc_path: Path,
        goal: str,
        test_folder: str,
        generic_language_tests: Tuple[str, ...],
        accelerator: Accelerator,
        docker_user: str,
        docker_password: str,
        test_container_folder: str,
    ) -> bool:
        logging.info(f"Running command 'run_db_test' for flavor-path {flavor_path}")
        db_test_result = self._db_test_runner.run(
            flavor_path=flavor_path,
            test_folder=(test_folder,),
            release_goal=(goal,),
            generic_language_tests=generic_language_tests,
            accelerator=accelerator,
            workers=7,
            docker_username=docker_user,
            docker_password=docker_password,
            test_container_folder=test_container_folder,
            use_existing_container=str(slc_path),
        )
        self._printer.print_file(db_test_result.command_line_output_path)
        return db_test_result.tests_are_ok
