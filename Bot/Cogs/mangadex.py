import asyncio

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from rin_exceptions import NoItemsError

jsonParser = simdjson.Parser()


class MangaDexV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    md = SlashCommandGroup("mangadex", "Commmands for the MangaDex service")
    mdSearch = md.create_subgroup("search", "Search for stuff on MangaDex")

    @mdSearch.command(name="manga")
    async def manga(self, ctx, *, manga: Option(str, "Name of Manga")):
        """Searches for up to 25 manga on MangaDex"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "title": manga,
                "publicationDemographic[]": "none",
                "contentRating[]": "safe",
                "order[title]": "asc",
                "limit": 25,
                "includes[]": "cover_art",
            }
            async with session.get(
                f"https://api.mangadex.org/manga/", params=params
            ) as r:
                data = await r.content.read()
                dataMain = jsonParser.parse(data, recursive=True)
                try:
                    if len(dataMain["data"]) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=mainItem["attributes"]["title"]["en"]
                                    if "en" in mainItem["attributes"]["title"]
                                    else mainItem["attributes"]["title"],
                                    description=mainItem["attributes"]["description"][
                                        "en"
                                    ]
                                    if "en" in mainItem["attributes"]["description"]
                                    else mainItem["attributes"]["description"],
                                )
                                .add_field(
                                    name="Original Language",
                                    value=f'[{mainItem["attributes"]["originalLanguage"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Last Volume",
                                    value=f'[{mainItem["attributes"]["lastVolume"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Last Chapter",
                                    value=f'[{mainItem["attributes"]["lastChapter"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Status",
                                    value=f'[{mainItem["attributes"]["status"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Year",
                                    value=f'[{mainItem["attributes"]["year"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Content Rating",
                                    value=f'[{mainItem["attributes"]["contentRating"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Created At",
                                    value=parser.isoparse(
                                        mainItem["attributes"]["createdAt"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Last Updated At",
                                    value=parser.isoparse(
                                        mainItem["attributes"]["updatedAt"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Available Translated Language",
                                    value=f'{mainItem["attributes"]["availableTranslatedLanguages"]}'.replace(
                                        "'", ""
                                    ),
                                    inline=True,
                                )
                                .add_field(
                                    name="Tags",
                                    value=str(
                                        [
                                            str(
                                                [
                                                    val
                                                    for _, val in items["attributes"][
                                                        "name"
                                                    ].items()
                                                ]
                                            )
                                            .replace("[", "")
                                            .replace("]", "")
                                            .replace("'", "")
                                            for items in mainItem["attributes"]["tags"]
                                        ]
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                .add_field(
                                    name="MangaDex URL",
                                    value=f'https://mangadex.org/title/{mainItem["id"]}',
                                    inline=True,
                                )
                                .set_image(
                                    url=str(
                                        [
                                            f'https://uploads.mangadex.org/covers/{mainItem["id"]}/{items["attributes"]["fileName"]}'
                                            for items in mainItem["relationships"]
                                            if items["type"]
                                            not in ["manga", "author", "artist"]
                                        ]
                                    )
                                    .replace("'", "")
                                    .replace("[", "")
                                    .replace("]", "")
                                )
                                for mainItem in dataMain["data"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedErrorAlt2 = discord.Embed()
                    embedErrorAlt2.description = "Sorry, but the manga you searched for does not exist or is invalid. Please try again."
                    await ctx.respond(embed=embedErrorAlt2)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @md.command(name="random")
    async def manga_random(self, ctx):
        """Returns an random manga from MangaDex"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get("https://api.mangadex.org/manga/random") as r:
                data2 = await r.content.read()
                dataMain2 = jsonParser.parse(data2, recursive=True)
                mangaFilter2 = [
                    "tags",
                    "title",
                    "altTitles",
                    "description",
                    "links",
                    "background",
                    "createdAt",
                    "updatedAt",
                ]
                tagFilter = ["id", "type", "relationships"]
                embedVar = discord.Embed()
                try:
                    try:
                        if r.status == 500:
                            embedErrorMain = discord.Embed()
                            embedErrorMain.description = "It seems like there is no manga to select from... Don't worry about it, just try again"
                            embedErrorMain.add_field(
                                name="HTTP Response Code", value=r.status, inline=True
                            )
                            await ctx.respond(embed=embedErrorMain)
                        elif len(dataMain2["data"]) == 0:
                            raise ValueError
                        else:
                            mangaTitle2 = (
                                dataMain2["data"]["attributes"]["title"]["en"]
                                if "en" in dataMain2["data"]["attributes"]["title"]
                                else dataMain2["data"]["attributes"]["title"]
                            )
                            mainDesc2 = (
                                dataMain2["data"]["attributes"]["description"]["en"]
                                if "en"
                                in dataMain2["data"]["attributes"]["description"]
                                else dataMain2["data"]["attributes"]["description"]
                            )
                            for k, v in dataMain2["data"]["attributes"].items():
                                if k not in mangaFilter2:
                                    embedVar.add_field(
                                        name=k, value=f"[{v}]", inline=True
                                    )
                            for tagItem in dataMain2["data"]["attributes"]["tags"]:
                                mainTags = [
                                    v["name"]["en"]
                                    for k, v in tagItem.items()
                                    if k not in tagFilter
                                ]
                            for item in dataMain2["data"]["relationships"]:
                                mangaID2 = dataMain2["data"]["id"]
                                if item["type"] not in ["manga", "author", "artist"]:
                                    coverArtID2 = item["id"]
                                    async with session.get(
                                        f"https://api.mangadex.org/cover/{coverArtID2}"
                                    ) as rp:
                                        cover_art_data2 = await rp.json(
                                            loads=orjson.loads
                                        )
                                        cover_art2 = cover_art_data2["data"][
                                            "attributes"
                                        ]["fileName"]
                                        embedVar.set_image(
                                            url=f"https://uploads.mangadex.org/covers/{mangaID2}/{cover_art2}"
                                        )
                            embedVar.title = (
                                str(mangaTitle2)
                                .replace("'", "")
                                .replace("[", "")
                                .replace("]", "")
                            )
                            embedVar.description = (
                                str(mainDesc2)
                                .replace("'", "")
                                .replace("[", "")
                                .replace("]", "")
                            )
                            embedVar.add_field(
                                name="Alt Titles",
                                value=str(
                                    [
                                        v
                                        for items in dataMain2["data"]["attributes"][
                                            "altTitles"
                                        ]
                                        for _, v in items.items()
                                    ]
                                ).replace("'", ""),
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Tags",
                                value=str(mainTags).replace("'", ""),
                                inline=True,
                            )
                            embedVar.add_field(
                                name="MangaDex URL",
                                value=f'https://mangadex.org/title/{dataMain2["data"]["id"]}',
                                inline=True,
                            )
                            await ctx.respond(embed=embedVar)
                    except ValueError:
                        embedValErrorMain = discord.Embed()
                        embedValErrorMain.description = "It seems like there wasn't any manga found. Please try again"
                        await ctx.respond(embed=embedValErrorMain)
                except Exception as e:
                    embedErrorMain = discord.Embed()
                    embedErrorMain.description = "There was an error. Please try again."
                    embedErrorMain.add_field(name="Error", value=e, inline=True)
                    await ctx.respond(embed=embedErrorMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(MangaDexV1(bot))
