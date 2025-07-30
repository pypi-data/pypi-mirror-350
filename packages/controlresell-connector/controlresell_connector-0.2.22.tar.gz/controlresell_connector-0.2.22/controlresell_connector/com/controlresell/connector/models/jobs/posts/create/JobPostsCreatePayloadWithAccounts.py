from pydantic import BaseModel
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.posts.create.JobPostsCreatePayload import JobPostsCreatePayload

class JobPostsCreatePayloadWithAccounts(BaseModel):
    accountsId: list[UUID]
    payload: JobPostsCreatePayload
