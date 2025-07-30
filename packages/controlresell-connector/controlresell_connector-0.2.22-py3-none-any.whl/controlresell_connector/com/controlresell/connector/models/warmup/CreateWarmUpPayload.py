from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.accounts.AccountPlatform import AccountPlatform

class CreateWarmUpPayload(BaseModel):
    platform: AccountPlatform
