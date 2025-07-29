from asyncio import run
from pg_channel import plsql, Act
from pyrogram.enums import ClientPlatform
from tortoise.backends.asyncpg import AsyncpgDBClient
from x_auth.models import App, Dc
from x_model import init_db
from xync_schema import models
from xync_schema.enums import exs
from xync_schema.models import Ex, TestEx, ExAction

from xync_script.loader import DSN


async def main(cn: AsyncpgDBClient = None):
    if not cn:
        cn = await init_db(DSN, models, True)
    # dirty hack for on_update user.id->fiat.user_id
    # await cn.execute_query("alter table cred drop constraint cred_person_id_fkey;")
    # await cn.execute_query(
    #     'alter table cred add foreign key (person_id) references "person" on update cascade on delete cascade;'
    # )
    await Ex.bulk_create(
        (
            Ex(name=n, type_=val[0], logo=val[1], host=val[2], host_p2p=val[3], url_login=val[4], status=val[5])
            for n, val in exs.items()
        ),
        update_fields=["host", "host_p2p", "logo", "url_login"],
        on_conflict=["name", "type_"],
    )
    texs = [TestEx(ex=ex, action=act) for act in ExAction for ex in await Ex.exclude(logo="")]
    await TestEx.bulk_create(texs, ignore_conflicts=True)
    print("Exs&TestExs filled DONE")

    # await set_triggers(cn)
    # print("Triggers set DONE")

    await Dc.update_or_create(id=1, ip="149.154.175.56")
    await Dc.update_or_create(
        id=2,
        ip="149.154.167.50",
        pub="MIIBCgKCAQEA6LszBcC1LGzyr992NzE0ieY+BSaOW622Aa9Bd4ZHLl+Tu"
        "FQ4lo4g5nKaMBwK/BIb9xUfg0Q29/2mgIR6Zr9krM7HjuIcCzFvDtr+L0"
        "GQjae9H0pRB2OO62cECs5HKhT5DZ98K33vmWiLowc621dQuwKWSQKjWf5"
        "0XYFw42h21P2KXUGyp2y/+aEyZ+uVgLLQbRA1dEjSDZ2iGRy12Mk5gpYc"
        "397aYp438fsJoHIgJ2lgMv5h7WY9t6N/byY9Nw9p21Og3AoXSL2q/2IJ1"
        "WRUhebgAdGVMlV1fkuOQoEzR7EdpqtQD9Cs5+bfo3Nhmcyvk5ftB0WkJ9"
        "z6bNZ7yxrP8wIDAQAB",
    )
    await Dc.update_or_create(id=4, ip="149.154.167.91")
    await Dc.update_or_create(id=5, ip="91.108.56.112")
    await App.update_or_create(
        id=20373304,
        hsh="ebb72106dfd08d613093f81ab3c9b362",
        title="XyncNet",
        short="XyncNet",
        dc_id=2,
        ver="1.1",
        platform=ClientPlatform.IOS,
    )
    await cn.close()


async def set_triggers(cn: AsyncpgDBClient):
    # plsql("dep", Act.NEW+Act.UPD, {"stts": ("is_active",), "_prof": ["apr", "max_limit", "fee"]})
    ad = plsql("ad", Act.NEW + Act.UPD + Act.DEL, {"prof": ["price", "max_fiat", "min_fiat"], "stts": ("status",)})
    order = plsql("order", Act.NEW + Act.UPD + Act.DEL, {"stts": ("status",)})
    msg = plsql("msg", Act.NEW)
    await cn.execute_script(ad)
    await cn.execute_script(order)
    await cn.execute_script(msg)


if __name__ == "__main__":
    run(main())
