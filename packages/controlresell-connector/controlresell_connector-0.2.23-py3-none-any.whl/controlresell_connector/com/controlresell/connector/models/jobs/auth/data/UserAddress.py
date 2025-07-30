from pydantic import BaseModel
from typing import Optional

class UserAddress(BaseModel):
    id: str
    userId: str
    countryId: int
    entryType: int
    name: str
    postalCode: str
    city: str
    state: str
    line1: str
    line2: Optional[str] = None
    createdAt: str
    isComplete: bool
    countryCode: str
    countryIsoCode: str
    country: str
