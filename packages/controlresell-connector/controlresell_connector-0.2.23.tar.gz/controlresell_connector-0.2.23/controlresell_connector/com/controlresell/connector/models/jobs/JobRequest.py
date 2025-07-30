from pydantic import BaseModel
from typing import Generic
from typing import TypeVar
from controlresell_connector.com.controlresell.connector.models.accounts.Account import Account

T = TypeVar('T')
class JobRequest(BaseModel, Generic[T]):
    account: Account
    payload: T
