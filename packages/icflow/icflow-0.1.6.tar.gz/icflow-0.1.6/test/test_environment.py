import shutil

from iccore.test_utils import get_test_output_dir
from icflow import environment


def test_runtime_ctx():

    output_dir = get_test_output_dir()

    env = environment.load()

    assert env.cpu_info.cores_per_node > 0
    environment.write(env, output_dir)

    shutil.rmtree(output_dir)
