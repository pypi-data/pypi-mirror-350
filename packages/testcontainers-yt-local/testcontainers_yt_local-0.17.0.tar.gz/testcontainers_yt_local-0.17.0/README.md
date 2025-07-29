A way to run https://ytsaurus.tech/docs/en/overview/try-yt#using-docker via testcontainers.

Pypi: https://pypi.org/project/testcontainers-yt-local/

## Installation

```shell
pip install testcontainers-yt-local
```

or (to install pytest fixtures also)

```shell
pip install "testcontainers-yt-local[pytest]"
```

## Usage
```python
from testcontainers_yt_local.container import YtContainerInstance


with YtContainerInstance() as yt:
    yt_cli = yt.get_client()
    print(yt_cli.list("/"))
```

or use a fixture (requires `testcontainers-yt-local[pytest]` installed)
```python
def test_with_fixture(yt_cluster_function):
    # there is a bunch of fixtures available:
    # yt_cluster_session, yt_cluster_function, yt_cluster_module, yt_cluster_class, yt_cluster_package.
    # The only difference is their scope.
    url = f"{yt_cluster_function.proxy_url_http}/ping"
    r = requests.get(url)
    assert r.status_code == 200
```
