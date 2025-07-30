from datetime import datetime
from typing import TypedDict
from uuid import UUID

from ed_domain.core.entities.order import Parcel

from ed_optimization.application.features.order.dtos.create_business_dto import \
    CreateBusinessDto
from ed_optimization.application.features.order.dtos.create_consumer_dto import \
    CreateConsumerDto


class CreateOrderDto(TypedDict):
    id: UUID
    consumer: CreateConsumerDto
    business: CreateBusinessDto
    latest_time_of_delivery: datetime
    parcel: Parcel
    create_datetime: datetime
