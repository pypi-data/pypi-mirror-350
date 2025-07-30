from pydantic import BaseModel
from zodable_idschema import IdSchema

class JobPostsCreateError(BaseModel):
    itemId: IdSchema
