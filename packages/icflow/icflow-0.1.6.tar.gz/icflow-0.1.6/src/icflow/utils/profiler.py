"""
This module has functionality for performance profiling
"""

import time
from pathlib import Path


class Profiler:
    """
    Base class for profilers
    """

    def __init__(self, result_dir: Path):
        self.result_dir = result_dir

    def start(self):
        pass

    def stop(self):
        pass


class TimerProfiler(Profiler):
    """
    A simple profiler using a timer
    """

    def __init__(self, result_dir: Path):
        super().__init__(result_dir)
        self.start_time = 0
        self.end_time = 0

    def get_runtime(self):
        return self.end_time - self.start_time

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()


class ProfilerCollection:
    """
    A collection of profilers
    """

    def __init__(self) -> None:
        self.profilers: dict[str, Profiler] = {}

    def add_profiler(self, name: str, profiler: Profiler):
        self.profilers[name] = profiler

    def start(self):
        for profiler in self.profilers.values():
            profiler.start()

    def stop(self):
        for profiler in self.profilers.values():
            profiler.stop()
