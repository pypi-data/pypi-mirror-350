from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class Proxy(BaseModel):
    host: str
    port: int
    username: str
    password: str
    accountId: Optional[UUID] = None
