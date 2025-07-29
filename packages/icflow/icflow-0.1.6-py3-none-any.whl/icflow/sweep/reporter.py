"""
This module allows reporting on past or current parameter sweeps.
"""

import logging
import csv
from typing import Callable
from pathlib import Path

import ictasks
from ictasks.task import Task
from icsystemutils.monitor.sample import Sample
from icplot.graph import Plot, matplotlib, LinePlotSeries, PlotAxis, Color

logger = logging.getLogger()


def deserialize_args(cli_args: str, delimiter: str = "--") -> dict[str, str]:
    """
    Convert command line args in the form 'program --key0 value0 --key1 value1'
    to a dict of key value pairs.
    """
    stripped_entries = cli_args.split(" ")
    args: dict = {}
    last_key = ""
    for entry in stripped_entries:
        if entry.startswith(delimiter):
            if last_key:
                # Flag
                args[last_key] = ""
            last_key = entry[len(delimiter) :]
        else:
            if last_key:
                args[last_key] = entry
                last_key = ""
    return args


def task_params_in_range(task: Task, config: dict[str, dict]) -> bool:
    """
    Check that this task's parameters are in line with the upper and lower bounds
    and specific values given in the config.
    """

    for key, value in deserialize_args(task.launch_cmd).items():
        if key not in config:
            continue
        param = config[key]

        if "range" in param:
            value_range = param["range"]
            if "lower" in value_range:
                if value < param["lower"]:
                    return False
            if "upper" in value_range:
                if value > param["upper"]:
                    return False
        if "values" in param:
            values = param["values"]
            if "exclude" in values:
                if value in values["exclude"]:
                    return False
            if "include" in values:
                if value not in values["include"]:
                    return False
    return True


def filter_tasks_with_config(
    tasks: list[Task], config: dict, predicate: Callable
) -> list[Task]:
    return [t for t in tasks if predicate(t, config)]


def find_time_point(
    task: Task,
    event_type: str,
    cores_argument: str = "",
) -> dict[str, float | str]:
    time_point: dict[str, float | str] = {}
    time_point["event"] = event_type
    if cores_argument:
        args = deserialize_args(task.launch_cmd)
        time_point["cores"] = int(args[cores_argument])
    if event_type == "launch":
        time_point["time"] = task.launch_time
    else:
        time_point["time"] = task.finish_time
    return time_point


def find_tasks_launch_finish(tasks_dir: Path, cores_argument: str = ""):
    tasks = ictasks.task.read_all(tasks_dir)
    launch_points: list[dict] = []
    finish_points: list[dict] = []
    for task in tasks:
        launch_points.append(find_time_point(task, "launch", cores_argument))
        finish_points.append(find_time_point(task, "finish", cores_argument))
    launch_points.sort(key=lambda d: d["time"])
    finish_points.sort(key=lambda d: d["time"])
    return launch_points, finish_points


def find_point_iterator(point):
    if "cores" in point:
        return point["cores"]
    return 1


def find_task_timeline(tasks_dir: Path, cores_argument: str = ""):
    launch_points, finish_points = find_tasks_launch_finish(tasks_dir, cores_argument)
    n_tasks_cores = 0
    # Initialize task_timelines with an initial point before first task launch
    task_timelines: dict[float, int] = {launch_points[0]["time"] - 0.01: n_tasks_cores}
    finish_i = 0
    for launch_point in launch_points:
        launch_time = launch_point["time"]
        finish_point = finish_points[finish_i]
        finish_time = finish_point["time"]
        if finish_time < launch_time:
            n_tasks_cores -= find_point_iterator(finish_point)
            if finish_time < launch_time - 0.1:
                task_timelines[finish_time] = n_tasks_cores
            finish_i += 1
        n_tasks_cores += find_point_iterator(launch_point)
        task_timelines[launch_time] = n_tasks_cores

    # Plot task/core values for the remaining finish points
    for finish_point in finish_points[finish_i:]:
        n_tasks_cores -= find_point_iterator(finish_point)
        task_timelines[finish_point["time"]] = n_tasks_cores

    return task_timelines


def monitor_plot(sweep_dir: Path, cores_argument: str = ""):

    monitor_dir = sweep_dir / "monitor"
    tasks_dir = sweep_dir / "tasks"

    with open(monitor_dir / "monitor.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        samples = [Sample(**dict(row)) for row in reader]

    task_timeline = find_task_timeline(tasks_dir, cores_argument)

    task_times = list(task_timeline.keys())
    n_tasks_cores = list(task_timeline.values())

    sample_times = [s.sample_time for s in samples]
    cpu_percent = [s.cpu_percent for s in samples]
    memory_percent = [s.memory_percent for s in samples]

    # Normalize times
    min_time = min(task_times[0], sample_times[0])
    task_times = [t - min_time for t in task_times]
    monitor_times = [t - min_time for t in sample_times]

    cpu_series = LinePlotSeries(x=monitor_times, y=cpu_percent, label="cpu", marker="")
    memory_series = LinePlotSeries(
        x=monitor_times, y=memory_percent, label="memory", marker=""
    )
    task_cores_series = LinePlotSeries(
        x=task_times,
        y=n_tasks_cores,
        label="current tasks/cores",
        position_right=True,
        drawstyle="steps-post",
        marker=".",
        highlight=True,
        color=Color(),
    )

    twin_label = "Number of running tasks"
    if cores_argument:
        twin_label = "Number of cores being used"
    tasks_axis = PlotAxis(
        label=twin_label,
    )
    cpu_plot = Plot(
        title="CPU usage and concurrent tasks during the sweep against time.",
        x_axis=PlotAxis(label="Time (s)"),
        y_axes=[
            PlotAxis(
                label="CPU usage (Percent)",
            ),
            tasks_axis,
        ],
        line_series=[cpu_series, task_cores_series],
        legend="none",
    )

    memory_plot = Plot(
        title="Memory usage and concurrent tasks during the sweep against time.",
        x_axis=PlotAxis(label="Time (s)"),
        y_axes=[
            PlotAxis(
                label="Memory usage (Percent)",
            ),
            tasks_axis,
        ],
        line_series=[memory_series, task_cores_series],
        legend="none",
    )

    matplotlib.render(cpu_plot, monitor_dir / "monitor_cpu.svg")
    matplotlib.render(memory_plot, monitor_dir / "monitor_memory.svg")
