from asyncio import sleep

from uvloop import run
from xync_schema import models
from xync_schema.models import Pair, Ex, TradeType
from xync_client.binance.sapi import Sapi
from tortoise_api_model import init_db

from loader import BKEY, BSEC

sql = """
(select fiat.id, amount, target, user_id, cur_id, pt_id, "group", amount - target as need, (amount - target) / rate as need_usd
 from fiat
          inner join ptc p on p.id = fiat.ptc_id and NOT p.blocked
          inner join cur c on c.id = p.cur_id
          inner join pt p2 on p2.name = p.pt_id
 where target is not null
   and (amount - target) / rate < 0
 order by need_usd)
UNION ALL
(select fiat.id, amount, target, user_id, cur_id, pt_id, "group", amount - target as need, (amount - target) / rate as need_usd
 from fiat
          inner join ptc p on p.id = fiat.ptc_id and NOT p.blocked
          inner join cur c on c.id = p.cur_id
          inner join pt p2 on p2.name = p.pt_id
 where target is null
 order by amount / rate)
UNION ALL
(select fiat.id, amount, target, user_id, cur_id, pt_id, "group", amount - target as need, (amount - target) / rate as need_usd
 from fiat
          inner join ptc p on p.id = fiat.ptc_id and NOT p.blocked
          inner join cur c on c.id = p.cur_id
          inner join pt p2 on p2.name = p.pt_id
 where target is not null
   and (amount - target) / rate > 0
 order by need_usd)
"""


async def cycle():
    await init_db(dsn, models)
    Sapi(BKEY, BSEC)
    for ex in await Ex.filter(id__in=[1]).prefetch_related("coins"):
        ex: Ex
        for pmcur in await ex.pmcurs.filter(blocked=False, fiats=True):
            for coin in ex.coins:
                for tt in TradeType:
                    pass
                    # res = await bn_sapi.search_ads(coin.ticker, pmcur.cur.ticker, tt.name, [pmcur.pm.identifier])
                    # if total := res["total"]:
                    #     add = res["data"][0]["adv"]
                    #     fee = add["commissionRate"]
                    #     {"fee": fee, "total": res["total"]}
                    #     pair, _ = Pair.update_or_create({"fee": fee}, coin=coin, cur=pmcur.cur, ex=ex)
                    # else:
                    #     await bn_sapi.post_ad()
                    # elif anti_pair := await Pair.get_or_none(sell=int(not tt), coin=coin, cur=pmcur.cur, ex=ex):
                    #     pair_dict = {'fee': anti_pair.fee, 'total': res['total']}
        while True:
            pass
            # await sleep(1)


asci_map = ["\u2591", "\u2592", "\u2593", "\u2588"]


async def tick(pairs: [Pair]):
    _suc, _err, _lp = 0, 0, len(pairs)
    # fiats = await cns[0].execute_query_dict(sql)
    # fd = {}
    # for fiat in fiats:
    #     fd[fiat["cur_id"]] = fd.get(fiat["cur_id"], []) + [
    #         (fiat["pt_id"], fiat["need"], fiat["group"], fiat["user_id"])
    #     ]
    # for pair in pairs:
    #     pts = [fiat for fiat in fd[pair.cur_id] if fiat[1] is None or fiat[1] * (int(pair.sell) * 2 - 1) > 0]
    #     if not pair.sell:  # add in-group pts only for buy
    #         pt_groups = {pt[2] for pt in pts if pt[2]}
    #         pts += [
    #             (pt.name, None, pt.group)
    #             for pt in await Pm.filter(group__in=pt_groups).prefetch_related("ptcs")
    #             if True not in {ptc.blocked for ptc in pt.ptcs}
    #         ]
    #     if (res := await bn_sapi.search_ads(pair.coin_id, pair.cur_id, pair.sell, list(set(pt[0] for pt in pts)))).get(
    #         "data"
    #     ):
    #         ad_mod = await ad_proc(res, pts)
    #         suc += 1
    #         # just process indicate:
    #         print("[", end="")
    #         for x in range(suc + err):
    #             print(asci_map[ad_mod], end="")
    #         for x in range(lp - suc - err):
    #             print("_", end="")
    #         print("]", end="\r")
    #         cnt = (cnt + 1) % 4
    #     else:
    #         pair.total = 0
    #         await pair.save()
    #         err += 1
    #         print(f"NO Ads for pair {pair.id}: {pair}")
    # print(f"\nSuccess: {suc}, Error: {err}, All: {lp}\n")
    await sleep(1)


if __name__ == "__main__":
    try:
        from loader import BKEY, BSEC, dsn

        run(cycle())
    except KeyboardInterrupt:
        print("Stopped.")
