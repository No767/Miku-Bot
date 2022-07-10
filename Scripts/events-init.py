import asyncio
import os
import sys

import uvloop

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "Bot"))

from miku_events_utils import MikuEventsUtils

utils = MikuEventsUtils()


async def main():
    await utils.initTables()


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
