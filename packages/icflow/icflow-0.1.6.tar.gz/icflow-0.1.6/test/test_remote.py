import os
from pathlib import Path
from icsystemutils.network import remote


def create_file_with_text(path, content):
    with open(path, "w") as f:
        f.write(content)


def check_file_has_content(path, content):
    assert os.path.exists(path)

    with open(path, "r") as f:
        file_content = f.read()

    assert file_content == content


def test_remote_upload():
    return

    # TODO Add https://pypi.org/project/mock-ssh-server/
    host = remote.Host(name="localhost")

    file_name = "test_remote_upload"
    file_content = "test"

    local_path = Path(os.getcwd()) / f"{file_name}.dat"
    create_file_with_text(local_path, file_content)

    remote_path = Path(os.getcwd()) / f"{file_name}_remote.dat"
    remote.upload(host, local_path, remote_path, None)

    check_file_has_content(remote_path, file_content)
