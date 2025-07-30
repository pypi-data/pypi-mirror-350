from pydantic import BaseModel
from typing import Optional

class JobPostsListError(BaseModel):
    reason: Optional[str] = None
