from pydantic import BaseModel
from zodable_idschema import IdSchema
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPost import JobPost

class JobPostsCreatePayload(BaseModel):
    itemId: IdSchema
    post: JobPost
