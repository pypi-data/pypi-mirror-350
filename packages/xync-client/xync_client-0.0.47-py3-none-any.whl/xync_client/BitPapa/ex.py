from asyncio import run
import json
from x_model import init_db

from bs4 import BeautifulSoup
from xync_client.loader import PG_DSN
from xync_client.Abc.Ex import BaseExClient
from xync_client.Abc.Base import MapOfIdsList
from xync_client.Abc.types import PmEx
# from xync_client.Mexc.etype import pm, ad

from xync_schema import types
from xync_schema import models
from xync_schema.models import Ex

class ExClient(BaseExClient):
    async def c2c_data(self):
        doc = await self._get("/buy")
        soup = BeautifulSoup(doc, "html.parser")

    async def curs(self) -> dict[str, types.CurEx]:  # {cur.ticker: cur}
        curs = await self.c2c_data()
        return curs


async def main():
    _ = await init_db(PG_DSN, models, True)
    ex = await Ex.get(name="BitPapa")
    cl = ExClient(ex)
    _ads = await cl.ads(2, 11, True)
    await cl.set_pmcurexs()
    await cl.set_coinexs()
    _cr = await cl.curs()
    _cn = await cl.coins()
    await cl.set_pairs()
    _pms = await cl.pms()
    await cl.close()

if __name__ == "__main__":
    run(main())
