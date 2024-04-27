from pytest import fixture
import base64

def pytest_addoption(parser):
    parser.addoption(
        "--ado_config",
        action="store"
    )

@fixture()
def ado_config(request):
    encoded_value = request.config.getoption("--ado_config")
    decoded_value = base64.b64decode(encoded_value).decode()
    return decoded_value