import logging
import re
from asyncio import run, sleep, gather
from enum import IntEnum
from http.client import HTTPException
from typing import Literal

import pyotp
from asyncpg import ConnectionDoesNotExistError
from bybit_p2p import P2P
from bybit_p2p._exceptions import FailedRequestError
from urllib3.exceptions import ReadTimeoutError
from x_model import init_db
from xync_schema import models

from xync_client.Abc.Base import FlatDict
from xync_schema.models import Cur, Actor

from xync_client.Abc.Agent import BaseAgentClient
from xync_client.Abc.types import BaseOrderReq
from xync_client.Bybit.etype.ad import AdPostRequest, AdUpdateRequest, AdDeleteRequest, Ad
from xync_client.Bybit.etype.cred import CredEpyd
from xync_client.Bybit.etype.order import OrderRequest, PreOrderResp, OrderResp, CancelOrderReq
from xync_client.loader import PG_DSN


class NoMakerException(Exception):
    pass


class AdsStatus(IntEnum):
    REST = 0
    WORKING = 1


class AgentClient(BaseAgentClient):  # Bybit client
    host = "api2.bybit.com"
    headers = {"cookie": ";"}  # rewrite token for public methods
    api: P2P
    last_ad_id: list[str] = []
    update_ad_body = {
        "priceType": "1",
        "premium": "118",
        "quantity": "0.01",
        "minAmount": "500",
        "maxAmount": "3500000",
        "paymentPeriod": "30",
        "remark": "",
        "price": "398244.84",
        "paymentIds": ["3162931"],
        "tradingPreferenceSet": {
            "isKyc": "1",
            "hasCompleteRateDay30": "0",
            "completeRateDay30": "",
            "hasOrderFinishNumberDay30": "0",
            "orderFinishNumberDay30": "0",
            "isMobile": "0",
            "isEmail": "0",
            "hasUnPostAd": "0",
            "hasRegisterTime": "0",
            "registerTimeThreshold": "0",
            "hasNationalLimit": "0",
            "nationalLimit": "",
        },
        "actionType": "MODIFY",
        "securityRiskToken": "",
    }

    def __init__(self, actor: Actor, **kwargs):
        super().__init__(actor, **kwargs)
        self.api = P2P(testnet=False, api_key=actor.agent.auth["key"], api_secret=actor.agent.auth["sec"])

    """ Private METHs"""

    def fiat_new(self, payment_type: int, real_name: str, account_number: str) -> FlatDict:
        method1 = self._post(
            "/fiat/otc/user/payment/new_create",
            {"paymentType": payment_type, "realName": real_name, "accountNo": account_number, "securityRiskToken": ""},
        )
        if srt := method1["result"]["securityRiskToken"]:
            self._check_2fa(srt)
            method2 = self._post(
                "/fiat/otc/user/payment/new_create",
                {
                    "paymentType": payment_type,
                    "realName": real_name,
                    "accountNo": account_number,
                    "securityRiskToken": srt,
                },
            )
            return method2
        else:
            print(method1)

    def get_payment_method(self, fiat_id: int = None) -> dict:
        list_methods = self.get_user_pay_methods()
        if fiat_id:
            fiat = [m for m in list_methods if m["id"] == fiat_id][0]
            return fiat
        return list_methods[1]

    def creds(self) -> list[CredEpyd]:
        data = self.api.get_user_payment_types()
        if data["ret_code"] > 0:
            return data
        return [CredEpyd.model_validate(credex) for credex in data["result"]]

    async def cred_epyd2db(self, cred: CredEpyd) -> models.CredEx:
        if cred.paymentType not in (416,):
            if not (
                pmex := await models.Pmex.get_or_none(exid=cred.paymentType, ex=self.ex_client.ex).prefetch_related(
                    "pm__curs"
                )
            ):
                raise HTTPException(f"No Pmex {cred.paymentType} on ex#{self.ex_client.ex.name}", 404)
            if cred_old := await models.Cred.get_or_none(credexs__exid=cred.id, credexs__ex=self.ex).prefetch_related(
                "pmcur"
            ):
                cur_id = cred_old.pmcur.cur_id
            else:  # is new Cred
                cur_id = (
                    pmex.pm.df_cur_id
                    or (pmex.pm.country_id and await pmex.pm.country.cur_id)
                    or (cred.currencyBalance and await models.Cur.get_or_none(ticker=cred.currencyBalance[0]))
                    or (0 < len(pmex.pm.curs) < 20 and pmex.pm.curs[-1].id)
                )
            if not cur_id:
                raise Exception(f"Set default cur for {pmex.name}")
            if not (pmcur := await models.Pmcur.get_or_none(cur_id=cur_id, pm_id=pmex.pm_id)):
                raise HTTPException(f"No Pmcur with cur#{cred.currencyBalance} and pm#{cred.paymentType}", 404)
            dct = {
                "pmcur_id": pmcur.id,
                "name": cred.paymentConfigVo.paymentName,
                "person_id": self.actor.person_id,
                "detail": cred.accountNo,
                "extra": cred.branchName or cred.bankName,
            }  # todo: WTD with multicur pms?
            cred_in = models.Cred.validate(dct, False)
            cred_db, _ = await models.Cred.update_or_create(**cred_in.df_unq())
            credex_in = models.CredEx.validate({"exid": cred.id, "cred_id": cred_db.id, "ex_id": self.ex.id})
            credex_db, _ = await models.CredEx.update_or_create(**credex_in.df_unq())
            return credex_db

    # 25: Список реквизитов моих платежных методов
    async def set_creds(self) -> list[models.CredEx]:
        credexs_epyd: list[CredEpyd] = self.creds()
        credexs: list[models.CredEx] = [await self.cred_epyd2db(f) for f in credexs_epyd]
        return credexs

    async def ott(self):
        t = await self._post("/user/private/ott")
        return t

    # 27
    async def fiat_upd(self, fiat_id: int, detail: str, name: str = None) -> dict:
        fiat = self.get_payment_method(fiat_id)
        fiat["realName"] = name
        fiat["accountNo"] = detail
        result = await self._post("/fiat/otc/user/payment/new_update", fiat)
        srt = result["result"]["securityRiskToken"]
        await self._check_2fa(srt)
        fiat["securityRiskToken"] = srt
        result2 = await self._post("/fiat/otc/user/payment/new_update", fiat)
        return result2

    # 28
    async def fiat_del(self, fiat_id: int) -> dict | str:
        data = {"id": fiat_id, "securityRiskToken": ""}
        method = await self._post("/fiat/otc/user/payment/new_delete", data)
        srt = method["result"]["securityRiskToken"]
        await self._check_2fa(srt)
        data["securityRiskToken"] = srt
        delete = await self._post("/fiat/otc/user/payment/new_delete", data)
        return delete

    async def switch_ads(self, new_status: AdsStatus) -> dict:
        data = {"workStatus": new_status.name}
        res = await self._post("/fiat/otc/maker/work-config/switch", data)
        return res

    async def ads(self, cnx: models.Coinex, crx: models.Curex, is_sell: bool, pmxs: list[models.Pmex]) -> list[Ad]:
        return await self.ex_client.ads(cnx.exid, crx.exid, is_sell, [pmex.exid for pmex in pmxs])

    def online_ads(self) -> str:
        online = self._get("/fiat/otc/maker/work-config/get")
        return online["result"]["workStatus"]

    @staticmethod
    def get_rate(list_ads: list) -> float:
        ads = [ad for ad in list_ads if set(ad["payments"]) - {"5", "51"}]
        return float(ads[0]["price"])

    async def my_fiats(self, cur: Cur = None):
        upm = await self._post("/fiat/otc/user/payment/list")
        return upm["result"]

    def get_user_ads(self, active: bool = True) -> list:
        uo = self._post("/fiat/otc/item/personal/list", {"page": "1", "size": "10", "status": "2" if active else "0"})
        return uo["result"]["items"]

    def get_security_token_create(self):
        data = self._post("/fiat/otc/item/create", self.create_ad_body)
        if data["ret_code"] == 912120019:  # Current user can not to create add as maker
            raise NoMakerException(data)
        security_risk_token = data["result"]["securityRiskToken"]
        return security_risk_token

    def _check_2fa(self, risk_token):
        # 2fa code
        bybit_secret = self.agent.auth["2fa"]
        totp = pyotp.TOTP(bybit_secret)
        totp_code = totp.now()

        res = self._post(
            "/user/public/risk/verify", {"risk_token": risk_token, "component_list": {"google2fa": totp_code}}
        )
        if res["ret_msg"] != "success":
            print("Wrong 2fa, wait 5 secs and retry..")
            sleep(5)
            self._check_2fa(risk_token)
        return res

    def _post_ad(self, risk_token: str):
        self.create_ad_body.update({"securityRiskToken": risk_token})
        data = self._post("/fiat/otc/item/create", self.create_ad_body)
        return data

    # создание объявлений
    def post_create_ad(self, token: str):
        result__check_2fa = self._check_2fa(token)
        assert result__check_2fa["ret_msg"] == "success", "2FA code wrong"

        result_add_ad = self._post_ad(token)
        if result_add_ad["ret_msg"] != "SUCCESS":
            print("Wrong 2fa on Ad creating, wait 9 secs and retry..")
            sleep(9)
            return self._post_create_ad(token)
        self.last_ad_id.append(result_add_ad["result"]["itemId"])

    def ad_new(self, ad: AdPostRequest):
        data = self.api.post_new_ad(**ad.model_dump())
        return data["result"]["itemId"] if data["ret_code"] == 0 else data

    def ad_upd(self, upd: AdUpdateRequest):
        params = upd.model_dump()
        data = self.api.update_ad(**params)
        return data["result"] if data["ret_code"] == 0 else data

    def get_security_token_update(self) -> str:
        self.update_ad_body["id"] = self.last_ad_id
        data = self._post("/fiat/otc/item/update", self.update_ad_body)
        security_risk_token = data["result"]["securityRiskToken"]
        return security_risk_token

    def post_update_ad(self, token):
        result__check_2fa = self._check_2fa(token)
        assert result__check_2fa["ret_msg"] == "success", "2FA code wrong"

        result_update_ad = self.update_ad(token)
        if result_update_ad["ret_msg"] != "SUCCESS":
            print("Wrong 2fa on Ad updating, wait 10 secs and retry..")
            sleep(10)
            return self._post_update_ad(token)
        # assert result_update_ad['ret_msg'] == 'SUCCESS', "Ad isn't updated"

    def update_ad(self, risk_token: str):
        self.update_ad_body.update({"securityRiskToken": risk_token})
        data = self._post("/fiat/otc/item/update", self.update_ad_body)
        return data

    def ad_del(self, ad_id: AdDeleteRequest):
        data = self.api.remove_ad(**ad_id.model_dump())
        return data

    async def order_request(self, br: BaseOrderReq) -> OrderResp:
        res0 = await self._post("/fiat/otc/item/simple", data={"item_id": str(br.ad_id)})
        if res0["ret_code"] == 0:
            res0 = res0["result"]
        res0 = PreOrderResp.model_validate(res0)
        req = OrderRequest(
            itemId=br.ad_id,
            tokenId=br.coin_exid,
            currencyId=br.cur_exid,
            side=str(OrderRequest.Side(int(br.is_sell))),
            amount=str(br.fiat_amount or br.asset_amount * float(res0.price)),
            curPrice=res0.curPrice,
            quantity=str(br.asset_amount or round(br.fiat_amount / float(res0.price), br.coin_scale)),
            flag="amount" if br.amount_is_fiat else "quantity",
        )
        # вот непосредственно сам запрос на ордер
        res = await self._post("/fiat/otc/order/create", data=req.model_dump())
        if res["ret_code"] == 0:
            return OrderResp.model_validate(res["result"])
        elif res["ret_code"] == 912120030 or res["ret_msg"] == "The price has changed, please try again later.":
            return await self.order_request(br)

    async def cancel_order(self, order_id: str) -> bool:
        cr = CancelOrderReq(orderId=order_id)
        res = await self._post("/fiat/otc/order/cancel", cr.model_dump())
        return res["ret_code"] == 0

    def get_order_info(self, order_id: str) -> dict:
        data = self._post("/fiat/otc/order/info", json={"orderId": order_id})
        return data["result"]

    def get_chat_msg(self, order_id):
        data = self._post("/fiat/otc/order/message/listpage", json={"orderId": order_id, "size": 100})
        msgs = [
            {"text": msg["message"], "type": msg["contentType"], "role": msg["roleType"], "user_id": msg["userId"]}
            for msg in data["result"]["result"]
            if msg["roleType"] not in ("sys", "alarm")
        ]
        return msgs

    def block_user(self, user_id: str):
        return self._post("/fiat/p2p/user/add_block_user", {"blockedUserId": user_id})

    def unblock_user(self, user_id: str):
        return self._post("/fiat/p2p/user/delete_block_user", {"blockedUserId": user_id})

    def user_review_post(self, order_id: str):
        return self._post(
            "/fiat/otc/order/appraise/modify",
            {
                "orderId": order_id,
                "anonymous": "0",
                "appraiseType": "1",  # тип оценки 1 - хорошо, 0 - плохо. При 0 - обязательно указывать appraiseContent
                "appraiseContent": "",
                "operateType": "ADD",  # при повторном отправлять не 'ADD' -> а 'EDIT'
            },
        )

    def get_orders_active(self, begin_time: int, end_time: int, status: int, side: int, token_id: str):
        return self._post(
            "/fiat/otc/order/pending/simplifyList",
            {
                "status": status,
                "tokenId": token_id,
                "beginTime": begin_time,
                "endTime": end_time,
                "side": side,  # 1 - продажа, 0 - покупка
                "page": 1,
                "size": 10,
            },
        )

    def get_orders_done(self, begin_time: int, end_time: int, status: int, side: int, token_id: str):
        return self._post(
            "/fiat/otc/order/simplifyList",
            {
                "status": status,  # 50 - завершено
                "tokenId": token_id,
                "beginTime": begin_time,
                "endTime": end_time,
                "side": side,  # 1 - продажа, 0 - покупка
                "page": 1,
                "size": 10,
            },
        )

    async def mad_upd(self, mad: Ad, attrs: dict, cxids: list[str]):
        if not [setattr(mad, k, v) for k, v in attrs.items() if getattr(mad, k) != v]:
            print(end="v" if mad.side else "^", flush=True)
            return await sleep(5)
        req = AdUpdateRequest.model_validate({**mad.model_dump(), "paymentIds": cxids})
        try:
            return self.ad_upd(req)
        except FailedRequestError as e:
            if ExcCode(e.status_code) == ExcCode.FixPriceLimit:
                if limits := re.search(
                    r"The fixed price set is lower than ([0-9]+\.?[0-9]{0,2}) or higher than ([0-9]+\.?[0-9]{0,2})",
                    e.message,
                ):
                    return await self.mad_upd(mad, {"price": limits.group(1 if mad.side else 2)}, cxids)
            elif ExcCode(e.status_code) == ExcCode.RareLimit:
                await sleep(180)
            else:
                raise e
        except (ReadTimeoutError, ConnectionDoesNotExistError):
            logging.warning("Connection failed. Restarting..")
        print("-" if mad.side else "+", end=req.price, flush=True)
        await sleep(60)

    def overprice_filter(self, ads: list[Ad], ceil: float, k: Literal[-1, 1]):
        # вырезаем ads с ценами выше потолка
        if ads and (ceil - float(ads[0].price)) * k > 0:
            if int(ads[0].userId) != self.actor.exid:
                ads.pop(0)
                self.overprice_filter(ads, ceil, k)

    def get_cad(self, ads: list[Ad], ceil: float, k: Literal[-1, 1], place: int, cur_plc: int) -> Ad:
        # чью цену будем обгонять, предыдущей или слещующей объявы?
        cad: Ad = ads[place] if cur_plc > place else ads[cur_plc]
        # а цена обгоняемой объявы не выше нашего потолка?
        if (float(cad.price) - ceil) * k <= 0:
            # тогда берем следующую
            ads.pop(place)
            cad = self.get_cad(ads, ceil, k, place, cur_plc)
        # todo: добавить фильтр по лимитам min-max
        return cad

    async def battle(
        self,
        coinex: models.Coinex,
        curex: models.Curex,
        is_sell: bool,
        pms: list[str],
        ceil: float,
        volume: float = None,
        place: int = 0,
    ):
        k = (-1) ** int(is_sell)  # on_buy=1, on_sell=-1

        creds: dict[models.Pmex, models.CredEx] = await get_creds(pms, self.ex)
        if not volume:
            if is_sell:  # гонка в стакане продажи - мы покупаем монету за ФИАТ
                # todo: we using the only one fiat exactly from THE FIRST cred
                fiat = await models.Fiat.get(cred_id=list(creds.values())[0].cred_id)
                volume = fiat.amount / ceil
            else:  # гонка в стакане покупки - мы продаем МОНЕТУ за фиат
                asset = await models.Asset.get(addr__actor=self.actor, addr__coin_id=coinex.coin_id)
                volume = asset.free - (asset.freeze or 0) - (asset.lock or 0)

        volume = str(round(volume, coinex.coin.scale))

        credex_ids = [str(p.exid) for p in creds.values()]

        while self.actor.person.user.status > 0:
            ads: list[Ad] = await self.ads(coinex, curex, is_sell, list(creds.keys()))
            self.overprice_filter(ads, ceil, k)
            if not ads:
                print(coinex.exid, curex.exid, is_sell, "no ads!")
                await sleep(15)
                continue
            cur_plc = [i for i, ad in enumerate(ads) if int(ad.userId) == self.actor.exid][0]
            mad: Ad = ads.pop(cur_plc)
            if not ads:
                await sleep(60)
                continue
            cad = self.get_cad(ads, ceil, k, place, cur_plc)
            new_price = f"%.{curex.cur.scale}f" % round(float(cad.price) - k * step(mad, cad), curex.cur.scale)
            if mad.price == new_price:  # Если нужная цена и так уже стоит
                print(end="v" if is_sell else "^", flush=True)
                await sleep(3)
                continue
            if cad.priceType:  # Если цена конкурента плавающая, то повышаем себе не цену, а %
                new_premium = str(round(float(cad.premium) - k * step(mad, cad), 2))
                if mad.premium == new_premium:  # Если нужный % и так уже стоит
                    print(end="v" if is_sell else "^", flush=True)
                    await sleep(3)
                    continue
                mad.premium = new_premium
            mad.priceType = cad.priceType
            mad.quantity = volume
            mad.maxAmount = str(2_000_000)
            req = AdUpdateRequest.model_validate({**mad.model_dump(), "price": new_price, "paymentIds": credex_ids})
            try:
                _res = self.ad_upd(req)
                print("-" if is_sell else "+", end=req.price, flush=True)
            except FailedRequestError as e:
                if ExcCode(e.status_code) == ExcCode.FixPriceLimit:
                    if limits := re.search(
                        r"The fixed price set is lower than ([0-9]+\.?[0-9]{0,2}) or higher than ([0-9]+\.?[0-9]{0,2})",
                        e.message,
                    ):
                        req.price = limits.group(1 if is_sell else 2)
                        if req.price != mad.price:
                            _res = self.ad_upd(req)
                    else:
                        raise e
                elif ExcCode(e.status_code) == ExcCode.InsufficientAmount:
                    asset = await models.Asset.get(addr__actor=self.actor, addr__coin_id=coinex.coin_id)
                    req.quantity = round(asset.free - (asset.freeze or 0) - (asset.lock or 0), coinex.coin.scale)
                    _res = self.ad_upd(req)
                elif ExcCode(e.status_code) == ExcCode.RareLimit:
                    await sleep(195)
                elif ExcCode(e.status_code) == ExcCode.Timestamp:
                    await sleep(2)
                else:
                    raise e
            except (ReadTimeoutError, ConnectionDoesNotExistError):
                logging.warning("Connection failed. Restarting..")
            await sleep(42)


def step(mad, cad) -> float:
    return (
        0.01
        if cad.recentExecuteRate > mad.recentExecuteRate
        or (cad.recentExecuteRate == mad.recentExecuteRate and cad.recentOrderNum > mad.recentOrderNum)
        else 0
    )


def listen(data: dict):
    print(data)


async def get_creds(norms: list[str], ex: models.Ex) -> dict[models.Pmex, models.CredEx]:
    return {
        await models.Pmex.get(ex=ex, pm__norm=n): await models.CredEx.get(ex=ex, cred__pmcur__pm__norm=n) for n in norms
    }


class ExcCode(IntEnum):
    FixPriceLimit = 912120022
    RareLimit = 912120050
    InsufficientAmount = 912120024
    Timestamp = 10002
    IP = 10010


async def main():
    _ = await init_db(PG_DSN, models, True)
    logging.basicConfig(level=logging.INFO)
    actor = (
        await models.Actor.filter(ex_id=9, agent__isnull=False).prefetch_related("ex", "agent", "person__user").first()
    )
    cl: AgentClient = actor.client()
    # await cl.ex_client.set_pmcurexs(cookies=actor.agent.auth["cookies"])  # 607 -> 629
    usdt = await models.Coinex.get(coin__ticker="USDT", ex=cl.ex).prefetch_related("coin")
    btc = await models.Coinex.get(coin__ticker="BTC", ex=cl.ex).prefetch_related("coin")
    eth = await models.Coinex.get(coin__ticker="ETH", ex=cl.ex).prefetch_related("coin")
    usdc = await models.Coinex.get(coin__ticker="USDC", ex=cl.ex).prefetch_related("coin")
    rub = await models.Curex.get(cur__ticker="RUB", ex=cl.ex).prefetch_related("cur")
    # await models.Direction.get(
    #     pairex__ex=cl.ex, pairex__pair__coin__ticker="USDT", pairex__pair__cur__ticker="RUB", sell=True
    # )
    # await cl.set_creds()
    await gather(
        cl.battle(usdt, rub, False, ["volet"], 83.88),  # гонка в стакане покупки - мы продаем
        cl.battle(usdt, rub, True, ["volet"], 82),  # гонка в стакане продажи - мы покупаем
        cl.battle(eth, rub, False, ["volet"], 160_000),
        cl.battle(eth, rub, True, ["volet"], 144_000),
        cl.battle(btc, rub, False, ["volet"], 8_700_000),
        cl.battle(btc, rub, True, ["volet"], 7_600_000),
        cl.battle(usdc, rub, True, ["volet"], 82),
        cl.battle(usdc, rub, False, ["volet"], 86),
    )

    bor = BaseOrderReq(
        ad_id="1861440060199632896",
        # asset_amount=40,
        fiat_amount=3000,
        amount_is_fiat=True,
        is_sell=False,
        cur_exid=rub.exid,
        coin_exid=usdt.exid,
        coin_scale=usdt.coin.scale,
    )
    res: OrderResp = await cl.order_request(bor)
    await cl.cancel_order(res.orderId)
    await cl.close()


if __name__ == "__main__":
    run(main())
