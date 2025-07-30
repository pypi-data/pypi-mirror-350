from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UpdateProxyPayload(BaseModel):
    accountId: Optional[UUID] = None
