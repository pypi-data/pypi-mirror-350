from uuid import UUID

from pydantic import BaseModel


class DropOffOrderDto(BaseModel):
    order_id: UUID
    driver_id: UUID
    consumer_id: UUID
