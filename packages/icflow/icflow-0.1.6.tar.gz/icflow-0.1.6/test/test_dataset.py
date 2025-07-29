from pathlib import Path
from functools import partial

from iccore.runtime import ctx
from icflow.data import dataset, Dataset


class MockRemoteHost:

    def __init__(self) -> None:
        self.last_upload_src: Path | None = None
        self.last_upload_tgt: Path | None = None
        self.last_download_src: Path | None = None
        self.last_download_tgt: Path | None = None
        self.name = "mock_remote"


def upload(host, name, source_path: Path, target_path: Path):
    host.name = name
    host.last_upload_src = source_path
    host.last_upload_tgt = target_path


def download(host, name, source_path: Path, target_path: Path):
    host.name = name
    host.last_download_src = source_path
    host.last_download_tgt = target_path


def test_base_dataset():

    ctx.set_is_dry_run(True)

    local_dataset_path = Path("my_local_dataset")
    archive_path = Path("dataset_loc/my_dataset/my_dataset.zip")

    ds = Dataset(path=Path("dataset_loc"), name="my_dataset", hostname="localhost")

    host = MockRemoteHost()
    dataset.upload(ds, local_dataset_path, partial(upload, host))

    assert host.last_upload_src == local_dataset_path
    assert host.last_upload_tgt == archive_path

    dataset.download(ds, local_dataset_path, partial(download, host))
    assert host.last_download_src == archive_path
    assert host.last_download_tgt == local_dataset_path
