from pydantic import BaseModel
from typing import Optional

class JobAccountsHumanActivityResponse(BaseModel):
    data: Optional[str] = None
