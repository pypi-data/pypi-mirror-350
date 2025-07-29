import logging
from typing import Callable, Set

from exasol_script_languages_container_ci.lib.branch_config import BranchConfig
from exasol_script_languages_container_ci.lib.ci_build import CIBuild
from exasol_script_languages_container_ci.lib.ci_prepare import CIPrepare
from exasol_script_languages_container_ci.lib.ci_push import CIPush
from exasol_script_languages_container_ci.lib.ci_security_scan import CISecurityScan
from exasol_script_languages_container_ci.lib.ci_test import CIExecuteTest
from exasol_script_languages_container_ci.lib.config.config_data_model import Config
from exasol_script_languages_container_ci.lib.git_access import GitAccess


def get_all_affected_files(git_access: GitAccess, base_branch: str) -> Set[str]:
    base_last_commit_sha = git_access.get_head_commit_sha_of_branch(base_branch)
    changed_files = set()  # type: ignore
    for commit in git_access.get_last_commits():
        if commit == base_last_commit_sha:
            break
        changed_files.update(git_access.get_files_of_commit(commit))
    return changed_files


def check_if_need_to_build(
    branch_name: str, config: Config, flavor: str, git_access: GitAccess
):
    if BranchConfig.build_always(branch_name):
        return True
    if "[rebuild]" in git_access.get_last_commit_message():
        return True
    affected_files = list(get_all_affected_files(git_access, config.build.base_branch))
    logging.debug(
        f"check_if_need_to_build: Found files of last commits: {affected_files}"
    )
    for ignore_path in config.build.ignore.paths:
        affected_files = list(
            filter(lambda file: not file.startswith(ignore_path), affected_files)
        )

    if len(affected_files) > 0:
        # Now filter out also other flavor folders
        this_flavor_path = f"flavors/{flavor}"
        affected_files = list(
            filter(
                lambda file: not file.startswith("flavors")
                or file.startswith(this_flavor_path),
                affected_files,
            )
        )
    logging.debug(f"check_if_need_to_build: filtered files: {affected_files}")
    return len(affected_files) > 0


def ci(
    flavor: str,
    branch_name: str,
    docker_user: str,
    docker_password: str,
    docker_build_repository: str,
    docker_release_repository: str,
    commit_sha: str,
    build_config: Config,
    git_access: GitAccess,
    ci_build: CIBuild = CIBuild(),
    ci_execute_tests: CIExecuteTest = CIExecuteTest(),
    ci_push: CIPush = CIPush(),
    ci_security_scan: CISecurityScan = CISecurityScan(),
    ci_prepare: CIPrepare = CIPrepare(),
):
    """
    Run CI build:
    1. Build image
    2. Run db tests
    3. Run security scan
    4. Push to docker repositories
    """
    logging.info(f"Running CI build for parameters: {locals()}")

    flavor_path = (f"flavors/{flavor}",)
    test_container_folder = "test_container"
    rebuild = BranchConfig.rebuild(branch_name)
    needs_to_build = check_if_need_to_build(
        branch_name, build_config, flavor, git_access
    )
    if needs_to_build:
        ci_prepare.prepare()
        ci_build.build(
            flavor_path=flavor_path,
            rebuild=rebuild,
            build_docker_repository=docker_build_repository,
            commit_sha=commit_sha,
            docker_user=docker_user,
            docker_password=docker_password,
            test_container_folder=test_container_folder,
        )
        ci_execute_tests.execute_tests(
            flavor_path=flavor_path,
            docker_user=docker_user,
            docker_password=docker_password,
            test_container_folder=test_container_folder,
        )
        ci_security_scan.run_security_scan(flavor_path=flavor_path)
        ci_push.push(
            flavor_path=flavor_path,
            target_docker_repository=docker_build_repository,
            target_docker_tag_prefix=commit_sha,
            docker_user=docker_user,
            docker_password=docker_password,
        )
        ci_push.push(
            flavor_path=flavor_path,
            target_docker_repository=docker_build_repository,
            target_docker_tag_prefix="",
            docker_user=docker_user,
            docker_password=docker_password,
        )
        if BranchConfig.push_to_docker_release_repo(branch_name):
            ci_push.push(
                flavor_path=flavor_path,
                target_docker_repository=docker_release_repository,
                target_docker_tag_prefix="",
                docker_user=docker_user,
                docker_password=docker_password,
            )
    else:
        logging.warning(f"Skipping build...")
