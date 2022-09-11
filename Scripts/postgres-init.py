import asyncio
import os
import sys
from pathlib import Path

import uvloop
from disquest_utils import DisQuestUsers
from dotenv import load_dotenv

path = Path(__file__).parents[1]
sys.path.append(os.path.join(str(path), "Bot"))
envPath = os.path.join(str(path), "Bot", ".env")

from miku_events_utils import MikuEventsUtils

load_dotenv(dotenv_path=envPath)

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_USER = os.getenv("Postgres_User")
POSTGRES_IP = os.getenv("Postgres_IP")
POSTGRES_PORT = os.getenv("Postgres_Port")
POSTGRES_DISQUEST_DATABASE = os.getenv("Postgres_Disquest_Database")
POSTGRES_EVENTS_DATABASE = os.getenv("Postgres_Events_Database")

DISQUEST_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_IP}:{POSTGRES_PORT}/{POSTGRES_DISQUEST_DATABASE}"
EVENTS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_IP}:{POSTGRES_PORT}/{POSTGRES_EVENTS_DATABASE}"

eventUtils = MikuEventsUtils()
disquestUtils = DisQuestUsers()


async def main():
    await disquestUtils.initTables(uri=DISQUEST_CONNECTION_URI)
    await eventUtils.initTables(uri=EVENTS_CONNECTION_URI)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
