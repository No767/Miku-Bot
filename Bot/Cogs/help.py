import discord
from discord.commands import Option, slash_command
from discord.ext import commands, pages


class MainHelpV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="help",
        description="Provides the help page for Miku",
        guild_ids=[978546162745348116],
    )
    async def mikuHelp(
        self,
        ctx,
        *,
        command: Option(
            str,
            "The command to search. This does not include subcommands.",
            required=False,
        ),
    ):
        if command is None:
            mainPages = pages.Paginator(
                pages=[
                    discord.Embed(
                        title=items.name, description=items.description
                    ).add_field(
                        name="Parent Name",
                        value=f"[{items.full_parent_name}]",
                        inline=True,
                    )
                    for items in self.bot.walk_application_commands()
                ]
            )
            await mainPages.respond(ctx.interaction, ephemeral=False)
        else:
            commandItem = self.bot.get_application_command(command)
            if commandItem is None:
                await ctx.respond(
                    embed=discord.Embed(
                        description="Sorry, but that command was not found. Please try again"
                    )
                )
            else:
                embed = discord.Embed()
                if len(commandItem.options) == 0:
                    commandItemOptions = None
                else:
                    commandItemOptionsMain = commandItem.options
                    for items in commandItemOptionsMain:
                        commandItemOptions = items.name
                embed.title = commandItem.qualified_name
                embed.description = commandItem.description
                embed.add_field(name="Options", value=commandItemOptions, inline=True)
                embed.add_field(
                    name="Parent Command",
                    value=f"[{commandItem.full_parent_name}]",
                    inline=True,
                )
                embed.add_field(name="Type", value=commandItem.type, inline=True)
                await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(MainHelpV1(bot))
