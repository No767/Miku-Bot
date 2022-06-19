import asyncio
import os
import random

import asyncpraw
import discord
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from rin_exceptions import ThereIsaRSlashInSubreddit, NoItemsError
import datetime

load_dotenv()

Reddit_ID = os.getenv("Reddit_ID")
Reddit_Secret = os.getenv("Reddit_Secret")


class RedditV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    reddit = SlashCommandGroup("reddit", "Commands for Reddit Service", guild_ids=[978546162745348116])
    redditUsers = reddit.create_subgroup("users", "Subgroup for Reddit Users", guild_ids=[978546162745348116])

    @reddit.command(name="search")
    async def redditSearch(
        self,
        ctx,
        *,
        search: Option(
            str,
            "The query you want to search. Also supports searching subreddits as well",
        ),
    ):
        """Searches on Reddit for Content"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:miku:v0.1.0 (by /u/No767)",
        ) as api:
            original_search = search
            try:
                if "r/" in search:
                    search = search.split("/")
                    sub = search[1]
                    search = "all"
                else:
                    sub = "all"
                sub = await api.subreddit(sub)
                searcher = sub.search(query=search)
                posts = [
                    post
                    async for post in searcher
                    if ".jpg" in post.url
                    or ".png" in post.url
                    or ".gif" in post.url
                    and not post.over_18
                ]
                try:
                    if len(posts) == 0:
                        raise NoItemsError
                    else:
                        post = random.choice(posts) # nosec B311
                        submission = post
                        await post.author.load()
                        reddit_embed = discord.Embed(
                            color=discord.Color.from_rgb(255, 69, 0))
                        reddit_embed.title = submission.title
                        reddit_embed.description = submission.selftext
                        reddit_embed.set_image(url=submission.url)
                        reddit_embed.add_field(name="Author", value=submission.author.name, inline=True)
                        reddit_embed.add_field(name="Subreddit", value=f"r/{submission.subreddit.display_name}", inline=True)
                        reddit_embed.add_field(name="URL", value=f"https://reddit.com{submission.permalink}", inline=True)
                        reddit_embed.add_field(name="Upvotes", value=submission.score, inline=True)
                        reddit_embed.add_field(name="NSFW?", value=submission.over_18, inline=True)
                        reddit_embed.add_field(name="Flair", value=submission.link_flair_text, inline=True)
                        reddit_embed.add_field(name="Number of comments", value=submission.num_comments, inline=True)
                        reddit_embed.add_field(name="Created At (UTC, 24hr)", value=datetime.datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M'), inline=True)
                        reddit_embed.add_field(name="Created At (UTC, 12hr or AM/PM)", value=datetime.datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %I:%M %p'), inline=True)
                        reddit_embed.set_thumbnail(url=post.author.icon_img)
                        await ctx.respond(embed=reddit_embed)
                except NoItemsError:
                    await ctx.respond(embed=discord.Embed(description=f"It seems like there are no posts that could be found with the query {search}. Please try again"))
            except Exception as e:
                embed = discord.Embed()
                embed.description = f"There was an error, this is likely caused by a lack of posts found in the query {original_search}. Please try again."
                embed.add_field(name="Reason", value=e, inline=True)
                await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @reddit.command(name="feed")
    async def redditFeed(self, ctx, *, subreddit: Option(str, "The subreddit to search"), filters: Option(str, "Sort by filters - new, hot, top, etc", choices=["new", "top", "hot", "rising"])):
        """Provides up to 25 reddit posts based on the filters provided"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:miku:v0.1.0 (by /u/No767)",
        ) as redditapi:
            try:
                try:
                    if "r/" in subreddit:
                        raise ThereIsaRSlashInSubreddit
                    else:
                            mainSub = await redditapi.subreddit(str(subreddit))
                            if "new" in filters:
                                subLooper = mainSub.new(limit=25)
                            elif "top" in filters:
                                subLooper = mainSub.top(limit=25)
                            elif "hot" in filters:
                                subLooper = mainSub.hot(limit=25)
                            elif "rising" in filters:
                                subLooper = mainSub.rising(limit=25)
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        title=submission.title, description=submission.selftext
                                    )
                                    # .add_field(name="Author", value=submission.author.name, inline=True)
                                    .add_field(name="Created At (UTC, 24hr)", value=datetime.datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M'), inline=True)
                                    .add_field(name="Created At (UTC, 12hr or AM/PM)", value=datetime.datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %I:%M %p'), inline=True)
                                    .add_field(name="Flair", value=submission.link_flair_text, inline=True)
                                    .add_field(name="Number of Comments", value=submission.num_comments, inline=True)
                                    .add_field(name="NSFW?", value=submission.over_18, inline=True)
                                    .add_field(name="URL", value=f"https://reddit.com{submission.permalink}", inline=True)
                                    .add_field(name="Upvotes", value=submission.score, inline=True)
                                    .add_field(name="Spoiler?", value=submission.spoiler, inline=True)
                                    .set_image(url=submission.url)
                                    async for submission in subLooper
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                except ThereIsaRSlashInSubreddit:
                    await ctx.respond(embed=discord.Embed(description="There seems to be an `r/` within the subreddit that you put in. In order for this to work, you have to leave out the `r/`"))
            except Exception:
                embedError = discord.Embed()
                embedError.description = f"There was an error with the query. This is more than likely due to a invalid subreddit name, or a search on a private subreddit. Please try again."
                await ctx.respond(embed=embedError)
                
    
    @redditUsers.command(name="info")
    async def redditor(self, ctx, *, redditor: Option(str, "The name of the Redditor")):
        """Provides info about a Redditor"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:miku:v0.1.0 (by /u/No767)",
        ) as redditorApi:
            try:
                user = await redditorApi.redditor(redditor)
                await user.load()
                embedVar = discord.Embed()
                embedVar.title = user.name
                embedVar.set_thumbnail(url=user.icon_img)
                embedVar.add_field(
                    name="Comment Karma", value=user.comment_karma, inline=True
                )
                embedVar.add_field(name="Created At (UTC, 24hr)", value=datetime.datetime.fromtimestamp(user.created_utc).strftime('%Y-%m-%d %H:%M'), inline=True)
                embedVar.add_field(name="Created At (UTC, 12hr or AM/PM)", value=datetime.datetime.fromtimestamp(user.created_utc).strftime('%Y-%m-%d %I:%M %p'), inline=True)
                embedVar.add_field(
                    name="Link Karma", value=user.link_karma, inline=True
                )
                await ctx.respond(embed=embedVar)
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = "Something went wrong. Please try again..."
                embedError.add_field(name="Reason", value=e, inline=True)
                await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def setup(bot):
    bot.add_cog(RedditV1(bot))