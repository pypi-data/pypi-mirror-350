from typing import List, Optional, Any, Literal
from pydantic import BaseModel
from xync_schema.types import BaseAd

from xync_client.Abc.types import BaseAdUpdate


class AdsReq(BaseModel):
    tokenId: str
    currencyId: str
    side: Literal["0", "1"]  # 0 покупка, # 1 продажа


class Currency(BaseModel):
    currencyId: str
    exchangeId: str
    id: str
    orgId: str
    scale: int


class Token(BaseModel):
    exchangeId: str
    id: str
    orgId: str
    scale: int
    sequence: int
    tokenId: str


class SymbolInfo(BaseModel):
    buyAd: Optional[Any]
    buyFeeRate: str
    currency: Currency
    currencyId: str
    currencyLowerMaxQuote: str
    currencyMaxQuote: str
    currencyMinQuote: str
    exchangeId: str
    id: str
    itemDownRange: str
    itemSideLimit: int
    itemUpRange: str
    kycCurrencyLimit: str
    lowerLimitAlarm: int
    orderAutoCancelMinute: int
    orderFinishMinute: int
    orgId: str
    sellAd: Optional[Any]
    sellFeeRate: str
    status: int
    token: Token
    tokenId: str
    tokenMaxQuote: str
    tokenMinQuote: str
    tradeSide: int
    upperLimitAlarm: int


class TradingPreferenceSet(BaseModel):
    completeRateDay30: str
    hasCompleteRateDay30: int
    hasNationalLimit: int
    hasOrderFinishNumberDay30: int
    hasRegisterTime: int
    hasUnPostAd: int
    isEmail: int
    isKyc: int
    isMobile: int
    nationalLimit: str
    orderFinishNumberDay30: int
    registerTimeThreshold: int


class Ad(BaseAd):
    accountId: str
    authStatus: int
    authTag: List[str]
    ban: bool
    baned: bool
    blocked: str
    createDate: str
    currencyId: str
    executedQuantity: str
    fee: str
    finishNum: int
    frozenQuantity: str
    id: str
    isOnline: bool
    itemType: str
    lastLogoutTime: str
    lastQuantity: str
    makerContact: bool
    maxAmount: str
    minAmount: str
    nickName: str
    orderNum: int
    paymentPeriod: int
    payments: List[str]
    premium: str
    price: str
    priceType: Literal[0, 1]  # 0 - fix rate, 1 - floating    status: int
    quantity: str
    recentExecuteRate: int
    recentOrderNum: int
    recommend: bool
    recommendTag: str
    remark: str
    side: Literal[0, 1]  # 0 - покупка, 1 - продажа
    symbolInfo: SymbolInfo
    tokenId: str
    tokenName: str
    tradingPreferenceSet: TradingPreferenceSet
    userId: str
    userMaskId: str
    userType: str
    verificationOrderAmount: str
    verificationOrderLabels: List[Any]
    verificationOrderSwitch: bool
    version: int


class AdPostRequest(BaseModel):
    tokenId: str
    currencyId: str
    side: Literal[0, 1]  # 0 - покупка, 1 - продажа
    priceType: Literal[0, 1]  # 0 - fix rate, 1 - floating
    premium: str
    price: str
    minAmount: str
    maxAmount: str
    remark: str
    tradingPreferenceSet: TradingPreferenceSet
    paymentIds: list[str]
    quantity: str
    paymentPeriod: int
    itemType: str


class AdUpdateRequest(AdPostRequest, BaseAdUpdate):
    actionType: Literal["MODIFY", "ACTIVE"] = "MODIFY"


class AdDeleteRequest(BaseModel):
    itemId: str
