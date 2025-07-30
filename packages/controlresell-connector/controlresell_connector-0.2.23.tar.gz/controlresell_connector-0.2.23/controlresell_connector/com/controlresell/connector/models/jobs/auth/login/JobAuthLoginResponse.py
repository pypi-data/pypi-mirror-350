from pydantic import BaseModel
from uuid import UUID

class JobAuthLoginResponse(BaseModel):
    accountId: UUID
