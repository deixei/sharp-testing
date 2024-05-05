import pytest
from pytest import fixture
import base64
import json

class TSharpPyTestPlugin:


    def pytest_sessionstart(session):
        print("*** [TSharpPyTestPlugin]: test run reporting starting")

    def pytest_sessionfinish(session, exitstatus):
        print("*** [TSharpPyTestPlugin]: test run reporting finishing")

    def pytest_addoption(self, parser, pluginmanager):
        parser.addoption(
            "--ado_config",
            action="store"
        )

        parser.addoption(
            "--test_run_id",
            action="store"
        )

        parser.addoption(
            "--test_result_id",
            action="store"
        )
