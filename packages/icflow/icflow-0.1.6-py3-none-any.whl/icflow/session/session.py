"""
This module is for workflow sessions
"""

import os
from pathlib import Path
import logging

from iccore import time_utils

from icflow.environment import Environment

logger = logging.getLogger(__name__)


def _setup_result_dir(result_dir: Path):
    """
    Utility to create a result directory with a timestamp
    -based name.
    """
    current_time = time_utils.get_timestamp_for_paths()
    result_dir = result_dir / Path(current_time)
    os.makedirs(result_dir, exist_ok=True)
    return result_dir


class Session:
    """
    A workflow session is an instance of a workflow being
    executed, possibly in parallel over multiple workers.
    """

    def __init__(
        self,
        env: Environment,
        result_dir: Path = Path(),
    ) -> None:

        self.env = env
        self.result_dir = result_dir
