from pytest import fixture


def pytest_addoption(parser):
    parser.addoption(
        "--ado_config",
        action="store"
    )

@fixture()
def ado_config(request):
    return request.config.getoption("--ado_config")