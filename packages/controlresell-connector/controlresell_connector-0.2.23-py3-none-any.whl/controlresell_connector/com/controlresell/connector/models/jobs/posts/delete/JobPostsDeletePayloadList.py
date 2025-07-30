from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.posts.delete.JobPostsDeletePayload import JobPostsDeletePayload

class JobPostsDeletePayloadList(BaseModel):
    payloads: list[JobPostsDeletePayload]
