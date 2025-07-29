from asyncio import sleep, gather

from aiohttp.http_exceptions import HttpProcessingError
from uvloop import run
from xync_schema import models
from xync_client.Binance.earn_api import Ebac
from xync_client.Bybit.web_earn import BybitEarn, ProductType
from xync_client.Htx.web import Earn as HtxEarn, Private as HtxPrivate
from xync_client.KuCoin.web import Earn as Kucoin
from xync_client.Okx.web import Public as Okx
from x_client import repeat_on_fault
from httpx import ReadTimeout
from okx.Earning import EarningAPI

# from pybit.unified_trading import HTTP
from tortoise import Tortoise
from xync_schema.models import Dep, DepType, Coin
from x_model import init_db

from loader import BKEY, BSEC, OKXKEY, OKXSEC, OKXPSF, dsn, BYT  # , BYKEY, BYSEC


async def kucoin() -> tuple[int, int]:
    i, pids = 0, []
    ku = Kucoin()
    kes = await ku.get_earn_products()
    # cats = {'ACTIVITY', 'DEMAND', 'PROTECTIVE_EARN', 'DUAL', 'ETH2', 'STAKING', 'POLKA_FUND'}
    # types = {'DEMAND', 'MULTI_TIME', 'SAVING', 'TIME', 'DUAL', 'ETH2', 'POLKA_FUND'}
    for ke in kes:
        for p in ke["products"]:
            pid = p["product_id"]
            pids.append(pid)
            unq = {"pid": pid, "coin": await Coin.get_or_create_by_name(p["currency"]), "ex_id": 5}
            apr = float(p["apr"]) * 0.01 if p["apr"] != "-" else 0
            if (
                p["category"] not in ("PROTECTIVE_EARN", "DUAL")
                and apr > 0
                and (p["status"] == "ONGOING")
                or (p["status"] != "ONGOING" and await Dep.exists(**unq, is_active=True))
            ):
                typ = {"ACTIVITY": DepType.earn, "ETH2": DepType.beth, "STAKING": DepType.stake}.get(
                    p["category"], DepType.earn
                )
                dtl = await ku.get_product_detail(p["product_id"])
                mn = dtl.get("user_lower_limit", 0)
                mx = (
                    p["return_rates"]["STEP"][1]["amount"] - mn
                    if p["return_type"] == "STEP"
                    else dtl.get("user_upper_limit", 0)
                )
                dfd = {
                    "apr": apr,
                    "is_active": p["status"] == "ONGOING",
                    "early_redeem": False if p["category"] == "ACTIVITY" or int(p["duration"]) > 0 else True,
                    "min_limit": mn,
                    "max_limit": mx,
                    "type": typ,
                    "duration": p["duration"],
                    "fee": dtl.get("pol_fee_percent", 0),
                }
                d, c = await Dep.update_or_create(dfd, **unq)
                if c:
                    i += 1

    kos = await ku.get_onchain_products()
    for ko in kos:
        pid = f"KUS_{ko['currency']}"
        pids.append(pid)
        unq = {"pid": pid, "coin": await Coin.get_or_create_by_name(ko["currency"]), "ex_id": 5, "type": DepType.stake}
        if ko["state"] == "ENABLE" or (ko["state"] != "ENABLE" and await Dep.exists(**unq, is_active=True)):
            dfd = {
                "apr": ko["yearInterestRate"],
                "is_active": ko["state"] == "ENABLE",
                "min_limit": ko["lendMinAmount"],
                "lendMaxAmount": ko["lendMaxAmount"],
            }  # , 'duration': 0
            d, c = await Dep.update_or_create(dfd, **unq)
            if c:
                i += 1
    await ku.close()
    dlt = await Dep.filter(ex_id=5, pid__not_in=pids).delete()
    return i, dlt


async def huobi() -> tuple[int, int]:
    i, pids = 0, []
    # BETH
    client = HtxPrivate()
    # try:
    hbr = await client.get_beth_rate()
    pids.append("HBETH")
    d, c = await Dep.update_or_create(
        {"apr": hbr},
        pid="HBETH",
        type=DepType.beth,
        apr_is_fixed=False,
        min_limit=0.0001,
        coin=await Coin.get_or_create_by_name("BETH"),
        ex_id=2,
    )
    if c:
        i += 1
    # except HttpProcessingError:
    #     print('HTX-BETH 504')
    await client.close()
    # Stakes
    huobi_earn = HtxEarn()
    hbstks = await huobi_earn.get_staking_products() or []
    for hbstk in hbstks:
        c = hbstk["currency"]
        pid = hbstk["id"]
        pids.append(pid)
        unq = {
            "pid": pid,
            "min_limit": 0,
            "coin": await Coin.get_or_create_by_name(c),
            "ex_id": 2,
            "type": DepType.stake,
        }
        if hbstk["status"] == 1 or (hbstk["status"] != 1 and await Dep.exists(**unq, is_active=True)):
            d, c = await Dep.update_or_create(
                {"apr": hbstk["annualizedRate"], "is_active": hbstk["status"] == 1, "duration": hbstk["lockupPeriod"]},
                **unq,
            )
            if c:
                i += 1
    # New
    hbns = await huobi_earn.get_new_products()
    for hbn in hbns:
        c = hbn["currency"]
        pid = hbn["projectId"]
        pids.append(pid)
        unq = {"pid": pid, "coin": await Coin.get_or_create_by_name(c), "ex_id": 2, "type": DepType.earn}
        if hbn["projectStatus"] == 1 or (hbn["projectStatus"] != 1 and await Dep.exists(**unq, is_active=True)):
            d, c = await Dep.update_or_create(
                {
                    "apr": hbn["viewYearRate"],
                    "is_active": hbn["projectStatus"] == 1,
                    "min_limit": hbn["startAmount"],
                    "max_limit": hbn["totalAmount"] - hbn["finishAmount"],
                    "duration": hbn["term"],
                },
                **unq,
            )
            if c:
                i += 1
    # Fixed
    hbls = await huobi_earn.get_lock_products()
    for hbl in hbls:
        c = hbl["currency"]
        pid = hbl["projectId"]
        pids.append(pid)
        unq = {"pid": pid, "coin": await Coin.get_or_create_by_name(c), "ex_id": 2, "type": DepType.earn}
        if hbl["projectStatus"] == 1 or (hbl["projectStatus"] != 1 and await Dep.exists(**unq, is_active=True)):
            d, c = await Dep.update_or_create(
                {
                    "apr": hbl["viewYearRate"],
                    "apr_is_fixed": True,
                    "is_active": hbl["projectStatus"] == 1,
                    "max_limit": hbl["totalAmount"] - hbl["finishAmount"],
                    "min_limit": hbl["startAmount"],
                    "duration": hbl["term"],
                },
                **unq,
            )
            if c:
                i += 1
    # Flexible
    hbfs = await huobi_earn.get_flex_products()
    for hbf in hbfs:
        c = hbf["currency"]
        pid = hbf["projectId"]
        pids.append(pid)
        unq = {"pid": pid, "coin": await Coin.get_or_create_by_name(c), "ex_id": 2, "type": DepType.earn}
        if hbf["projectStatus"] == 1 or (hbf["projectStatus"] != 1 and await Dep.exists(**unq, is_active=True)):
            d, c = await Dep.update_or_create(
                {
                    "apr": hbf["viewYearRate"],
                    "is_active": hbf["projectStatus"] == 1,
                    "max_limit": hbf["totalAmount"] - hbf["finishAmount"],
                    "min_limit": hbf["startAmount"],
                    "duration": hbf["term"],
                },
                **unq,
            )
            if c:
                i += 1
    # Large
    hbms = await huobi_earn.get_large_products()
    for hbm in hbms:
        c = hbm["currency"]
        pid = hbm["projectId"]
        pids.append(pid)
        unq = {"pid": pid, "coin": await Coin.get_or_create_by_name(c), "ex_id": 2, "type": DepType.earn}
        if hbm["projectStatus"] == 1 or (hbm["projectStatus"] != 1 and await Dep.exists(**unq, is_active=True)):
            d, c = await Dep.update_or_create(
                {
                    "apr": hbm["viewYearRate"],
                    "apr_is_fixed": True,
                    "is_active": hbm["projectStatus"] == 1,
                    "max_limit": hbm["totalAmount"] - hbm["finishAmount"],
                    "min_limit": hbm["startAmount"],
                    "duration": hbm["term"],
                },
                **unq,
            )
            if c:
                i += 1
    await huobi_earn.close()
    dlt = await Dep.filter(ex_id=2, pid__not_in=pids).delete()
    return i, dlt


@repeat_on_fault()
async def Binance() -> tuple[int, int]:
    i, pids = 0, []
    ebac = await Ebac.create(BKEY, BSEC)
    lst = await ebac.get_staking_product_list(product="L_DEFI", size=100)
    fst = await ebac.get_staking_product_list(product="F_DEFI", size=100)
    fps = await ebac.flex_products()
    lps = await ebac.lock_products()
    await ebac.flex_position()
    await ebac.lock_position()
    # fpps = await ebac.get_fixed_activity_project_list()
    # lpls = await ebac.get_lending_product_list() # todo: fix deprecated

    # binance flexible simple-earns
    for fp in fps:
        pid = fp["productId"]
        pids.append(pid)
        unq = {"pid": pid, "ex_id": 1, "type": DepType.earn}
        if not fp["isSoldOut"] or (fp["isSoldOut"] and await Dep.exists(**unq, is_active=True)):
            upd = {
                "coin": await Coin.get_or_create_by_name(fp["asset"]),
                "apr": fp["latestAnnualPercentageRate"],
                "apr_is_fixed": False,
                "min_limit": fp["minPurchaseAmount"],
                "is_active": not fp["isSoldOut"],
            }
            d, c = await Dep.update_or_create(upd, **unq)
            if c:
                i += 1

    # binance locked simple-earns
    for lp in lps:
        d = lp["detail"]
        if ((er := d.get("extraRewardAsset")) and d.get("rewardAsset")) or (
            (era := d.get("extraRewardAPR")) and d.get("apr")
        ):
            raise Exception
        pid = lp["projectId"]
        pids.append(pid)
        unq = {"pid": pid, "ex_id": 1, "type": DepType.earn}
        if not d["isSoldOut"] or (d["isSoldOut"] and await Dep.exists(**unq, is_active=True)):
            upd = {
                "coin": await Coin.get_or_create_by_name(d["asset"]),
                "reward_coin": er and await Coin.get_or_create_by_name(er),
                "apr": d.get("apr", era),
                "apr_is_fixed": True,
                "is_active": not d["isSoldOut"],
                "duration": d["duration"],
                "min_limit": lp["quota"]["minimum"],
                "max_limit": lp["quota"]["totalPersonalQuota"],
            }
            d, c = await Dep.update_or_create(upd, **unq)
            if c:
                i += 1

    # binance locked stakes
    for ls in lst:
        d = ls["detail"]
        if d.get("asset") != d.get("rewardAsset"):
            raise Exception
        pid = ls["projectId"]
        pids.append(pid)
        unq = {"pid": pid, "ex_id": 1, "type": DepType.stake}
        if not d["isSoldOut"] or (d["isSoldOut"] and await Dep.exists(**unq, is_active=True)):
            upd = {
                "coin": await Coin.get_or_create_by_name(d["asset"]),
                "apr": d["apy"],
                "apr_is_fixed": True,
                "is_active": not d["isSoldOut"],
                "duration": d["duration"],
                "min_limit": ls["quota"]["minimum"],
                "max_limit": ls["quota"]["totalPersonalQuota"],
            }
            d, c = await Dep.update_or_create(upd, **unq)
            if c:
                i += 1
    # binance flexible stakes
    for fs in fst:
        d = fs["detail"]
        if d.get("asset") != d.get("rewardAsset"):
            raise Exception
        pid = fs["projectId"]
        pids.append(pid)
        unq = {"pid": pid, "ex_id": 1, "type": DepType.stake}
        if not d["isSoldOut"] or (d["isSoldOut"] and await Dep.exists(**unq, is_active=True)):
            upd = {
                "coin": await Coin.get_or_create_by_name(d["asset"]),
                "apr": d["apy"],
                # 'apr_is_fixed': True,
                "is_active": not d["isSoldOut"],
                "min_limit": fs["quota"]["minimum"],
                "max_limit": fs["quota"]["totalPersonalQuota"],
            }
            d, c = await Dep.update_or_create(upd, **unq)
            if c:
                i += 1
    # BETH
    br = await ebac.get_beth_rate()
    pids.append("BETH")
    d, c = await Dep.update_or_create(
        {"apr": br},
        pid="BETH",
        type=DepType.beth,
        apr_is_fixed=False,
        min_limit=0.0001,
        coin=await Coin.get_or_create_by_name("BETH"),
        ex_id=1,
    )
    if c:
        i += 1

    await ebac.close_connection()
    dlt = await Dep.filter(ex_id=1, pid__not_in=pids).delete()
    return i, dlt


async def bybit() -> tuple[int, int]:
    i, pids = 0, []
    # by_sess = HTTP(
    #     testnet=False,
    #     api_key=BYKEY,
    #     api_secret=BYSEC,
    # )
    # coins = by_sess.get_coin_info(coin='ETH')
    client = BybitEarn(BYT)
    # try:
    coins = await client.get_coins()
    # except HttpProcessingError:
    #     print('Bybit:coins http error')
    #     return 0, 0
    bls = (await client.get_home_earn_products(ProductType.fixed_term_saving_products))[
        "fixed_term_saving_products"
    ]  # fix
    bes = (await client.get_product_detail())["pos_staking_product_detail"]  # eth2
    bfs = (await client.get_home_earn_products(ProductType.flexible_saving_products))[
        "flexible_saving_products"
    ]  # flex
    await client.close()
    # eth2
    pid = bes["product_id"]
    pids.append(pid)
    unq = {"pid": pid, "coin": await Coin.get_or_create_by_name(bes["name"]), "ex_id": 4, "type": DepType.beth}
    apy = float(bes["yesterday_apy_e8"]) * 0.00000001
    dfd = {
        "apr": apy,
        "is_active": bes["status"] == 1,
        "min_limit": bes["min_investment"],
        "max_limit": bes["min_investment"],
    }
    d, c = await Dep.update_or_create(dfd, **unq)
    if c:
        i += 1
    # flex
    for bf in bfs:
        pid = bf["product_id"]
        pids.append(pid)
        unq = {
            "pid": pid,
            "coin": await Coin.get_or_create_by_name(bf["name"]),
            "ex_id": 4,
            "type": {"Savings": DepType.earn, "Flexible Staking": DepType.stake}[bf["category"]],
        }
        apy = float(bf["apy"][:-1]) * 0.01
        dfd = {
            "apr": apy,
            "is_active": bf["display_status"] == 1,
            "min_limit": 0,
            "max_limit": float(bf["product_max_share"]) - float(bf["total_deposit_share"]),
        }
        if bf["coin"] != bf["return_coin"]:
            raise Exception
            # dfd.update({'reward_coin': ccoin()})
        d, c = await Dep.update_or_create(dfd, **unq)
        if c:
            i += 1
    # fixed
    for bl in bls:
        pid = bl["product_id"]
        pids.append(pid)
        unq = {
            "pid": pid,
            "coin": await Coin.get_or_create_by_name(coins[bl["coin"]]),
            "ex_id": 4,
            "type": DepType.earn,
        }
        apy = float(bl["apy"][:-1]) * 0.01
        dfd = {
            "apr": apy,
            "is_active": bl["display_status"] == 1,
            "min_limit": 0,
            "duration": bl["staking_term"],
            "apr_is_fixed": True,
            "max_limit": float(bl["product_max_share"]) - float(bl["total_deposit_share"]),
        }
        if bl["coin"] != bl["return_coin"]:
            raise Exception
            # dfd.update({'reward_coin': ccoin()})
        d, c = await Dep.update_or_create(dfd, **unq)
        if c:
            i += 1
    dlt = await Dep.filter(ex_id=4, pid__not_in=pids).delete()
    return i, dlt


async def okx() -> tuple[int, int]:
    i, pids = 0, []

    cl = Okx()
    try:
        res = await cl.get("asset/earn/simple-earn/all-products")
    except HttpProcessingError:
        print("Okx http error")
        return 0, 0

    # print('okx web:', l:=len(res['data']['flexible'])+len(res['data']['fixed']), end=' ')
    # if not l:
    #     print(res)
    for f in res["data"]["flexible"]:
        coin: Coin = await Coin.get_or_create_by_name(f["investCurrency"]["currencyName"])
        rate = float(f["rate"]["rateNum"]["value"][0]) * 0.01
        if (
            f["lockUpPeriod"]
            or f["canPurchase"]
            or f["campaignUid"]
            or f["products"][0]["bonusCurrency"]
            or f["rate"]["rateType"] != "SINGLE_RATE"
            or len(f["rate"]["rateNum"]["value"]) != 1
        ):
            pass
        pid = f"{coin.ticker}_{rate}*flex"
        pids.append(pid)
        if (dep := await Dep.get_or_none(ex_id=3, pid=pid)) and dep.apr == rate:
            continue
        dct = {"apr": rate, "apr_is_fixed": f["rate"]["rateType"] == "SINGLE_RATE", "min_limit": 0}
        rwc = await Coin.get(ticker=f["products"][0]["interestCurrency"]["currencyName"])
        if rwc != coin:
            dct.update({"reward_coin": rwc})
        await Dep.update_or_create(dct, ex_id=3, coin=coin, pid=pid, type=DepType.earn, duration=0)
        i += 1
    for f in res["data"]["fixed"]:
        coin: Coin = await Coin.get_or_create_by_name(f["investCurrency"]["currencyName"])
        for p in f["products"]:
            rate = float(f["rate"]["rateNum"]["value"][0]) * 0.01
            dur = p["term"]["value"]
            if (
                p["lockUpPeriod"]
                or f["canPurchase"]
                or p["campaignUid"]
                or p["bonusCurrency"]
                or p["rate"]["rateType"] != "SINGLE_RATE"
                or len(p["rate"]["rateNum"]["value"]) != 1
            ):
                pass
            pid = f"{coin.ticker}_{rate}*{dur}"
            pids.append(pid)
            if (dep := await Dep.get_or_none(ex_id=3, pid=pid)) and dep.apr == rate:
                continue
            dct = {"apr": rate, "apr_is_fixed": p["rate"]["rateType"] == "SINGLE_RATE", "min_limit": 0}
            rwc = await Coin.get(ticker=f["products"][0]["interestCurrency"]["currencyName"])
            if rwc != coin:
                dct.update({"reward_coin": rwc})
            await Dep.update_or_create(dct, ex_id=3, coin=coin, pid=pid, type=DepType.earn, duration=dur)
            i += 1

    earning_api = EarningAPI(OKXKEY, OKXSEC, OKXPSF, flag="0", debug=False)  # flag = live trading: 0, demo trading: 1
    try:
        offers = gof["data"] if (gof := earning_api.get_offers()) else []
    except ReadTimeout:
        offers = []
    # print('okx api:', l:=len(offers), end=' ')
    # if not l:
    #     print(res)
    for of in offers:
        if of["state"] not in ("sold_out", "stop", "purchasable"):
            raise Exception
        if of["protocolType"] not in ("defi", "staking"):
            raise Exception
        pid = f"{of['productId']}_{of['ccy']}{'*'+of['term'] if int(of['term']) else ''}"
        pids.append(pid)
        unq = {"pid": pid, "ex_id": 3, "coin": await Coin.get_or_create_by_name(of["ccy"])}
        if len(of["investData"]) == 1 and (
            of["state"] == "purchasable" or (of["state"] != "purchasable" and await Dep.exists(**unq, is_active=True))
        ):
            if of["investData"][0]["ccy"] != of["ccy"]:
                raise Exception
            if of["protocol"] not in (
                "Regular interest",
                "Compound",
                "AAVE",
                "APE",
                "LOOKS",
                "Tokenlon",
                "GMX",
                "BETH",
            ):
                raise Exception("New protocol:", of["protocol"])
            dfd = {
                "apr": of["apy"],
                "is_active": of["state"] == "purchasable",
                "min_limit": of["investData"][0]["minAmt"],
                "max_limit": of["investData"][0]["maxAmt"],
                "duration": of["term"],
                "early_redeem": of["earlyRedeem"],
                "apr_is_fixed": of["protocol"] == "Regular interest",
                "type": DepType.stake,
            }
            if len(of["earningData"]) > 1:
                if len(of["earningData"]) > 2:
                    raise Exception
                rcs = [ed["ccy"] for ed in of["earningData"] if int(ed["earningType"])]
                if len(rcs) > 1:
                    raise Exception
                if rcs[0] != of["ccy"]:
                    dfd.update({"reward_coin": await Coin.get_or_create_by_name(of["ccy"])})
            d, c = await Dep.update_or_create(dfd, **unq)
            if c:
                i += 1
        else:
            if of["protocol"] != "Sushiswap" and of["state"] == "purchasable":
                raise Exception

    await cl.close()
    dlt = await Dep.filter(ex_id=3, pid__not_in=pids).delete()
    return i, dlt


async def cycle(func, idle: int):
    while True:
        print(f"{func.__name__[0]}:{(r:=await func())[0]}|{r[1]}")
        await sleep(idle)


async def main():
    await init_db(dsn, models)
    await Tortoise.generate_schemas()
    funcs = {okx: 17, Binance: 13, kucoin: 11, huobi: 23, bybit: 27}
    try:
        await gather(*(cycle(func, secs) for func, secs in funcs.items()))
    except KeyboardInterrupt:
        print("Stopped.")


run(main())
