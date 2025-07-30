from pydantic import BaseModel
from uuid import UUID

class JobPostsGetPayload(BaseModel):
    accountId: UUID
    platformId: str
