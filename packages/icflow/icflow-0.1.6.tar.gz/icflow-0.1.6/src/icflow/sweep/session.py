"""
This module allows a parameter sweep to be performed.
"""

import logging
import uuid
import shutil
import os
import queue
from pathlib import Path
from functools import partial

from iccore import time_utils
from iccore.cli_utils import serialize_args
from icsystemutils import monitor
import ictasks
from ictasks.task import Task

from icflow import environment

from .config import SweepConfig

logger = logging.getLogger()


def run(
    config: SweepConfig,
    work_dir: Path = Path(os.getcwd()),
    config_path: Path | None = None,
) -> Path:
    """
    Run a parameter sweep defined by the config.

    :param config: The config to control the sweep
    :param work_dir: Directory to run the sweep in
    :param config_path: If provided will copy the config into the work dir
    """

    timestamp = time_utils.get_timestamp_for_paths()
    resume_sweep = in_sweep_dir(work_dir)
    if not resume_sweep:
        sweep_dir = work_dir / f"sweep_{config.title}_{timestamp}"
        os.makedirs(sweep_dir)
    else:
        sweep_dir = work_dir
    task_dir = sweep_dir / "tasks"

    if not resume_sweep:
        if config_path:
            shutil.copyfile(config_path, sweep_dir / "sweep_config.yaml")
        tasks = [
            Task(
                id=str(uuid.uuid4()),
                launch_cmd=f"{config.program} {serialize_args(args)}",
            )
            for args in config.get_expanded_params()
        ]
    else:
        tasks = ictasks.task.read_all(work_dir / "tasks")
        tasks = [t for t in tasks if not t.finished or t.return_code != 0]

    task_queue: queue.Queue[Task] = queue.Queue()
    for task in tasks:
        task_queue.put(task)

    write_task_func = partial(ictasks.task.write, task_dir)
    for task in tasks:
        write_task_func(task)

    monitor_dir = sweep_dir / "monitor"
    os.makedirs(monitor_dir, exist_ok=True)

    env = environment.load()
    environment.write(env, sweep_dir)

    with monitor.run(sweep_dir / "monitor") as _:
        ictasks.session.run(
            task_queue,
            task_dir,
            config.config,
            on_task_launched=write_task_func,
            on_task_completed=write_task_func,
        )
    return sweep_dir


def in_sweep_dir(work_dir: Path) -> bool:
    config = work_dir / "sweep_config.yaml"
    task_dir = work_dir / "tasks"
    return config.exists() and task_dir.exists()
