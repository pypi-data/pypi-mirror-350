from pydantic import BaseModel

class VintedCredentials(BaseModel):
    username: str
    password: str
