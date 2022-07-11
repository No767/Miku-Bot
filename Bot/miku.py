import logging
import os

import discord
from discord.ext import bridge
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
Discord_Bot_Token = os.getenv("Gumi")
intents = discord.Intents.default()
intents.message_content = True
bot = bridge.Bot(command_prefix=".", intents=intents, help_command=None)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

# Loads in all extensions
initial_extensions = [
    "Cogs.anilist",
    # "Cogs.disquest",
    "Cogs.events",
    "Cogs.events_task",
    "Cogs.help",
    "Cogs.info",
    "Cogs.invite",
    "Cogs.qrcode-maker",
    "Cogs.reddit",
    # "Cogs.translate",
    "Cogs.waifu",
]
for extension in initial_extensions:
    bot.load_extension(extension)

# Adds in the bot presence
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
    )


# Run the bot
bot.run(Discord_Bot_Token)
