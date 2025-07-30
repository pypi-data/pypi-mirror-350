from pydantic import BaseModel

class JobAuthLoginError(BaseModel):
    key: str
