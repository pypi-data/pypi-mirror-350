from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostOptionals import JobPostOptionals

class JobPostListed(BaseModel):
    platformId: str
    platformUrl: Optional[str] = None
    sold: Optional[bool] = None
    createdAt: Optional[datetime] = None
    post: JobPostOptionals
    data: Optional[str] = None
