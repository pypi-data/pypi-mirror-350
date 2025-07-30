from uuid import UUID

from pydantic import BaseModel


class PickUpOrderDto(BaseModel):
    order_id: UUID
    driver_id: UUID
    business_id: UUID
