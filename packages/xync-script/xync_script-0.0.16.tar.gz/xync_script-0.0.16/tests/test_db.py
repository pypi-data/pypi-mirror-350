import logging
from asyncio import run

from tortoise.backends.asyncpg import AsyncpgDBClient
from x_model import init_db
from xync_schema import models

from xync_script.loader import dsn

logging.basicConfig(level=logging.DEBUG)


def test_init_db():
    cn = run(init_db(dsn, models))
    assert isinstance(cn, AsyncpgDBClient), "DB corrupt"
