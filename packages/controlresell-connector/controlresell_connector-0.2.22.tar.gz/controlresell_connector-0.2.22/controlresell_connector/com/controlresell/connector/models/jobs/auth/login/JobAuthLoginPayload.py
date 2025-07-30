from pydantic import BaseModel
from uuid import UUID

class JobAuthLoginPayload(BaseModel):
    accountId: UUID
