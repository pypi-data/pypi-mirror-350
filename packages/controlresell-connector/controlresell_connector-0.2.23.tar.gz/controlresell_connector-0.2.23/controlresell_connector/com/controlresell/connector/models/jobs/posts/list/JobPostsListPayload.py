from pydantic import BaseModel
from uuid import UUID
from typing import Any
from typing import Optional

class JobPostsListPayload(BaseModel):
    accountId: UUID
    condition: Optional[Any] = None
    offset: Optional[str] = None
