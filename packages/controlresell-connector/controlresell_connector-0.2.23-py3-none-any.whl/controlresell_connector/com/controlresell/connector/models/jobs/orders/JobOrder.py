from pydantic import BaseModel
from typing import Optional
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrderStatus import JobOrderStatus
from datetime import datetime

class JobOrder(BaseModel):
    id: str
    conversationId: Optional[str] = None
    transactionId: Optional[str] = None
    price: float
    currencyCode: str
    status: JobOrderStatus
    date: datetime
