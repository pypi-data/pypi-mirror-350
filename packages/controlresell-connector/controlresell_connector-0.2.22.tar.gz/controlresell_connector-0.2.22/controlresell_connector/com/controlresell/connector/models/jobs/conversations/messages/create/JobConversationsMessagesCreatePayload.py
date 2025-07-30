from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class JobConversationsMessagesCreatePayload(BaseModel):
    accountId: UUID
    messageId: UUID
    conversationId: str
    message: str
    photoUrl: Optional[list[str]] = None
