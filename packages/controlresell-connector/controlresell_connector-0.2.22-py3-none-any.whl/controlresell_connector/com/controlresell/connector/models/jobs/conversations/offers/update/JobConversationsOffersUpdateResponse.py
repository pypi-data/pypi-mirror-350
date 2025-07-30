from pydantic import BaseModel
from typing import Optional

class JobConversationsOffersUpdateResponse(BaseModel):
    transactionId: Optional[str] = None
    conversationId: str
    offerId: str
    accepted: bool
