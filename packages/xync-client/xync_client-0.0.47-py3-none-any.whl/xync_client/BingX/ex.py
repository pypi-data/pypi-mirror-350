from asyncio import run

from x_model import init_db
from xync_schema import models
from xync_schema.models import Ex
from xync_schema import types

from xync_client.Abc.Ex import BaseExClient
from xync_client.BingX.base import BaseBingXClient
from xync_client.loader import PG_DSN
from xync_client.Abc.Base import MapOfIdsList
from xync_client.BingX.etype import ad, pm
from xync_client.Abc.types import PmEx
from xync_client.pm_unifier import PmUnifier


class ExClient(BaseExClient, BaseBingXClient):
    class BingUnifier(PmUnifier):
        pm_map = {
            "СБП": "SBP",
            "Tinkoff Bank": "T-Bank",
            "Transfer with Specific Bank": "Transfers with specific bank",
            "Al-Rafidain Qi Services": "Al-Rafidain QiServices",
        }

    unifier_class = BingUnifier
    headers: dict[str, str] = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "app_version": "9.0.5",
        "device_id": "ccfb6d50-b63b-11ef-b31f-ef1f76f67c4e",
        "lang": "en",
        "platformid": "30",
        "device_brand": "Linux_Chrome_131.0.0.0",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    async def _pms(self, cur) -> list[pm.PmE]:
        pms = await self._get("/api/c2c/v1/advert/payment/list", params={"fiat": cur})
        return [pm.PmE(**_pm) for _pm in pms["data"]["paymentMethodList"]]

    # 19: Список всех платежных методов на бирже
    async def pms(self, cur: str = None) -> dict[int | str, PmEx]:
        all_pms = {}
        for cur in (await self.curs()).values():
            pms = await self._pms(cur.ticker)
            for p in pms:
                all_pms[p.id] = PmEx(exid=p.id, name=p.name, logo=p.icon)
        return all_pms

    # 20: Список поддерживаемых валют на BingX
    async def curs(self) -> list[types.CurEx]:  # {cur.exid: cur.ticker}
        params = {
            "type": "1",
            "asset": "USDT",
            "coinType": "2",
        }
        curs = await self._get("/api/c2c/v1/common/supportCoins", params=params)
        return {cur["name"]: types.CurEx(exid=cur["name"], ticker=cur["name"]) for cur in curs["data"]["coins"]}

    # 21: cur_pms_map на BingX
    async def cur_pms_map(self) -> MapOfIdsList:
        return {cur.exid: [pm.id for pm in await self._pms(cur.ticker)] for cur in (await self.curs()).values()}

    # 22: Монеты на BingX
    async def coins(self) -> list[types.CoinEx]:
        return {"USDT": types.CoinEx(exid="USDT", ticker="USDT", scale=4)}

    # 23: Список пар валюта/монет
    async def pairs(self) -> MapOfIdsList:
        coins = (await self.coins()).keys()
        curs = (await self.curs()).keys()
        p = {cur: {c for c in coins} for cur in curs}
        return p, p

    # 24: ads
    async def ads(
        self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None, amount: int = None
    ) -> list[ad.Ad]:
        params = {
            "type": 1,
            "fiat": cur_exid,
            "asset": coin_exid,
            "amount": amount or "",
            "hidePaymentInfo": "",
            "payMethodId": pm_exids or "",
            "isUserMatchCondition": "true" if is_sell else "false",
        }

        ads = await self._get("/api/c2c/v1/advert/list", params=params)
        return [ad.Ad(id=_ad["orderNo"], **_ad) for _ad in ads["data"]["dataList"]]


async def main():
    _ = await init_db(PG_DSN, models, True)
    bg = await Ex.get(name="BingX")
    cl = ExClient(bg)
    _ads = await cl.ads("USDT", "RUB", False)
    await cl.set_pairs()
    await cl.set_coinexs()
    await cl.set_pmcurexs()
    # _curs = await cl.curs()
    # _coins = await cl.coins()
    # _pairs = await cl.pairs()
    # _pms = await cl.pms("EUR")
    # _pms_map = await cl.cur_pms_map()
    await cl.close()


if __name__ == "__main__":
    run(main())
