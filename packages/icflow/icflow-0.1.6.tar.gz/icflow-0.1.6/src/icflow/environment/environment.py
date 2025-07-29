"""
This module has functionality to support running in
a distributed context
"""

import platform
from pathlib import Path

from pydantic import BaseModel

from iccore.serialization import write_model
from icsystemutils.network import info, NetworkInfo
from icsystemutils.cpu import process, cpu_info, Process, CpuInfo


class Environment(BaseModel):
    """
    This holds runtime information for the session, which is mostly
    useful in a distributed setting.
    """

    process: Process
    network: NetworkInfo
    cpu_info: CpuInfo
    node_id: int = 0
    num_nodes: int = 1
    gpus_per_node: int = 1
    platform: str = ""

    @property
    def is_multigpu(self) -> bool:
        return self.gpus_per_node > 1

    @property
    def world_size(self) -> int:
        return self.gpus_per_node * self.num_nodes

    @property
    def global_rank(self) -> int:
        return self.node_id * self.gpus_per_node + self.process.local_rank

    @property
    def is_master_process(self) -> bool:
        """
        Return true if this process has zero global rank
        """
        return self.global_rank == 0


def load(local_rank: int = 0) -> Environment:
    return Environment(
        process=process.load(local_rank),
        network=info.load(),
        cpu_info=cpu_info.read(),
        platform=platform.platform(),
    )


def write(env: Environment, path: Path, filename: str = "environment.json") -> None:
    write_model(env, path / filename)
