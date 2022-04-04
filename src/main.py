import os
import asyncpraw
from nextcord.ext import commands

cogs = ["cogs.img", "cogs.misc", "cogs.fun", "cogs.slash", "cogs.utility"]
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
    client.rollout_application_commands

client.run(os.environ.get("CLIENT_TOKEN"))
