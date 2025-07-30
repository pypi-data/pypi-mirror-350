from pydantic import BaseModel
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.accounts.AccountPlatform import AccountPlatform
from typing import Optional

class AccountLabels(BaseModel):
    id: UUID
    platform: AccountPlatform
    name: Optional[str] = None
    username: Optional[str] = None
