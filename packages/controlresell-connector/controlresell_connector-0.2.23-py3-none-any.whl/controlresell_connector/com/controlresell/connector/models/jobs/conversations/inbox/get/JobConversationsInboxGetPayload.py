from pydantic import BaseModel
from uuid import UUID

class JobConversationsInboxGetPayload(BaseModel):
    accountId: UUID
