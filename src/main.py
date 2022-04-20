import os
import asyncpraw
import nextcord
from nextcord.ext import commands

COMMAND_PREFIX = '?'
client = commands.Bot(COMMAND_PREFIX)
client.remove_command('help')
cogs = ["cogs.img", "cogs.misc", "cogs.fun", "cogs.utility"]
reddit_data = os.environ.get("REDDIT_API_DATA").split(",")
client.reddit = asyncpraw.Reddit(
    client_id = reddit_data[0],
    client_secret = reddit_data[1],
    username = reddit_data[2],
    password = reddit_data[3],
    user_agent = reddit_data[4]
)

class Toucan(commands.Bot):
    def __init__(self):
        allowed_mentions = nextcord.AllowedMentions(roles = True, everyone = False, users = True)
        super().__init__(
            allowed_mentions = allowed_mentions
        )

    client.load_extension("cogs.slash")
    print("Initialised slash commands")

    @client.event
    async def on_ready():
        for i in cogs:
            try: 
                client.load_extension(i)
                print(f"Initialised cog: {i}")
            except:
                print(f"{i} failed to load")
        print('Online')
        client.rollout_application_commands
        uptime = nextcord.utils.utcnow()

    @client.check
    async def block_dms(ctx):
        return ctx.guild is not None

    @client.event
    async def on_command_error(ctx, err):
        if isinstance(err, commands.ArgumentParsingError) or isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(err)
        if isinstance(err, commands.CommandOnCooldown):
            await ctx.send("This command is on cooldown")
        else:
            print(err)

client.run(os.environ.get("CLIENT_TOKEN"))
