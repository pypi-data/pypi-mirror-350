from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostOptionals import JobPostOptionals

class JobPostsUpdateResponse(BaseModel):
    platformId: str
    post: JobPostOptionals
