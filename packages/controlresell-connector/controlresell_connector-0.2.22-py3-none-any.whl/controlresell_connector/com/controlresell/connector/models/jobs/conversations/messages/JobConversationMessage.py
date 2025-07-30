from pydantic import BaseModel
from typing import Optional
from controlresell_connector.com.controlresell.connector.models.jobs.conversations.messages.JobConversationMessageType import JobConversationMessageType
from controlresell_connector.com.controlresell.connector.models.jobs.conversations.messages.JobConversationMessageOffer import JobConversationMessageOffer
from datetime import datetime

class JobConversationMessage(BaseModel):
    id: str
    body: Optional[str] = None
    photos: Optional[list[str]] = None
    userId: Optional[str] = None
    isHidden: Optional[bool] = None
    type: JobConversationMessageType
    offer: Optional[JobConversationMessageOffer] = None
    createdAt: datetime
