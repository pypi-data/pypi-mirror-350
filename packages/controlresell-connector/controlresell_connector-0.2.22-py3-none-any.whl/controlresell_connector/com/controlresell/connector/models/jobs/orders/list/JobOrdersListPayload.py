from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class JobOrdersListPayload(BaseModel):
    accountId: UUID
    recent: Optional[bool] = None
    offset: Optional[str] = None
