from pydantic import BaseModel

class JobPostsDeleteResponse(BaseModel):
    platformId: str
