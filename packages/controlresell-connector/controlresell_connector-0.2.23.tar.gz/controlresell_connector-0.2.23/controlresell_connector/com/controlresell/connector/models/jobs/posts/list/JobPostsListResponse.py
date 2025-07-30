from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostListed import JobPostListed
from typing import Any
from typing import Optional

class JobPostsListResponse(BaseModel):
    posts: list[JobPostListed]
    condition: Optional[Any] = None
    nextOffset: Optional[str] = None
