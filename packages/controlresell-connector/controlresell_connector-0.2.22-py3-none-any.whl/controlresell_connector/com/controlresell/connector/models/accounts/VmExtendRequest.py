from pydantic import BaseModel
from uuid import UUID

class VmExtendRequest(BaseModel):
    accountId: UUID
    check: int
