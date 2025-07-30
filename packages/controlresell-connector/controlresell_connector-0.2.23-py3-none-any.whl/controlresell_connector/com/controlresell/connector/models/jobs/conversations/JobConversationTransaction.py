from pydantic import BaseModel
from typing import Optional

class JobConversationTransaction(BaseModel):
    id: str
    status: int
    offlineVerification: Optional[bool] = None
    offerId: Optional[int] = None
    buyerId: Optional[int] = None
    sellerId: Optional[int] = None
    isCompleted: Optional[bool] = None
    shippingOrderId: Optional[int] = None
    availableActions: Optional[list[str]] = None
    currentUserSide: Optional[str] = None
    isBundle: Optional[bool] = None
    isReserved: Optional[bool] = None
    isPackageSizeSelected: Optional[bool] = None
    isBusinessSeller: Optional[bool] = None
    itemCount: Optional[int] = None
    itemId: Optional[str] = None
    itemIds: Optional[list[str]] = None
    itemTitle: Optional[str] = None
    itemUrl: Optional[str] = None
    itemIsClosed: Optional[bool] = None
    offerPriceAmount: Optional[str] = None
    offerPriceCurrency: Optional[str] = None
    serviceFeeAmount: Optional[str] = None
    serviceFeeCurrency: Optional[str] = None
    shipmentPriceAmount: Optional[str] = None
    shipmentPriceCurrency: Optional[str] = None
    totalWithoutShipmentAmount: Optional[str] = None
    totalWithoutShipmentCurrency: Optional[str] = None
    totalAmountWithoutTax: Optional[str] = None
    sellerItemCount: Optional[int] = None
    sellerCity: Optional[str] = None
    shipmentId: Optional[str] = None
    shipmentStatus: Optional[int] = None
    packageSizeCode: Optional[str] = None
