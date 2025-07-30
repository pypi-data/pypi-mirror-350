from pydantic import BaseModel
from zodable_idschema import IdSchema

class JobPostsCompletionResponse(BaseModel):
    itemId: IdSchema
    platformId: str
