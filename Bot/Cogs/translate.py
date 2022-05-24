from discord.ext import commands
from discord.commands import slash_command, Option
import discord
from gpytranslate import Translator

class TranslateV1(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command(name="translate", description="Uses Google Translate to translate the given message", guild_ids=[978546162745348116])
    async def translateMessages(self, ctx, *, message: Option(str, "The message to translate"), lang: Option(str, "The language to translate to")):
        trans = Translator()
        translatedMessage = await trans.translate(f"{message}", targetlang=f"{lang}")
        embed = discord.Embed()
        embed.description = translatedMessage.text
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(TranslateV1(bot))
