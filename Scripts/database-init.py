import asyncio
import os

import uvloop
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Column, Integer, MetaData, Table
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

PASSWORD = os.getenv("Postgres_Password")
IP = os.getenv("Postgres_IP")
USER = os.getenv("Postgres_User")
DATABASE = os.getenv("Postgres_Database")
PORT = os.getenv("Postgres_Port")


async def main():
    meta = MetaData()
    engine = create_async_engine(
        f"postgresql+asyncpg://{USER}:{PASSWORD}@{IP}:{PORT}/{DATABASE}", echo=True
    )
    Table(
        "users",
        meta,
        Column("id", BigInteger),
        Column("gid", BigInteger),
        Column("xp", Integer),
    )
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
