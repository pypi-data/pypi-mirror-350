from pydantic import BaseModel
from typing import Optional

class JobOrdersLabelsCreateResponse(BaseModel):
    transactionId: Optional[str] = None
    shipmentId: Optional[str] = None
