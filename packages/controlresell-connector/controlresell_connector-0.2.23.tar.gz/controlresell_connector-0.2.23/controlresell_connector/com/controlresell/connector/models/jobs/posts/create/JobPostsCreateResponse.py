from pydantic import BaseModel
from zodable_idschema import IdSchema

class JobPostsCreateResponse(BaseModel):
    platformId: str
    platformUrl: str
    platformPrice: float
    itemId: IdSchema
