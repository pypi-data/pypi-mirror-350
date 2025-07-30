from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.conversations.JobConversation import JobConversation

class JobConversationsGetResponse(BaseModel):
    conversation: JobConversation
