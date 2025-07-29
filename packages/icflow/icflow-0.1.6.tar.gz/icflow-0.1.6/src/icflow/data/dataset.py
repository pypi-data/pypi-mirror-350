"""
This module has functionaly for handling generic datasets.
"""

from pathlib import Path
import logging
from typing import Callable

from pydantic import BaseModel

from iccore import filesystem as fs
from icsystemutils.network import remote

logger = logging.getLogger(__name__)


class Dataset(BaseModel, frozen=True):
    """
    This class represents a named dataset with a location,
    which can be on a remote system.
    """

    path: Path
    name: str = ""
    archive_name_override: str = ""
    hostname: str = ""

    @property
    def archive_name(self) -> str:
        if self.archive_name_override:
            return self.archive_name
        return self.name + ".zip"

    @property
    def is_readable(self) -> bool:
        return self.path.exists()


def archive(dataset: Dataset, dst: Path) -> None:
    """
    Archive the dataset in the provided location
    """
    archive_name, archive_format = dataset.archive_name.split(".")
    fs.make_archive(Path(archive_name), archive_format, dst)


def _get_archive_path(dataset: Dataset) -> Path:
    return dataset.path / Path(dataset.name) / Path(dataset.archive_name)


def upload(dataset: Dataset, loc: Path, upload_func: Callable | None = None) -> None:
    """
    Upload the dataset to the given path
    """
    archive_path = _get_archive_path(dataset)
    if loc.is_dir():
        logger.info("Zipping dataset %s", dataset.archive_name)
        archive(dataset, loc)
        logger.info("Finished zipping dataset %s", dataset.archive_name)
        loc = loc / dataset.archive_name
    if dataset.hostname:
        logger.info(
            "Uploading %s to remote at %s:%s", loc, dataset.hostname, archive_path
        )

        if upload_func:
            upload_func(dataset.hostname, loc, archive_path)
        else:
            remote.upload(loc, remote.Host(name=dataset.hostname), archive_path, None)
        logger.info("Finished Uploading %s to %s", loc, archive_path)
    else:
        logger.info("Doing local copy of %s to %s", loc, archive_path)
        fs.copy(loc, archive_path)
        logger.info("Finished local copy of %s to %s", loc, archive_path)


def download(
    dataset: Dataset, loc: Path, download_func: Callable | None = None
) -> None:
    """
    Download the dataset from the given path
    """
    archive_path = _get_archive_path(dataset)
    if dataset.hostname:
        remote_loc = f"{dataset.hostname}:{archive_path}"
        logger.info("Downloading remote %s to %s", remote_loc, loc)
        if download_func:
            download_func(dataset.hostname, archive_path, loc)
        else:
            remote.download(remote.Host(name=dataset.hostname), archive_path, loc, None)
    else:
        logger.info("Copying %s to %s", archive_path, loc)
        fs.copy(archive_path, loc)

    archive_loc = loc / dataset.archive_name
    logger.info("Unpacking %s to %s", archive_path, loc)
    fs.unpack_archive(archive_loc, loc)
