from pydantic import BaseModel
from typing import Optional

class JobOrdersLabelsCreateError(BaseModel):
    reason: Optional[str] = None
