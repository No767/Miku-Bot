import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
Discord_Bot_Token = os.getenv("Gumi")
bot = commands.Bot()

# Loads in all extensions
initial_extensions = [
    "Cogs.images",
    "Cogs.translate"
]
for extension in initial_extensions:
    bot.load_extension(extension)


# Adds in the bot presence
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/kumikohelp"))

# Run the bot
bot.run(Discord_Bot_Token)
