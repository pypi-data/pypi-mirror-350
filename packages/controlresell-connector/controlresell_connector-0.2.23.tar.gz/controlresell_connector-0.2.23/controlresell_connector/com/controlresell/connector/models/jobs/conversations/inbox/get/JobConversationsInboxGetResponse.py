from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.conversations.inbox.JobConversationInbox import JobConversationInbox

class JobConversationsInboxGetResponse(BaseModel):
    conversations: list[JobConversationInbox]
