from discord.ext import commands
import discord
from discord.commands import slash_command
class invite(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
        
    @slash_command(name="invite", description="Provides the invite links for Miku")
    async def invite(self, ctx):
        embed = discord.Embed()
        embed.description = f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8"
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(invite(bot))
