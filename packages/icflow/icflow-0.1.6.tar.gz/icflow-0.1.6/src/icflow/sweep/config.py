"""
This module is for a parameter sweep config file
"""

from pathlib import Path
import logging
import itertools

from pydantic import BaseModel

from iccore.serialization import read_yaml
from iccore.dict_utils import merge_dicts, split_dict_on_type
from ictasks.session import Config

logger = logging.getLogger(__name__)


class SweepConfig(BaseModel, frozen=True):
    """
    This class handles reading a parameter sweep config file and
    also expansion of parameter ranges in lists
    """

    title: str
    program: str
    parameters: dict
    stop_on_error: bool = False
    config: Config = Config()

    def get_expanded_params(self) -> list:
        """
        Produce a list of dictionaries from a single dictionary containing list values.
        Each dictionary in this list is a unique permutation from the list entries of
        the original dictionary.
        """
        no_lists, with_lists = split_dict_on_type(self.parameters, list)
        items = []
        list_keys, values = zip(*with_lists.items())
        permutations = itertools.product(*values)
        for perm in permutations:
            perm_dict = dict(zip(list_keys, perm))
            item = merge_dicts(perm_dict, no_lists)
            items.append(item)
        return items


def read(path: Path) -> SweepConfig:
    """
    Read the config from file
    """

    logger.info("Reading config from: %s", path)
    return SweepConfig(**read_yaml(path))
