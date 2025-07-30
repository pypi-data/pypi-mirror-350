from datetime import datetime
from uuid import UUID

from ed_domain.core.entities.bill import Bill, BillStatus, Money
from pydantic import BaseModel


class BillDto(BaseModel):
    id: UUID
    amount: Money
    bill_status: BillStatus
    due_date: datetime

    @classmethod
    def from_bill(cls, bill: Bill) -> "BillDto":
        return cls(
            id=bill["id"],
            amount=bill["amount"],
            bill_status=bill["bill_status"],
            due_date=bill["due_date"],
        )
