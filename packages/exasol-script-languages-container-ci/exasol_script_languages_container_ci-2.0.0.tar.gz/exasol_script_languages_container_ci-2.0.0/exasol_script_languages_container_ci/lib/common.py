import json
from contextlib import contextmanager
from inspect import cleandoc
from pathlib import Path
from typing import Callable

import docker


@contextmanager
def get_config(config_file: str):
    """
    Opens config file and returns parsed JSON object.
    """
    with open(config_file) as f:
        yield json.load(f)
