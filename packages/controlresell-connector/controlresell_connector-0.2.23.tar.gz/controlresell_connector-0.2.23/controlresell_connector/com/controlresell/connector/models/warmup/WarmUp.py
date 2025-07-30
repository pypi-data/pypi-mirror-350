from pydantic import BaseModel
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.accounts.AccountPlatform import AccountPlatform

class WarmUp(BaseModel):
    id: UUID
    platform: AccountPlatform
