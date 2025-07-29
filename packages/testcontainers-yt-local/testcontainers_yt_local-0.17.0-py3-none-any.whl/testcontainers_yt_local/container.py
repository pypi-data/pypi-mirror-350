import copy
import os
import logging
from typing import Any, Optional, Dict

import yt.yson
from yt.wrapper.client import YtClient
from deepmerge import always_merger
from typing_extensions import Self

from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_container_is_ready

from testcontainers_yt_local.base import YtBaseInstance


LOGGER = logging.getLogger(__name__)


DEFAULT_CLIENT_CONFIG: Dict[str, Any] = {
    "proxy": {
        "enable_proxy_discovery": False,
    },
    "is_local_mode": True,
}


DEFAULT_IMAGES = {
    "ytsaurus-local-original": "ghcr.io/ytsaurus/local:stable",
    "ytsaurus-local-ng": "ghcr.io/dmi-feo/ytsaurus-local:0.4.0",
}

NG_IMAGE_ADMIN_TOKEN = "topsecret"


class YtContainerInstance(DockerContainer, YtBaseInstance):
    PORT_HTTP = 80
    PORT_RPC = 20069

    def __init__(
        self,
        image: Optional[str] = None,
        use_ng_image: Optional[bool] = None,
        enable_cri_jobs: bool = False,
        enable_auth: bool = False,
        privileged: bool = False,
        set_yt_config_env_var: bool = False,
        **kwargs: Any,
    ):
        super().__init__(image=image, privileged=privileged, **kwargs)

        self._use_ng_image = use_ng_image
        self._enable_cri_jobs = enable_cri_jobs
        self._enable_auth = enable_auth
        self._privileged = privileged
        self._set_yt_config_env_var = set_yt_config_env_var

        self._validate_params()

        if enable_cri_jobs:
            self.env["YTLOCAL_CRI_ENABLED"] = "1"

        if enable_auth:
            self.env["YTLOCAL_AUTH_ENABLED"] = "1"

        if image is None:
            if use_ng_image:
                self.image = DEFAULT_IMAGES["ytsaurus-local-ng"]
            else:
                self.image = DEFAULT_IMAGES["ytsaurus-local-original"]

        if not self._use_ng_image:
            self._command = [
                "--fqdn", "localhost",
                "--rpc-proxy-count", "1",
                "--rpc-proxy-port", str(self.PORT_RPC),
                "--node-count", "1",
            ]

        self.with_exposed_ports(self.PORT_HTTP, self.PORT_RPC)

    def _validate_params(self):
        if self._enable_auth or self._enable_cri_jobs:
            assert self._use_ng_image is True, "Only ng image supports CRI jobs and auth"

        if self._enable_cri_jobs:
            assert self._privileged is True, "CRI jobs require privileged mode"


    @property
    def proxy_url_http(self):
        return f"http://{self.get_container_host_ip()}:{self.get_exposed_port(self.PORT_HTTP)}"

    @property
    def proxy_url_rpc(self):
        return f"http://{self.get_container_host_ip()}:{self.get_exposed_port(self.PORT_RPC)}"

    def get_client(self, config: Optional[Dict[str, Any]] = None, token: str = "") -> YtClient:
        effective_config = always_merger.merge(DEFAULT_CLIENT_CONFIG, config or {})
        return YtClient(
            proxy=self.proxy_url_http,
            config=effective_config,
            token=token,
        )

    def get_client_rpc(self, config: Optional[Dict[str, Any]] = None) -> YtClient:
        effective_config = always_merger.merge(DEFAULT_CLIENT_CONFIG, config or {})
        return YtClient(
            proxy=self.proxy_url_rpc,
            config={**effective_config, "backend": "rpc"},
        )

    def check_container_is_ready(self) -> None:
        yt_client_kwargs = {"token": NG_IMAGE_ADMIN_TOKEN} if self._enable_auth else {}

        try:
            yt_client = self.get_client(**yt_client_kwargs)
            assert {"sys", "home", "tmp"}.issubset(set(yt_client.list("/")))
            if self._use_ng_image:
                marker = "//sys/@ytsaurus_local_ready"
                assert yt_client.exists(marker) and yt_client.get(marker)
        except AssertionError:
            raise
        except Exception as exc:
            LOGGER.info("check_container_is_ready: got exception %r", exc)
            assert False

    @wait_container_is_ready(AssertionError)
    def _wait_container_is_ready(self) -> None:
        self.check_container_is_ready()

    def set_yt_config_env_var(self):
        full_config = copy.deepcopy(DEFAULT_CLIENT_CONFIG)
        full_config["proxy"]["url"] = self.proxy_url_http
        full_config["token"] = ""
        os.environ["YT_CONFIG_PATCHES"] = yt.yson.dumps(full_config).decode()

    def start(self) -> Self:
        super().start()
        self._wait_container_is_ready()

        if self._set_yt_config_env_var:
            self.set_yt_config_env_var()

        return self


YtLocalContainer = YtContainerInstance  # for backward compatibility
