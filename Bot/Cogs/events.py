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
        try:
            dateOfToday = datetime.now().isoformat()
            user_id = ctx.author.id
            eventPassedInit = False
            eventUUID = uuid.uuid4()
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
        except Exception:
            await ctx.respond("Oops, something went wrong... Please try again")

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
                            title=dict(items)["name"],
                            description=dict(items)["description"],
                        )
                        .add_field(
                            name="Date Added",
                            value=parser.isoparse(dict(items)["date_added"]).strftime(
                                "%Y-%m-%d %H:%M:%S %Z"
                            ),
                            inline=True,
                        )
                        .add_field(
                            name="Event Date",
                            value=parser.isoparse(dict(items)["event_date"]).strftime(
                                "%Y-%m-%d %H:%M:%S %Z"
                            ),
                            inline=True,
                        )
                        .add_field(
                            name="Passed?",
                            value=dict(items)["event_passed"],
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
                            title=dict(mainItems)["name"],
                            description=dict(mainItems)["description"],
                        )
                        .add_field(
                            name="Date Added",
                            value=parser.isoparse(
                                dict(mainItems)["date_added"]
                            ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                            inline=True,
                        )
                        .add_field(
                            name="Event Date",
                            value=parser.isoparse(
                                dict(mainItems)["event_date"]
                            ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                            inline=True,
                        )
                        .add_field(
                            name="Passed?",
                            value=dict(mainItems)["event_passed"],
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
                            title=dict(mainItems2)["name"],
                            description=dict(mainItems2)["description"],
                        )
                        .add_field(
                            name="Date Added",
                            value=parser.isoparse(
                                dict(mainItems2)["date_added"]
                            ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                            inline=True,
                        )
                        .add_field(
                            name="Event Date",
                            value=parser.isoparse(
                                dict(mainItems2)["event_date"]
                            ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                            inline=True,
                        )
                        .add_field(
                            name="Passed?",
                            value=dict(mainItems2)["event_passed"],
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

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @eventsView.command(name="countdown")
    async def eventCountdown(
        self, ctx, *, name: Option(str, "The name of the event to search for")
    ):
        """Checks how much days until an event will happen and pass"""
        mainRes = await utils.obtainEventsName(ctx.author.id, name)
        try:
            if len(mainRes) == 0:
                raise NoItemsError
            else:
                embed = discord.Embed()
                for items in mainRes:
                    mainItem = dict(items)
                    parsedDate = parser.isoparse(mainItem["event_date"])
                    timeDiff = parsedDate - datetime.now()
                    countHours, rem = divmod(timeDiff.seconds, 3600)
                    countMinutes, countSeconds = divmod(rem, 60)
                    embed.description = f"{name} will happen in {timeDiff.days} day(s), {countHours} hour(s), {countMinutes} minute(s), and {countSeconds} second(s)"
                    embed.add_field(
                        name="Event Date (24hr)",
                        value=parsedDate.strftime("%Y-%m-%d %H:%M:%S"),
                        inline=True,
                    )
                    embed.add_field(
                        name="Today's Date (24hr)",
                        value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        inline=True,
                    )
                    await ctx.respond(embed=embed)
        except NoItemsError:
            embedError = discord.Embed()
            embedError.description = (
                f"Sadly there are no events with the name of {name}. Please try again."
            )
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @events.command(name="update")
    async def updateDate(
        self,
        ctx,
        *,
        name: Option(str, "The item to update"),
        date: Option(str, "The new date of the event"),
        time: Option(str, "The new time of the event"),
    ):
        """Updates the date and time of an event"""
        mainRes = await utils.obtainItemUUID(ctx.author.id, name)
        try:
            if len(mainRes) == 0:
                raise NoItemsError
            else:
                for item in mainRes:
                    fullDateTime = parser.parse(f"{date} {time}").isoformat()
                    await utils.updateEvent(ctx.author.id, item, fullDateTime)
                    await ctx.respond(f"{name} has been successfully updated.")
        except NoItemsError:
            embedError = discord.Embed()
            embedError.description = (
                f"Sadly there are no events with the name of {name}. Please try again."
            )
            await ctx.respond(embed=embedError)


def setup(bot):
    bot.add_cog(UserEvents(bot))
