from pydantic import BaseModel
from zodable_idschema import IdSchema

class JobPostsCompletionError(BaseModel):
    itemId: IdSchema
