from pytest import fixture
import base64
import json

def pytest_addoption(parser):
    parser.addoption(
        "--ado_config",
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