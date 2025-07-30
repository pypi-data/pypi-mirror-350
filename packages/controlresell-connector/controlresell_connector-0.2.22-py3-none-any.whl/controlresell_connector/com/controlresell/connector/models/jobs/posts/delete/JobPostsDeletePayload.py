from pydantic import BaseModel
from uuid import UUID

class JobPostsDeletePayload(BaseModel):
    accountId: UUID
    platformId: str
