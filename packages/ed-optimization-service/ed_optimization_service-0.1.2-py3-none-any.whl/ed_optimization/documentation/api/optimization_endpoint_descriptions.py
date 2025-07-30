from ed_domain.documentation.api.abc_endpoint_descriptions import \
    ABCEndpointDescriptions
from ed_domain.documentation.api.definitions import (EndpointDescription,
                                                     HttpMethod)
from ed_domain.queues.ed_optimization.order_model import OrderModel


class OptimizationEndpointDescriptions(ABCEndpointDescriptions):
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._descriptions: list[EndpointDescription] = [
            {
                "name": "create_order",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/orders",
                "request_model": OrderModel,
            },
        ]

    @property
    def descriptions(self) -> list[EndpointDescription]:
        return self._descriptions
