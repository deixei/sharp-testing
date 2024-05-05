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
        parser.addoption("--ado_config",action="store")
        parser.addoption("--test_run_id",action="store")
        parser.addoption("--test_result_id",action="store")

        parser.addoption("--ado_url",action="store")
        parser.addoption("--ado_pat",action="store")
        parser.addoption("--ado_project",action="store")
        parser.addoption("--print_verbose",action="store")

        parser.addoption("--azure_tenant",action="store")
        parser.addoption("--azure_client_id",action="store")
        parser.addoption("--azure_secret",action="store")

