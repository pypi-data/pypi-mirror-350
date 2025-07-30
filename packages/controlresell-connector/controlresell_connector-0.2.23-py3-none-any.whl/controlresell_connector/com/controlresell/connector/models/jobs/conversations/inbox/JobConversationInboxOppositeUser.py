from pydantic import BaseModel

class JobConversationInboxOppositeUser(BaseModel):
    id: str
    login: str
