from pydantic import BaseModel
from typing import Optional

class GenericJobError(BaseModel):
    error: Optional[str] = None
