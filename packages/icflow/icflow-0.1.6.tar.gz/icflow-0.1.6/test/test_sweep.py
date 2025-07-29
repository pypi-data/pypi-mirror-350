#!/usr/bin/env python3

import shutil

from iccore.test_utils import get_test_data_dir, get_test_output_dir
import ictasks.task
from ictasks.task import Task

import icflow
import icflow.sweep
import icflow.sweep.reporter


def test_parameter_sweep():

    work_dir = get_test_output_dir()
    data_dir = get_test_data_dir()

    config_path = data_dir / "parameter_sweep_example.yaml"
    config = icflow.sweep.config.read(config_path)

    sweep_dir = icflow.sweep.run(config, work_dir, config_path)

    icflow.sweep.reporter.monitor_plot(sweep_dir)

    shutil.rmtree(work_dir)


def test_parameter_sweep_reporter():

    tasks = [
        Task(
            id="complete_task",
            launch_cmd="python3 fake.py --complete",
            state="finished",
            pid=21,
        ),
        Task(
            id="incomplete_task",
            launch_cmd="python3 fake.py --incomplete",
            state="created",
            pid=22,
        ),
    ]

    task_str = ictasks.task.tasks_to_str(
        [t for t in tasks if t.finished], ["id", "launch_cmd", "pid"]
    )

    assert "id: complete_task" in task_str
    assert "id: incomplete_task" not in task_str
    assert "launch_cmd: python3 fake.py --complete" in task_str
    assert "launch_cmd: python3 fake.py --incomplete" not in task_str
    assert "pid: 21" in task_str
    assert "pid: 22" not in task_str


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--parameter_str_array", type=str, help="Path to config file")
    parser.add_argument("--parameter_int_array", type=int, help="Path to config file")
    parser.add_argument(
        "--parameter_boolean",
        action="store_true",
        dest="boolean",
        default=False,
        help="Path to config file",
    )
    parser.add_argument("--parameter_string", type=str, help="Path to config file")
    parser.add_argument("--parameter_int", type=int, help="Path to config file")
    args = parser.parse_args()

    print(f"parameter_str_array: {args.parameter_str_array}")
    print(f"parameter_int_array: {args.parameter_int_array}")
    print(f"parameter_string: {args.parameter_string}")
    print(f"parameter_int: {args.parameter_int}")
