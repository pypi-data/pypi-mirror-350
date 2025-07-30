from typing import TypedDict
from uuid import UUID

from ed_optimization.application.features.order.dtos.create_location_dto import \
    CreateLocationDto


class CreateBusinessDto(TypedDict):
    id: UUID
    location: CreateLocationDto
