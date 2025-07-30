from asyncio import run

from x_model import init_db
from xync_schema import models
from xync_schema import types

from xync_client.Abc.Base import MapOfIdsList
from xync_client.Abc.Ex import BaseExClient
from xync_client.loader import PG_DSN
from xync_client.Okx.etype import ad, pm
from xync_client.Abc.types import PmEx
from xync_client.pm_unifier import PmUnifier


class ExClient(BaseExClient):
    class OkxUnifier(PmUnifier):
        pm_map = {
            "SBP Fast Bank Transfer": "SBP",
            "ADCB": "Abu Dhabi Commercial Bank ADCB",
            "Al-Rafdin QiServices": "Al-Rafidain QiServices",
            "Viettel Pay": "ViettelPay",
            "Zain Cash - Business": "ZainCash - Business"
        }

    unifier_class = OkxUnifier

    async def _pms(self, cur) -> list[pm.PmE]:
        params = {
            "quoteCurrency": cur,
            "needField": "false",
        }
        pms = await self._get("/v3/c2c/configs/receipt/templates", params=params)
        return [pm.PmE(**_pm) for _pm in pms["data"] if _pm["paymentMethod"]]

    # 19: Список поддерживаемых валют тейкера
    async def curs(self) -> dict[int, types.CurEx]:  # {cur.exid: cur.ticker}
        curs = await self._get("/v3/users/common/list/currencies")
        return {
            cur["displayName"]: types.CurEx(exid=cur["displayName"], ticker=cur["displayName"], scale=cur["precision"])
            for cur in curs["data"]
        }

    # 20: Список платежных методов
    async def pms(self, cur: models.Cur = None) -> dict[int | str, PmEx]:  # {pm.exid: pm}
        all_pms = {}
        for cur_obj in (await self.curs()).values():
            pms = await self._pms(cur_obj.ticker)
            for p in pms:
                all_pms[p.paymentMethod] = PmEx(exid=p.paymentMethod, name=p.paymentMethod)
        return all_pms

    # 21: Список платежных методов по каждой валюте
    async def cur_pms_map(self) -> MapOfIdsList:  # {cur.exid: [pm.exid]}
        return {
            cur.exid: [pm.paymentMethod for pm in await self._pms(cur.ticker)] for cur in (await self.curs()).values()
        }

    # 22: Список торгуемых монет (с ограничениям по валютам, если есть)
    async def coins(self) -> dict[int, types.CoinEx]:  # {coin.exid: coin.ticker}
        for cur in (await self.curs()).keys():
            coins = await self._get("/v3/c2c/currency/pairs", {"type": 2, "quote": cur})
            return {
                coin["baseCurrency"]: types.CoinEx(
                    exid=coin["baseCurrency"], ticker=coin["baseCurrency"], scale=coin["baseScale"]
                )
                for coin in coins["data"]
            }

    # 23: Список пар валюта/монет
    async def pairs(self) -> MapOfIdsList:
        coins = (await self.coins()).keys()
        curs = (await self.curs()).keys()
        p = {cur: {c for c in coins} for cur in curs}
        return p, p

    # 24: Список объяв по (buy/sell, cur, coin, pm)
    async def ads(
        self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None, amount: int = None
    ) -> list[ad.Ads]:  # {ad.id: ad}
        params = {
            "side": "sell",
            "paymentMethod": "all",
            "userType": "all",
            "hideOverseasVerificationAds": "true" if is_sell else "false",
            "sortType": "price_asc",
            "limit": "100",
            "cryptoCurrency": f"{coin_exid}",
            "fiatCurrency": f"{cur_exid}",
            "currentPage": "1",
            "numberPerPage": "5",
        }
        ads = await self._get("/v3/c2c/tradingOrders/getMarketplaceAdsPrelogin", params=params)
        return [ad.Ads(**a) for a in ads["data"]["sell"]]

    # 42: Чужая объява по id
    async def ad(self, ad_id: int) -> ad.Ad:
        params = {
            "publicUserId": "f81434eb2a",
            "t": f"{ad_id}",
        }
        ad = await self._get("/v3/c2c/merchant/liteProfile", params=params)
        return ad.Ad(**ad)


async def main():
    _ = await init_db(PG_DSN, models, True)
    bg = await models.Ex.get(name="Okx")
    cl = ExClient(bg)
    await cl.ads("USDT", "THB", False)
    # curs = await cl.curs()
    # coins = await cl.coins()
    await cl.pms()
    await cl.cur_pms_map()
    await cl.pairs()
    await cl.set_coinexs()
    await cl.set_pmcurexs()
    await cl.close()


if __name__ == "__main__":
    run(main())
