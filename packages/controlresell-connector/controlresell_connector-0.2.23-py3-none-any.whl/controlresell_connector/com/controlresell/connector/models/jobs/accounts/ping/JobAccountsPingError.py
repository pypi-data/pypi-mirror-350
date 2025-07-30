from pydantic import BaseModel
from uuid import UUID

class JobAccountsPingError(BaseModel):
    accountId: UUID
