from pytest import fixture
import base64
import json


def decode_list(encoded_list_values):
    decoded_string = base64.b64decode(encoded_list_values).decode()
    list_values = json.loads(decoded_string)
    return list_values

@fixture()
def ado_config(request):
    encoded_value = request.config.getoption("--ado_config")
    decoded_value = decode_list(encoded_value)
    return decoded_value


# Test Run ID
@fixture()
def test_run_id(request):
    value = request.config.getoption("--test_run_id")
    return value

# Test Result ID
@fixture()
def test_result_id(request):
    value = request.config.getoption("--test_result_id")
    return value

@fixture()
def ado_url(request):
    value = request.config.getoption("--ado_url")
    return value

@fixture()
def ado_pat(request):
    value = request.config.getoption("--ado_pat")
    return value

@fixture()
def ado_project(request):
    value = request.config.getoption("--ado_project")
    return value

@fixture()
def print_verbose(request):
    value = request.config.getoption("--print_verbose")
    return value


@fixture()
def azure_tenant(request):
    value = request.config.getoption("--azure_tenant")
    return value

@fixture()
def azure_client_id(request):
    value = request.config.getoption("--azure_client_id")
    return value

@fixture()
def azure_secret(request):
    value = request.config.getoption("--azure_secret")
    return value