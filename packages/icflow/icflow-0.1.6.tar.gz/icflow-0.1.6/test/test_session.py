from iccore.test_utils import get_test_output_dir

from icflow.session import Session
from icflow import environment


def test_session():

    work_dir = get_test_output_dir()

    env = environment.load()

    _ = Session(env, work_dir)
