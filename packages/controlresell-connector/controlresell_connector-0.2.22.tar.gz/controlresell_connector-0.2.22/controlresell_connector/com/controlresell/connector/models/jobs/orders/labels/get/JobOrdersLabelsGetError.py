from pydantic import BaseModel
from typing import Optional

class JobOrdersLabelsGetError(BaseModel):
    reason: Optional[str] = None
