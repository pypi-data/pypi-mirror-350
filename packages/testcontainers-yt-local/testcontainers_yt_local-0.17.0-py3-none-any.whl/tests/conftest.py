import pytest


pytest_plugins = ["testcontainers_yt_local"]


@pytest.fixture(scope="function", params=[False, True], ids=["default", "ng"])
def use_ng_image(request):
    return request.param
