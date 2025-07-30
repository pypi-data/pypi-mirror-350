from pydantic import BaseModel
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.conversations.messages.JobConversationMessage import JobConversationMessage

class JobConversationsMessagesCreateResponse(BaseModel):
    accountId: UUID
    messageId: UUID
    conversationId: str
    message: JobConversationMessage
