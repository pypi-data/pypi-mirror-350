import os
from pathlib import Path

from exasol_integration_test_docker_environment.cli.options.system_options import (
    DEFAULT_OUTPUT_DIRECTORY,
)
from exasol_integration_test_docker_environment.lib.logging import luigi_log_config


class CIPrepare:

    def prepare(self):
        log_path = Path(DEFAULT_OUTPUT_DIRECTORY) / "jobs" / "logs" / "main.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME] = f"{log_path.absolute()}"
