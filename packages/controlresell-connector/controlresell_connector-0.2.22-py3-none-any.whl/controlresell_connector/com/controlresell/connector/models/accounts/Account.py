from pydantic import BaseModel
from zodable_idschema import IdSchema
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.accounts.AccountPlatform import AccountPlatform
from typing import Optional
from datetime import datetime

class Account(BaseModel):
    id: UUID
    platform: AccountPlatform
    ownerId: IdSchema
    credentials: Optional[str] = None
    data: Optional[str] = None
    lastTask: Optional[datetime] = None
