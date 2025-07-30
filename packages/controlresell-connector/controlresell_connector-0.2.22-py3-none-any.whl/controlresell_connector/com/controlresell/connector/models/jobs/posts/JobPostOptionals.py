from pydantic import BaseModel
from typing import Optional

class JobPostOptionals(BaseModel):
    brand: Optional[str] = None
    catalogId: Optional[int] = None
    colorIds: Optional[list[int]] = None
    description: Optional[str] = None
    measurementLength: Optional[float] = None
    measurementWidth: Optional[float] = None
    packageSizeId: Optional[int] = None
    photoUrls: Optional[list[str]] = None
    price: Optional[float] = None
    sizeId: Optional[int] = None
    statusId: Optional[int] = None
    title: Optional[str] = None
    isDraft: Optional[bool] = None
    material: Optional[list[int]] = None
    manufacturerLabelling: Optional[str] = None
