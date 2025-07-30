from pydantic import BaseModel
from uuid import UUID

class JobAccountsPingPayload(BaseModel):
    accountId: UUID
