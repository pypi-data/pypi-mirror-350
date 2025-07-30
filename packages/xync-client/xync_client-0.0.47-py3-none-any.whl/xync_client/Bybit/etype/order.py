from datetime import datetime
from enum import IntEnum
from typing import Literal

from pydantic import BaseModel


class OrderRequest(BaseModel):
    class Side(IntEnum):
        BUY = 0
        SALE = 1

    itemId: str
    tokenId: str
    currencyId: str
    side: Literal["0", "1"]  # 0 покупка, # 1 продажа
    curPrice: str
    quantity: str
    amount: str
    flag: Literal["amount", "quantity"]
    version: str = "1.0"
    securityRiskToken: str = ""


class PreOrderResp(BaseModel):
    price: str  # float
    curPrice: str
    totalAmount: float
    minAmount: float
    maxAmount: float
    minQuantity: float
    maxQuantity: float
    payments: list[str]  # list[int]
    status: Literal[10]
    paymentTerms: list
    paymentPeriod: Literal[15]
    lastQuantity: float
    lastPrice: float
    isOnline: bool
    lastLogoutTime: datetime
    itemPriceAvailableTime: datetime
    itemPriceValidTime: int  # 45000
    itemType: Literal["ORIGIN"]


class OrderResp(BaseModel):
    orderId: str
    isNeedConfirm: bool
    success: bool
    isBulkOrder: bool
    confirmed: str = None
    delayTime: str


class CancelOrderReq(BaseModel):
    orderId: str
    cancelCode: Literal["cancelReason_transferFailed"] = "cancelReason_transferFailed"
    cancelRemark: str = ""
    voucherPictures: str = ""
