from pydantic import BaseModel
from typing import Optional

class JobConversationsGetError(BaseModel):
    reason: Optional[str] = None
