from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_optimization.application.common.responses.base_response import \
    BaseResponse
from ed_optimization.application.features.order.dtos.create_order_dto import \
    CreateOrderDto


@request(BaseResponse[None])
@dataclass
class ProcessOrderCommand(Request):
    model: CreateOrderDto
