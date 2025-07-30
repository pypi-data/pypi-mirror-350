from pydantic import BaseModel

class JobConversationOffer(BaseModel):
    id: str
    price: float
    currency: str
    transactionId: str
