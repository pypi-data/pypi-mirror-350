from pydantic import BaseModel

class JobAuthOtpPayload(BaseModel):
    otp: str
