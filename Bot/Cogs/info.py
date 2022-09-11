import asyncio
import platform

import discord
import uvloop
from discord.commands import Option, SlashCommandGroup
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
    async def getUserInfo(
        self, ctx, *, user: Option(discord.Member, "The user to get the info of")
    ):
        """Gets info about the requested user"""
        try:
            embed = discord.Embed()
            embed.set_thumbnail(url=user.display_avatar.url)
            embed.title = user.display_name
            embed.add_field(
                name="On Nitro Since (UTC)",
                value=user.premium_since.strftime("%Y-%m-%d %H:%M:%S")
                if user.premium_since is not None
                else None,
                inline=True,
            )
            embed.add_field(
                name="Account Creation Date (UTC)",
                value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                inline=True,
            )
            embed.add_field(
                name="Server Join Date (UTC)",
                value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S")
                if user.joined_at is not None
                else None,
                inline=True,
            )
            embed.add_field(
                name="Timeout Since",
                value=user.communication_disabled_until.strftime("%Y-%m-%d %H:%M:%S")
                if user.communication_disabled_until is not None
                else None,
                inline=True,
            )
            embed.add_field(
                name="Roles",
                value=str([roleName.name for roleName in user.roles][1:]).replace(
                    "'", ""
                ),
                inline=True,
            )
            embed.add_field(
                name="Desktop Status", value=user.desktop_status, inline=True
            )
            embed.add_field(name="Web Status", value=user.web_status, inline=True)
            embed.add_field(name="On Mobile?", value=user.is_on_mobile(), inline=True)
            embed.add_field(name="Bot?", value=user.bot, inline=True)
            embed.add_field(name="Top Role", value=user.top_role.name, inline=True)
            embed.add_field(
                name="Mutual Guilds",
                value=str([guilds.name for guilds in user.mutual_guilds]).replace(
                    "'", ""
                ),
                inline=True,
            )
            embed.add_field(name="Guild Nickname", value=user.nick, inline=True)
            embed.add_field(name="On Timeout?", value=user.timed_out, inline=True)
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"An error occured: {type(e).__name__}: {str(e)}")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(InfoV1(bot))
