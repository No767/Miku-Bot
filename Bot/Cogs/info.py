import asyncio
import platform

import discord
import uvloop
from discord.commands import SlashCommandGroup
from discord.ext import commands


class InfoV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    info = SlashCommandGroup(
        "info", "Commands that provide info", guild_ids=[978546162745348116]
    )

    @info.command(name="bot")
    async def botinfo(self, ctx):
        """Returns Stats for Miku"""
        bot = self.bot
        name = bot.user.name
        guilds = bot.guilds
        total_members = 0
        for guild in guilds:
            total_members += guild.member_count
        average_members_per_guild = total_members / len(guilds)
        embed = discord.Embed()
        embed.title = "Bot Info"
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="Servers", value=len(guilds), inline=True)
        embed.add_field(name="Total Users", value=total_members, inline=True)
        embed.add_field(
            name="Average Users Per Server",
            value=average_members_per_guild,
            inline=True,
        )
        embed.add_field(name="OS", value=f"[{platform.system()}]", inline=True)
        embed.add_field(name="Kernel", value=f"[{platform.release()}]", inline=True)
        embed.add_field(
            name="Machine Type", value=f"[{platform.machine()}]", inline=True
        )
        embed.add_field(
            name="Python Version", value=f"[{platform.python_version()}]", inline=True
        )
        embed.set_thumbnail(url=bot.user.display_avatar)
        await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @info.command(name="user")
    async def userInfo(self, ctx: discord.ClientUser):
        """Provides info about the current user"""
        embedUser = discord.Embed()
        embedUser.title = ctx.author.name
        embedUser.add_field(name="Bot Account?", value=ctx.author.bot, inline=True)
        embedUser.add_field(
            name="Creation Date (UTC, 24hr)",
            value=ctx.author.created_at.strftime("%Y-%m-%d %H:%M"),
            inline=True,
        )
        embedUser.add_field(
            name="Creation Date (UTC, 12hr or AM/PM)",
            value=ctx.author.created_at.strftime("%Y-%m-%d %I:%M %p"),
            inline=True,
        )
        embedUser.add_field(
            name="Discriminator", value=ctx.author.discriminator, inline=True
        )
        embedUser.add_field(
            name="Display Name", value=ctx.author.display_name, inline=True
        )
        embedUser.add_field(name="ID", value=ctx.author.id, inline=True)
        embedUser.set_thumbnail(url=ctx.author.display_avatar)
        await ctx.respond(embed=embedUser)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(InfoV1(bot))
