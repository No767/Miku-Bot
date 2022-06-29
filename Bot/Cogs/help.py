from discord.commands import slash_command
from discord.ext import commands


class MainHelpV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="help",
        description="Provides the help page for Miku",
        guild_ids=[978546162745348116],
    )
    async def mikuHelp(self, ctx):
        for items in self.bot.walk_application_commands():
            print(items.name)
            print(items.description)
            # print(items.module)

            # print(dir(items))
        # cogs = self.bot.get_cog("MainHelpV1")
        # commands = cogs.get_commands()
        # print(commands)
        # for cog, commands in mapping.items():
        #     cogs = self.bot.get_cog("MainHelpV1")
        #     commands = cog.get_commands()
        #     print([c.name for c in commands])
        await ctx.respond("testing")


def setup(bot):
    bot.add_cog(MainHelpV1(bot))
