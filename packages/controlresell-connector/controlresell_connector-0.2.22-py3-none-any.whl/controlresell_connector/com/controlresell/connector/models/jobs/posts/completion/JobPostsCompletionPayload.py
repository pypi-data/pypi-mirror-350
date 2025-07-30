from pydantic import BaseModel
from zodable_idschema import IdSchema
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPost import JobPost

class JobPostsCompletionPayload(BaseModel):
    accountId: UUID
    itemId: IdSchema
    platformId: str
    post: JobPost
