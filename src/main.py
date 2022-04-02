import re
import os
import asyncpraw
import nextcord
from nextcord.ext import commands

cogs = ["cogs.img", "cogs.misc", "cogs.fun", "cogs.slash"]
ids = [766423223595696198, 921103309526433843]
COMMAND_PREFIX = '?'
client = commands.Bot(COMMAND_PREFIX)
client.remove_command('help')

reddit_data = os.environ.get("REDDIT_API_DATA").split(",")
client.reddit = asyncpraw.Reddit(
    client_id = reddit_data[0],
    client_secret = reddit_data[1],
    username = reddit_data[2],
    password = reddit_data[3],
    user_agent = reddit_data[4]
)

@client.event
async def on_ready():
    for i in cogs:
        client.load_extension(i)
        print("Initialised cog: " + i)
    print('Online')

    for i in ids:
        guild = client.get_guild(i)
        await guild.rollout_application_commands()

@client.command(name = "ping", aliases = ["pong"])
async def ping(ctx):
    await ctx.send("Ping: " + (str(round(client.latency * 1000))) + "ms")

@client.event
async def on_message(message):
    if re.search("^<@!?921100533224337489>\\s+?prefix", message.content):
        await message.channel.send("The bot's prefix is `" + COMMAND_PREFIX + "`")
    await client.process_commands(message)

@client.command(name = "setstatus", aliases = ["status"])
async def setstatus(ctx, *, msg = None):
    if await client.is_owner(ctx.author):
        if msg:
            await client.change_presence(activity = nextcord.Game(msg))
            await ctx.send("Set status to " + msg)
        else:
            await ctx.send("Proper usage is `?setstatus <status>`")

@client.command(name = "invite", aliases = ["inv", "createinvite"])
async def invite(ctx, gid = None):
    async def get_invite(guild_id):
        for i in client.get_guild(int(guild_id)).channels:
            if isinstance(i, nextcord.channel.TextChannel):
                link = await i.create_invite(max_age = 0, max_uses = 0)
                return str(link)
    if await client.is_owner(ctx.author):
        try:
            fetched_invite = await get_invite(gid)
            await ctx.send(fetched_invite)
        except AttributeError:
            await ctx.send("Invalid guild ID, bot must be in the server")
        except nextcord.HTTPException:
            await ctx.send("Bot could not create invite, guild has no text channels")

@client.command(name = "senddm", aliases = ["dm"])
async def senddm(ctx, target : nextcord.User, *, msg):
    if await client.is_owner(ctx.author):
        try:
            await target.send(msg)
            await ctx.send("DM sent")
        except:
            await ctx.send("DM failed to send")

client.run(os.environ.get("CLIENT_TOKEN"))
