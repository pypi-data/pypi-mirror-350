from pydantic import BaseModel
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.conversations.offers.JobConversationOffer import JobConversationOffer

class JobConversationsOffersCreateResponse(BaseModel):
    offerId: UUID
    offer: JobConversationOffer
