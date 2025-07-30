from pydantic import BaseModel
from uuid import UUID

class JobConversationsGetPayload(BaseModel):
    accountId: UUID
    conversationId: str
