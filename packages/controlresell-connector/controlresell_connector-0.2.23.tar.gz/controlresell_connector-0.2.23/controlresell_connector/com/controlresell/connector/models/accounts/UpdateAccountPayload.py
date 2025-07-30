from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UpdateAccountPayload(BaseModel):
    credentials: Optional[str] = None
    data: Optional[str] = None
    lastTask: Optional[datetime] = None
