import asyncio
import logging

from discord.ext import commands
from miku_events_utils import MikuEventsUtils

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

eventUtils = MikuEventsUtils()


class EventTaskProcess:
    def __init__(self):
        self.self = self

    async def checkEventPassed(self):
        """Checks if the event has passed, and then set the value as passed"""
        while True:
            await asyncio.sleep(3)
            logging.info("bruh")


class EventTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(ctx):
        mainProcesses = EventTaskProcess()
        loop = asyncio.get_event_loop()
        task = loop.create_task(mainProcesses.checkEventPassed(), name="EventTasks")
        background_tasks = set(await task)
        await task.add_done_callback(background_tasks.discard)
        loop.run_forever()
        await task


def setup(bot):
    bot.add_cog(EventTasks(bot))
