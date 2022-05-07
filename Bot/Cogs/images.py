import bs4
import random
from discord.ext import commands
import discord
from discord.commands import slash_command, Option
import aiohttp
import uvloop
import orjson
import asyncio

class ImageScraperV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command(name="image", description="Scrapes some images off of DeviantArt", guild_ids=[866199405090308116])
    async def imageScraperV2(self, ctx, *, search: Option(str, "The search query to perform")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"q": search}
            async with session.get("https://www.deviantart.com/search", params=params) as r:
                data = await r.text()
                soup = bs4.BeautifulSoup(data, "lxml")
                links = []
                link = f"https://www.deviantart.com/search?&q={search}"
                for item in soup.find_all('img'):
                    if not 'avatar' in item['src'] and not 'hover' in item['src'] and not 'logo' in item['src'] and not 'icon' in item['src'] and not 'data' in item['src']:
                        if '//' in item['src']:
                            links.append(item['src'])
                        else:
                            links.append('https://'+ link.split('/')[2] + item['src'])
                embedVar = discord.Embed()
                embedVar.set_image(url=random.choice(links))
                await ctx.respond(embed=embedVar)
                # except Exception:
                #     embed = discord.Embed()
                #     embed.description = "Sorry, but it seems like there was no results for that... Please try agian"
                #     await ctx.respond(embed=embed)
    
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
def setup(bot):
    bot.add_cog(ImageScraperV2(bot))