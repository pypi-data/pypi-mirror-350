from pydantic import BaseModel
from uuid import UUID

class JobAccountsHumanActivityPayload(BaseModel):
    accountId: UUID
