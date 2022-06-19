import os

import discord
import discord.ext
import qrcode
from discord.commands import Option, slash_command
from discord.ext import commands


class qrcode_maker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="qrcode", description="Makes a QR code")
    async def code(
        self,
        ctx,
        *,
        link: Option(
            str, "The link that you want the qr code to have, or any text you wish"
        )
    ):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        if str(os.path.isfile("/qrcode/qrcode.png")) == "False":
            img = qrcode.make(link)
            img.save("./qrcode/qrcode.png")
        else:
            img = qrcode.make(link)
            img.save("./qrcode/qrcode.png")
        file = discord.File("./qrcode/qrcode.png")
        embedVar = discord.Embed()
        embedVar.set_image(url="attachment://qrcode.png")
        await ctx.respond(embed=embedVar, file=file)


def setup(bot):
    bot.add_cog(qrcode_maker(bot))
