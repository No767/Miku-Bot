import asyncio
import uuid
from datetime import datetime

import discord
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from miku_events_utils import MikuEventsUtils
from rin_exceptions import NoItemsError

utils = MikuEventsUtils()


class View(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction):
        itemUUIDAuth = await utils.obtainItemUUIDAuth(interaction.user.id)
        try:
            if len(itemUUIDAuth) == 0:
                raise NoItemsError
            else:
                for itemUUID in itemUUIDAuth:
                    pass
                await utils.deleteAllUserEvent(interaction.user.id)
                await interaction.response.send_message(
                    "Confirmed. All events that belong to you are purged. This is permanent and irreversible."
                )
        except NoItemsError:
            await interaction.response.send_message(
                "It seems like you don't have any to delete from at all..."
            )

    @discord.ui.button(
        label="No",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:xmark:314349398824058880>"),
    )
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message("Well glad you choose not to...")


class UserEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    events = SlashCommandGroup(
        "events", "Commands for Miku's Events System", guild_ids=[978546162745348116]
    )
    eventsView = events.create_subgroup(
        "view", "View the events", guild_ids=[978546162745348116]
    )
    eventsDelete = events.create_subgroup(
        "delete",
        "Delete commands for the events system",
        guild_ids=[978546162745348116],
    )

    @events.command(name="create")
    async def eventCreate(
        self,
        ctx,
        *,
        name: Option(str, "The name of the event"),
        description: Option(str, "The description of the event"),
        date: Option(str, "The date of the event"),
        time: Option(str, "The time of the event (eg 1:53 pm). Also supports seconds"),
    ):
        """Creates a new event"""
        dateOfToday = datetime.now().isoformat()
        user_id = ctx.author.id
        eventPassedInit = False
        eventUUID = uuid.uuid4().hex[:16]
        fullEventDateTimeInput = parser.parse(f"{date} {time}").isoformat()
        await utils.insertNewEvent(
            event_uuid=eventUUID,
            user_id=user_id,
            date_added=dateOfToday,
            name=name,
            description=description,
            event_date=fullEventDateTimeInput,
            event_passed=eventPassedInit,
        )
        await ctx.respond("Event created!")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eventsView.command(name="all")
    async def eventView(self, ctx):
        """Views all of your past and upcoming events"""
        user_id = ctx.author.id
        userEvents = await utils.selectUserEvent(user_id=user_id)
        try:
            if len(userEvents) == 0:
                raise NoItemsError
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=items.__dict__["name"],
                            description=items.__dict__["description"],
                        )
                        .add_field(
                            name="Date Added",
                            value=parser.isoparse(
                                items.__dict__["date_added"]
                            ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                            inline=True,
                        )
                        .add_field(
                            name="Event Date",
                            value=parser.isoparse(
                                items.__dict__["event_date"]
                            ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                            inline=True,
                        )
                        .add_field(
                            name="Passed?",
                            value=items.__dict__["event_passed"],
                            inline=True,
                        )
                        for items in userEvents
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
        except NoItemsError:
            embedNoItemsError = discord.Embed()
            embedNoItemsError.description = "There seems to be no events found that belong to you. Please create one to start."
            await ctx.respond(embed=embedNoItemsError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eventsView.command(name="upcoming")
    async def eventView(self, ctx):
        """View all of your upcoming events"""
        user_id = ctx.author.id
        userEventsPassed = await utils.selectUserEventPassed(
            user_id=user_id, event_passed=False
        )
        try:
            if len(userEventsPassed) == 0:
                raise NoItemsError
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=mainItems.__dict__["name"],
                            description=mainItems.__dict__["description"],
                        )
                        .add_field(
                            name="Date Added",
                            value=parser.isoparse(
                                mainItems.__dict__["date_added"]
                            ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                            inline=True,
                        )
                        .add_field(
                            name="Event Date",
                            value=parser.isoparse(
                                mainItems.__dict__["event_date"]
                            ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                            inline=True,
                        )
                        .add_field(
                            name="Passed?",
                            value=mainItems.__dict__["event_passed"],
                            inline=True,
                        )
                        for mainItems in userEventsPassed
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
        except NoItemsError:
            embedNoItemsError = discord.Embed()
            embedNoItemsError.description = "There seems to be no upcoming events found that belong to you. Please create one to start."
            await ctx.respond(embed=embedNoItemsError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eventsView.command(name="past")
    async def eventViewPast(self, ctx):
        """View all of your past events"""
        user_id = ctx.author.id
        userEventsPassed = await utils.selectUserEventPassed(
            user_id=user_id, event_passed=True
        )
        try:
            if len(userEventsPassed) == 0:
                raise NoItemsError
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=mainItems2.__dict__["name"],
                            description=mainItems2.__dict__["description"],
                        )
                        .add_field(
                            name="Date Added",
                            value=parser.isoparse(
                                mainItems2.__dict__["date_added"]
                            ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                            inline=True,
                        )
                        .add_field(
                            name="Event Date",
                            value=parser.isoparse(
                                mainItems2.__dict__["event_date"]
                            ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                            inline=True,
                        )
                        .add_field(
                            name="Passed?",
                            value=mainItems2.__dict__["event_passed"],
                            inline=True,
                        )
                        for mainItems2 in userEventsPassed
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
        except NoItemsError:
            embedNoItemsError = discord.Embed()
            embedNoItemsError.description = "There seems to be no past events found that belong to you. Please create one to start."
            await ctx.respond(embed=embedNoItemsError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eventsDelete.command(name="one")
    async def eventDeleteOne(
        self, ctx, name: Option(str, "The name of the event you wish to delete")
    ):
        """Deletes one event from your list of events"""
        userObtainUUID = await utils.obtainItemUUID(user_id=ctx.author.id, name=name)
        try:
            if len(userObtainUUID) == 0:
                raise NoItemsError
            else:
                for itemUUID in userObtainUUID:
                    eventItemUUID = itemUUID
                await utils.deleteOneUserEvent(
                    user_id=ctx.author.id, event_uuid=eventItemUUID
                )
                await ctx.respond("Event successfully deleted")
        except NoItemsError:
            embedNoItemsError = discord.Embed()
            embedNoItemsError.description = "There are no events that have that name. Therefore, the deletion process is rejected. Please try again"
            await ctx.respond(embed=embedNoItemsError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eventsDelete.command(name="all")
    async def eventDeleteAll(self, ctx):
        """Purges all events from your user. (WARNING: THIS IS PERMANENT)"""
        embed = discord.Embed()
        embed.description = "Are you sure you want to delete all of your events? This is permanent and cannot be undone."
        await ctx.respond(embed=embed, view=View())


def setup(bot):
    bot.add_cog(UserEvents(bot))
