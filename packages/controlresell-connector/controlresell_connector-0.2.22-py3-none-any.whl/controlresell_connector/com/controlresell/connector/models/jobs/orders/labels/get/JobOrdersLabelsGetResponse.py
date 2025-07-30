from pydantic import BaseModel
from typing import Optional

class JobOrdersLabelsGetResponse(BaseModel):
    orderId: Optional[str] = None
    labelUrl: str
    transactionId: Optional[str] = None
    shipmentId: Optional[str] = None
