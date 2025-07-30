from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class JobOrdersLabelsCreatePayload(BaseModel):
    accountId: UUID
    transactionId: Optional[str] = None
    conversationId: Optional[str] = None
