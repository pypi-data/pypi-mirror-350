from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class VmStopRequest(BaseModel):
    accountId: UUID
    lastTask: datetime
    check: int
