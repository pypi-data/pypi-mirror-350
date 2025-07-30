from pydantic import BaseModel
from typing import Optional
from controlresell_connector.com.controlresell.connector.models.jobs.conversations.messages.JobConversationMessageOfferStatus import JobConversationMessageOfferStatus

class JobConversationMessageOffer(BaseModel):
    id: str
    transactionId: Optional[str] = None
    price: float
    originalPrice: float
    status: JobConversationMessageOfferStatus
