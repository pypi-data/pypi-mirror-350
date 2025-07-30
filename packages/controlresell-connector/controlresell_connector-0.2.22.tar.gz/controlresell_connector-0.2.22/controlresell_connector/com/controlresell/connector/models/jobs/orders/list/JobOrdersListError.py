from pydantic import BaseModel
from typing import Optional

class JobOrdersListError(BaseModel):
    reason: Optional[str] = None
