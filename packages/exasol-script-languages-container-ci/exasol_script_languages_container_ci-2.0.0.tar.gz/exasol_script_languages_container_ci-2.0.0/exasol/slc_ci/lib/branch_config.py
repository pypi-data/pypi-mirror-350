import re
from dataclasses import dataclass


@dataclass(frozen=True)
class BuildActions:
    build_always: bool
    rebuild: bool
    push_to_docker_release_repo: bool


@dataclass(frozen=True)
class BranchConfig:
    develop = BuildActions(
        build_always=True, rebuild=True, push_to_docker_release_repo=False
    )
    main = BuildActions(
        build_always=True, rebuild=True, push_to_docker_release_repo=True
    )
    rebuild = BuildActions(
        build_always=True, rebuild=True, push_to_docker_release_repo=False
    )
    other = BuildActions(
        build_always=False, rebuild=False, push_to_docker_release_repo=False
    )


def _get_branch_config(branch_name: str) -> BuildActions:
    matches = (
        (re.compile(r"refs/heads/(master|main)"), BranchConfig.main),
        (re.compile(r"refs/heads/develop"), BranchConfig.develop),
        (re.compile(r"refs/heads/rebuild/.*"), BranchConfig.rebuild),
    )

    branch_cfg = BranchConfig.other
    for branch_regex, branch_config in matches:
        if branch_regex.match(branch_name):
            branch_cfg = branch_config
            break
    return branch_cfg


def build_always(branch_name: str) -> bool:
    return _get_branch_config(branch_name).build_always


def rebuild(branch_name) -> bool:
    return _get_branch_config(branch_name).rebuild


def push_to_docker_release_repo(branch_name: str) -> bool:
    return _get_branch_config(branch_name).push_to_docker_release_repo
