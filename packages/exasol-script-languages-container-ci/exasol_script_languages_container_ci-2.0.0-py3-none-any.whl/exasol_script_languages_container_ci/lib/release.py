import logging

from exasol_script_languages_container_ci.lib.ci_build import CIBuild
from exasol_script_languages_container_ci.lib.ci_prepare import CIPrepare
from exasol_script_languages_container_ci.lib.ci_push import CIPush
from exasol_script_languages_container_ci.lib.ci_security_scan import CISecurityScan
from exasol_script_languages_container_ci.lib.ci_test import CIExecuteTest
from exasol_script_languages_container_ci.lib.config.config_data_model import Config
from exasol_script_languages_container_ci.lib.release_uploader import ReleaseUploader


def release(
    flavor: str,
    docker_user: str,
    docker_password: str,
    docker_release_repository: str,
    build_config: Config,
    source_repo_url: str,
    release_id: int,
    is_dry_run: bool,
    release_uploader: ReleaseUploader,
    ci_build: CIBuild = CIBuild(),
    ci_execute_tests: CIExecuteTest = CIExecuteTest(),
    ci_push: CIPush = CIPush(),
    ci_security_scan: CISecurityScan = CISecurityScan(),
    ci_prepare: CIPrepare = CIPrepare(),
):
    """
    Run Release build:
    1. Build image
    2. Run basic tests
    3. Push to docker release repository
    4. Upload to GH release url
    """
    logging.info(f"Running Release build for parameters: {locals()}")

    flavor_path = (f"flavors/{flavor}",)
    test_container_folder = "test_container"
    ci_prepare.prepare()
    ci_build.build(
        flavor_path=flavor_path,
        rebuild=True,
        build_docker_repository=None,
        commit_sha="",
        docker_user=None,  # type: ignore
        docker_password=None,  # type: ignore
        test_container_folder=test_container_folder,
    )
    ci_execute_tests.execute_tests(
        flavor_path=flavor_path,
        docker_user=docker_user,
        docker_password=docker_password,
        test_container_folder=test_container_folder,
    )
    ci_security_scan.run_security_scan(flavor_path=flavor_path)
    if not is_dry_run:
        ci_push.push(
            flavor_path=flavor_path,
            target_docker_repository=docker_release_repository,
            target_docker_tag_prefix="",
            docker_user=docker_user,
            docker_password=docker_password,
        )
    else:
        logging.info("Skipping push to docker release repository due to dry-run.")
    release_uploader.release_upload(
        flavor_path=flavor_path, source_repo_url=source_repo_url, release_id=release_id
    )
