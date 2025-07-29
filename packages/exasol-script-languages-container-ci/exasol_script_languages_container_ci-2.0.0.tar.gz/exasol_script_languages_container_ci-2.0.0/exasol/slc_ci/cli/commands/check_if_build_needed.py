import click
from exasol_integration_test_docker_environment.lib.utils.cli_function_decorators import (
    add_options,
)

import exasol.slc_ci.lib.check_if_build_needed as lib_check_if_build_needed
from exasol.slc_ci.cli.cli import cli
from exasol.slc_ci.cli.options.branch_options import (
    base_branch_option,
    branch_option,
    remote_option,
)
from exasol.slc_ci.cli.options.flavor_options import flavor_options
from exasol.slc_ci.cli.options.github_options import github_options
from exasol.slc_ci.lib.git_access import GitAccess
from exasol.slc_ci.lib.github_access import GithubAccess


@cli.command()
@add_options(flavor_options)
@add_options([branch_option, base_branch_option, remote_option])
@add_options(github_options)
def check_if_build_needed(
    flavor: str, branch_name: str, base_ref: str, remote: str, github_output_var: str
) -> None:
    git_access: GitAccess = GitAccess()
    github_access: GithubAccess = GithubAccess(github_output_var)
    lib_check_if_build_needed.check_if_need_to_build(
        branch_name=branch_name,
        base_ref=base_ref,
        remote=remote,
        flavor=flavor,
        github_access=github_access,
        git_access=git_access,
    )
