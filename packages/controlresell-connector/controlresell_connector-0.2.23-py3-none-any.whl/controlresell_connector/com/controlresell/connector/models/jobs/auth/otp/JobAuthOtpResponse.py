from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobAuthOtpResponse(BaseModel):
    expiresAt: Optional[datetime] = None
    otp: Optional[int] = None
