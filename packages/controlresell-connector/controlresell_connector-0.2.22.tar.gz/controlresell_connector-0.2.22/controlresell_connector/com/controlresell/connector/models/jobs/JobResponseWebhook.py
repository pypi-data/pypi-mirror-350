from pydantic import BaseModel
from typing import Generic
from typing import TypeVar
from uuid import UUID
from typing import Optional

Response = TypeVar('Response')
Error = TypeVar('Error')
class JobResponseWebhook(BaseModel, Generic[Response, Error]):
    accountId: UUID
    response: Optional[Response] = None
    error: Optional[Error] = None
