from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from controlresell_connector.com.controlresell.connector.models.jobs.conversations.JobConversationUserRole import JobConversationUserRole

class JobConversationsOffersUpdatePayload(BaseModel):
    accountId: UUID
    transactionId: Optional[str] = None
    conversationId: str
    role: JobConversationUserRole
    offerId: str
    accepted: bool
