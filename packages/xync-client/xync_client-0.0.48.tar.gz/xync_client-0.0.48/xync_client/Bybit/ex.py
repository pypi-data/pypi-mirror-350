import json
from asyncio import run
from x_model import init_db
from xync_schema import types
from xync_schema import models
from xync_schema.models import Ex

from xync_client.Abc.Base import MapOfIdsList
from xync_client.Abc.Ex import BaseExClient
from xync_client.pm_unifier import PmUnifier
from xync_client.loader import PG_DSN
from xync_client.Bybit.etype import ad
from xync_client.Abc.types import PmEx


class ExClient(BaseExClient):  # Bybit client
    class BybitUnifier(PmUnifier):
        pm_map = {
            "Local Bank (R-Green)": "Sberbank",
            "Local Bank (S-Green)": "Sberbank",
            "Local Card (Red)": "Alfa-Bank",
            "Local Card(Red)": "Alfa-Bank",
            "Local Card (Yellow)": "T-Bank",
            "Local Card(Yellow)": "T-Bank",
            "Local Card M-redTS": "MTS-bank",
            "Local Card-Green": "Sberbank",
            "Local Bank(S-Green)": "Sberbank",
            "Local Card(Green)": "Sberbank",
            "Local Bank(R-Green)": "Sberbank",
            "Local Card-Yellow": "T-Bank",
            "Tinkoff": "T-Bank",
            "Banque de développement local (BDL)": "Banque de développement local (BDL)",
            "Al-Rajhi Bank": "Al Rajhi Bank",
            "BDO": "Banco De Oro (BDO)",
        }

    host = "api2.bybit.com"
    headers = {"cookie": ";"}  # rewrite token for public methods
    unifier_class = BybitUnifier

    async def _get_config(self):
        resp = await self._get("/fiat/p2p/config/initial")
        return resp["result"]  # todo: tokens, pairs, ...

    # 19: Список поддерживаемых валют тейкера
    async def curs(self) -> dict[types.CurEx]:
        config = await self._get_config()
        return {
            c["currencyId"]: types.CurEx(exid=c["currencyId"], ticker=c["currencyId"], scale=c["scale"])
            for c in config["currencies"]
        }

    # 20: Список платежных методов
    async def pms(self, cur: models.Cur = None) -> dict[int | str, PmEx]:
        pms = await self._post("/fiat/otc/configuration/queryAllPaymentList/")
        pms = pms["result"]["paymentConfigVo"]
        return {pm["paymentType"]: PmEx(exid=pm["paymentType"], name=pm["paymentName"]) for pm in pms}

    # 21: Список платежных методов по каждой валюте
    async def cur_pms_map(self) -> MapOfIdsList:
        pms = await self._post("/fiat/otc/configuration/queryAllPaymentList/")
        return json.loads(pms["result"]["currencyPaymentIdMap"])

    # 22: Список торгуемых монет (с ограничениям по валютам, если есть)
    async def coins(self) -> dict[types.CoinEx]:
        config = await self._get_config()
        coinexs = {}
        for c in config["symbols"]:
            coinexs[c["tokenId"]] = types.CoinEx(
                exid=c["tokenId"], ticker=c["tokenId"], minimum=c["currencyMinQuote"], scale=c["token"]["scale"]
            )
        return coinexs

    # 23: Список пар валюта/монет
    async def pairs(self) -> tuple[MapOfIdsList, MapOfIdsList]:
        config = await self._get_config()
        cc: dict[str, set[str]] = {}
        for c in config["symbols"]:
            cc[c["currencyId"]] = cc.get(c["currencyId"], set()) | {c["tokenId"]}
        return cc, cc

    # 24: Список объяв по (buy/sell, cur, coin, pm)
    async def ads(
        self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None, amount: int = None
    ) -> list[ad.Ad]:
        data = {
            "userId": "",
            "tokenId": coin_exid,
            "currencyId": cur_exid,
            "payment": pm_exids or [],
            "side": "0" if is_sell else "1",
            "size": "10",
            "page": "1",
            "amount": str(amount) if amount else "",
            "authMaker": False,
            "canTrade": False,
        }
        ads = await self._post("/fiat/otc/item/online/", data)
        return [ad.Ad(**_ad) for _ad in ads["result"]["items"]]


async def main():
    _ = await init_db(PG_DSN, models, True)
    ex = await Ex.get(name="Bybit")
    cl = ExClient(ex)
    # _ads = await cl.ads("USDT", "GEL", False)
    # await cl.set_pmcurexs()
    await cl.set_coinexs()
    # _cr = await cl.curs()
    # _cn = await cl.coins()
    # await cl.set_pairs()
    # _pms = await cl.pms()
    await cl.close()


if __name__ == "__main__":
    run(main())
