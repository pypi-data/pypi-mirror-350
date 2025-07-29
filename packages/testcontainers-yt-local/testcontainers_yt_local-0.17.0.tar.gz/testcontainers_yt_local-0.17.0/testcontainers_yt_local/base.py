import abc
from typing import Any, Optional, Dict

from typing_extensions import Self
from yt.wrapper import YtClient


class YtBaseInstance(abc.ABC):
    @abc.abstractmethod
    def __enter__(self) -> Self:
        pass

    @abc.abstractmethod
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    @property
    @abc.abstractmethod
    def proxy_url_http(self) -> str:
        pass

    @abc.abstractmethod
    def get_client(self, config: Optional[Dict[str, Any]] = None) -> YtClient:
        pass
