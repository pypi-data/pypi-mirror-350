from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrder import JobOrder
from typing import Optional

class JobOrdersListResponse(BaseModel):
    orders: list[JobOrder]
    nextOffset: Optional[str] = None
