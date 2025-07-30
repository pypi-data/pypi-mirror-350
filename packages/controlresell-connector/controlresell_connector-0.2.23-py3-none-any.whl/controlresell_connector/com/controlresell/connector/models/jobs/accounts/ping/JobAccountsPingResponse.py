from pydantic import BaseModel
from uuid import UUID

class JobAccountsPingResponse(BaseModel):
    accountId: UUID
