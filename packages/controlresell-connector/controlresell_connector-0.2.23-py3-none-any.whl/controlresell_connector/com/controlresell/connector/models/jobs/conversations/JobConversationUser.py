from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobConversationUser(BaseModel):
    id: str
    login: str
    lastLoggedInAt: Optional[datetime] = None
    isSystem: Optional[bool] = None
    reviewCount: Optional[int] = None
    reviewValue: Optional[float] = None
    isOnHoliday: Optional[bool] = None
    isModerator: Optional[bool] = None
    photo: Optional[str] = None
    location: Optional[str] = None
