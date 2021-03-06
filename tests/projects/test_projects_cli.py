import pytest

import mlflow
from mlflow import cli
from mlflow.utils.file_utils import TempDir
from tests.integration.utils import invoke_cli_runner, update_temp_env
from tests.projects.utils import TEST_PROJECT_DIR, GIT_PROJECT_URI


@pytest.mark.large
def test_run_local():
    with TempDir() as tmp:
        with update_temp_env({mlflow.tracking._TRACKING_URI_ENV_VAR: tmp.path()}):
            excitement_arg = 2
            name = "friend"
            res = invoke_cli_runner(cli.run, [TEST_PROJECT_DIR, "-e", "greeter", "-P",
                                              "greeting=hi", "-P", "name=%s" % name,
                                              "-P", "excitement=%s" % excitement_arg])
            assert name in res.output


@pytest.mark.large
def test_run_git():
    with TempDir() as tmp:
        with update_temp_env({mlflow.tracking._TRACKING_URI_ENV_VAR: tmp.path()}):
            res = invoke_cli_runner(cli.run, [GIT_PROJECT_URI, "--no-conda", "-P", "alpha=0.5"])
            assert "python train.py 0.5 0.1" in res.output
