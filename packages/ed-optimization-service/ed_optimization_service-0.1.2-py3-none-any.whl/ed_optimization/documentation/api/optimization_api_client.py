from ed_domain.documentation.api.definitions import ApiResponse
from ed_domain.queues.ed_optimization.order_model import OrderModel

from ed_optimization.common.api_helpers import ApiClient
from ed_optimization.documentation.api.abc_optimization_api_client import \
    ABCOptimizationApiClient
from ed_optimization.documentation.api.optimization_endpoint_descriptions import \
    OptimizationEndpointDescriptions


class OptimizationApiClient(ABCOptimizationApiClient):
    def __init__(self, core_api: str) -> None:
        self._endpoints = OptimizationEndpointDescriptions(core_api)

    def create_order(self, order_model: OrderModel) -> ApiResponse[None]:
        endpoint = self._endpoints.get_description("create_order")
        api_client = ApiClient[None](endpoint)

        return api_client({"request": order_model})
