import logging
from pathlib import Path
from typing import List

from exasol.slc_ci.lib.branch_config import build_always
from exasol.slc_ci.lib.get_build_config_model import get_build_config_model
from exasol.slc_ci.lib.git_access import GitAccess
from exasol.slc_ci.lib.github_access import GithubAccess


def get_all_affected_files(
    git_access: GitAccess, base_ref: str, remote: str
) -> List[Path]:
    complete_base_ref = f"{remote}/{base_ref}" if remote else base_ref
    base_last_commit_sha = git_access.get_head_commit_sha_of_branch(complete_base_ref)
    changed_files = set()  # type: ignore
    for commit in git_access.get_last_commits():
        if commit == base_last_commit_sha:
            break
        changed_files.update(git_access.get_files_of_commit(commit))
    return [Path(changed_file) for changed_file in changed_files]


def _run_check_if_need_to_build(
    branch_name: str, base_ref: str, remote: str, flavor: str, git_access: GitAccess
) -> bool:
    build_config = get_build_config_model()
    if build_always(branch_name):
        return True
    if "[rebuild]" in git_access.get_last_commit_message():
        return True
    affected_files = list(get_all_affected_files(git_access, base_ref, remote))
    logging.debug(
        f"check_if_need_to_build: Found files of last commits: {affected_files}"
    )
    affected_files = [
        file
        for file in affected_files
        if not any(
            [
                file.is_relative_to(ignore_path)
                for ignore_path in build_config.ignore_paths
            ]
        )
    ]

    if len(affected_files) > 0:
        # Now filter out also other flavor folders
        this_flavor_path = build_config.flavors_path / flavor
        affected_files = [
            file
            for file in affected_files
            if (
                file.is_relative_to(this_flavor_path)
                or not file.is_relative_to(build_config.flavors_path)
            )
        ]
    logging.debug(f"check_if_need_to_build: filtered files: {affected_files}")
    return len(affected_files) > 0


def check_if_need_to_build(
    branch_name: str,
    base_ref: str,
    remote: str,
    flavor: str,
    github_access: GithubAccess,
    git_access: GitAccess,
) -> None:
    res = _run_check_if_need_to_build(branch_name, base_ref, remote, flavor, git_access)
    github_access.write_result("True" if res else "False")
