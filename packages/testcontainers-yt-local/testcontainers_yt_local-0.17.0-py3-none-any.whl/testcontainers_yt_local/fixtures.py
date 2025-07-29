import pytest

from testcontainers_yt_local.container import YtLocalContainer


def _get_yt_cluster_fixture(scope: str, auth_enabled: bool = False, cri_jobs_enabled: bool = False):
    @pytest.fixture(scope=scope)
    def the_fixture():
        use_ng_image = auth_enabled or cri_jobs_enabled

        with YtLocalContainer(
                use_ng_image=use_ng_image,
                enable_auth=auth_enabled,
                enable_cri_jobs=cri_jobs_enabled,
                privileged=cri_jobs_enabled,
        ) as _yt_cluster:
            yield _yt_cluster

    return the_fixture


yt_cluster_session = _get_yt_cluster_fixture(scope="session")
yt_cluster_function = _get_yt_cluster_fixture(scope="function")
yt_cluster_module = _get_yt_cluster_fixture(scope="module")
yt_cluster_class = _get_yt_cluster_fixture(scope="class")
yt_cluster_package = _get_yt_cluster_fixture(scope="package")

yt_cluster_with_auth_session = _get_yt_cluster_fixture(scope="session", auth_enabled=True)
yt_cluster_with_auth_function = _get_yt_cluster_fixture(scope="function", auth_enabled=True)
yt_cluster_with_auth_module = _get_yt_cluster_fixture(scope="module", auth_enabled=True)
yt_cluster_with_auth_class = _get_yt_cluster_fixture(scope="class", auth_enabled=True)
yt_cluster_with_auth_package = _get_yt_cluster_fixture(scope="package", auth_enabled=True)

yt_cluster_with_cri_jobs_session = _get_yt_cluster_fixture(scope="session", cri_jobs_enabled=True)
yt_cluster_with_cri_jobs_function = _get_yt_cluster_fixture(scope="function", cri_jobs_enabled=True)
yt_cluster_with_cri_jobs_module = _get_yt_cluster_fixture(scope="module", cri_jobs_enabled=True)
yt_cluster_with_cri_jobs_class = _get_yt_cluster_fixture(scope="class", cri_jobs_enabled=True)
yt_cluster_with_cri_jobs_package = _get_yt_cluster_fixture(scope="package", cri_jobs_enabled=True)

yt_cluster_with_auth_and_cri_jobs_session = _get_yt_cluster_fixture(scope="session", auth_enabled=True, cri_jobs_enabled=True)
yt_cluster_with_auth_and_cri_jobs_function = _get_yt_cluster_fixture(scope="function", auth_enabled=True, cri_jobs_enabled=True)
yt_cluster_with_auth_and_cri_jobs_module = _get_yt_cluster_fixture(scope="module", auth_enabled=True, cri_jobs_enabled=True)
yt_cluster_with_auth_and_cri_jobs_class = _get_yt_cluster_fixture(scope="class", auth_enabled=True, cri_jobs_enabled=True)
yt_cluster_with_auth_and_cri_jobs_package = _get_yt_cluster_fixture(scope="package", auth_enabled=True, cri_jobs_enabled=True)
