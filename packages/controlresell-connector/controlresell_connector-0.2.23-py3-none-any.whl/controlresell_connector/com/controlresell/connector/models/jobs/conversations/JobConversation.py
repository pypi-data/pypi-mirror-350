from pydantic import BaseModel
from typing import Optional
from controlresell_connector.com.controlresell.connector.models.jobs.conversations.messages.JobConversationMessage import JobConversationMessage
from controlresell_connector.com.controlresell.connector.models.jobs.conversations.JobConversationUser import JobConversationUser
from controlresell_connector.com.controlresell.connector.models.jobs.conversations.JobConversationTransaction import JobConversationTransaction
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostListed import JobPostListed
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrder import JobOrder
from controlresell_connector.com.controlresell.connector.models.jobs.orders.labels.get.JobOrdersLabelsGetResponse import JobOrdersLabelsGetResponse

class JobConversation(BaseModel):
    id: str
    readByCurrentUser: Optional[bool] = None
    readByOppositeUser: Optional[bool] = None
    allowReply: Optional[bool] = None
    messages: list[JobConversationMessage]
    users: Optional[list[JobConversationUser]] = None
    transactions: Optional[list[JobConversationTransaction]] = None
    posts: Optional[list[JobPostListed]] = None
    orders: Optional[list[JobOrder]] = None
    labels: Optional[list[JobOrdersLabelsGetResponse]] = None
