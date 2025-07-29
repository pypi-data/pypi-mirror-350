from typing import Any, Optional, Dict

from typing_extensions import Self
from yt.wrapper import YtClient

from testcontainers_yt_local.base import YtBaseInstance


class YtExternalInstance(YtBaseInstance):
    def __init__(self, proxy_url: str, token: str):
        self.proxy_url = proxy_url
        self.token = token

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    @property
    def proxy_url_http(self) -> str:
        return self.proxy_url

    def get_client(self, config: Optional[Dict[str, Any]] = None) -> YtClient:
        return YtClient(
            proxy=self.proxy_url_http,
            config=config,
        )
