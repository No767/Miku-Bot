import os

import discord
from discord.ext import commands, bridge
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
Discord_Bot_Token = os.getenv("Gumi")
intents = discord.Intents.default()
intents.message_content = True
bot = bridge.Bot(command_prefix=".",  intents=intents, help_command=None)

# Loads in all extensions
initial_extensions = [
    "Cogs.translate",
    "Cogs.invitation",
    "Cogs.reddit",
    "Cogs.waifu-generator",
    "Cogs.disquest"
]
for extension in initial_extensions:
    bot.load_extension(extension)

# Adds in the bot presence
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))

# Run the bot
bot.run(Discord_Bot_Token)
