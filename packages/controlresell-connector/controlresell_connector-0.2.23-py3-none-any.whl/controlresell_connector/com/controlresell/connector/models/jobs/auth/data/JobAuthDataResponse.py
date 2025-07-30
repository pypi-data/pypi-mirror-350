from pydantic import BaseModel
from typing import Optional
from controlresell_connector.com.controlresell.connector.models.jobs.auth.data.UserAddress import UserAddress

class JobAuthDataResponse(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    userAddress: Optional[UserAddress] = None
