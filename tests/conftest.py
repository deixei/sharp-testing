from pytest import fixture
import base64
import json

def pytest_addoption(parser):
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