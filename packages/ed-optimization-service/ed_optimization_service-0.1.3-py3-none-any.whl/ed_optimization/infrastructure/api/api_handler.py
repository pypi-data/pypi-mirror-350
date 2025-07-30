from ed_core.documentation.api.abc_core_api_client import ABCCoreApiClient
from ed_core.documentation.api.core_api_client import CoreApiClient

from ed_optimization.application.contracts.infrastructure.api.abc_api import \
    ABCApi


class ApiHandler(ABCApi):
    def __init__(self, api_url: str) -> None:
        self._core_api = CoreApiClient(api_url)

    @property
    def core_api(self) -> ABCCoreApiClient:
        return self._core_api
