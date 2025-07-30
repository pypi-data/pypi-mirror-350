from pydantic import BaseModel
from typing import Optional

class JobPost(BaseModel):
    brand: str
    catalog: str
    catalogId: int
    colors: Optional[list[str]] = None
    colorIds: Optional[list[int]] = None
    description: str
    measurementLength: Optional[float] = None
    measurementWidth: Optional[float] = None
    packageSizeId: int
    photoUrls: list[str]
    price: float
    size: Optional[str] = None
    sizeId: Optional[int] = None
    status: str
    statusId: int
    title: str
    isDraft: bool
    material: Optional[list[int]] = None
    manufacturerLabelling: Optional[str] = None
