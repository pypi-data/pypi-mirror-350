import logging

import click

from exasol_script_languages_container_ci.cli.cli import cli
from exasol_script_languages_container_ci.lib.ci import ci
from exasol_script_languages_container_ci.lib.config.config_data_model import Config
from exasol_script_languages_container_ci.lib.git_access import GitAccess


@cli.command()
@click.option("--flavor", required=True, type=str, help="Flavor name.")
@click.option("--branch-name", required=True, type=str, help="Branch name.")
@click.option("--docker-user", required=True, type=str, help="Docker user name")
@click.option("--docker-password", required=True, type=str, help="Docker password")
@click.option(
    "--docker-build-repository", required=True, type=str, help="Docker build repository"
)
@click.option(
    "--docker-release-repository",
    required=True,
    type=str,
    help="Docker release repository",
)
@click.option("--commit-sha", required=True, type=str, help="Commit SHA")
@click.option(
    "--config-file",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="The build config file (project specific)",
)
@click.pass_context
def run_ci(
    ctx: click.Context,
    flavor: str,
    branch_name: str,
    docker_user: str,
    docker_password: str,
    docker_build_repository: str,
    docker_release_repository: str,
    commit_sha: str,
    config_file: str,
):
    logging.basicConfig(level=logging.INFO)
    build_config = Config.parse_file(config_file)
    ci(
        flavor=flavor,
        branch_name=branch_name,
        docker_user=docker_user,
        docker_password=docker_password,
        docker_build_repository=docker_build_repository,
        docker_release_repository=docker_release_repository,
        commit_sha=commit_sha,
        build_config=build_config,
        git_access=GitAccess(),
    )
