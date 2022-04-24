from cogs.queries import queries as q
import re
import os
import asyncpraw
import nextcord
from nextcord.ext import commands


def get_prefix(client, message):
    try:
        prefix = q.db_get('prefixes', str(message.guild.id))[1]
    except TypeError:
        return '?'
    return prefix

command_prefix = get_prefix
intents = nextcord.Intents.default()
intents.typing = False
intents.presences = False
client = commands.Bot(command_prefix, intents = intents)
client.remove_command('help')
cogs = ["cogs.img", "cogs.misc", "cogs.fun", "cogs.utility", "cogs.moderation"]
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
            except Exception as e:
                print(f"{i} failed to load\n" + e)
        print('Online')
        client.rollout_application_commands

    @client.check
    async def block_dms(ctx):
        return ctx.guild is not None

    @client.check
    async def mod_action_permission_check(ctx):
        if ctx.cog.qualified_name == "moderation":
            if ctx.message.author.guild_permissions.administrator:
                return True
            else:
                await ctx.send("You do not have permissions to use this command")
                return False
        return True

    @client.event
    async def on_command_error(ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send('`' + '` '.join(str(err).split(' ', 1)))
        elif isinstance(err, commands.ExpectedClosingQuoteError):
            await ctx.send("Command arguments cannot contain quotation marks")
        elif isinstance(err, commands.ArgumentParsingError):
            print(err)
        elif isinstance(err, commands.CommandOnCooldown):
            await ctx.send("This command is on cooldown")
        elif isinstance(err, commands.RoleNotFound):
            await ctx.send("Invalid role")
        elif isinstance(err, commands.CheckFailure):
            # Ignore pointless errors
            pass
        else:
            raise err

    @client.command()
    async def setprefix(ctx, prefix : str):
        if re.search(r'[\'\"1-9]', prefix) is None and prefix != '':
            if len(prefix) < 5:     
                q.db_set('prefixes', str(ctx.guild.id), prefix)
                await ctx.send("Prefix has been set to: `{}`".format(prefix))
            else:
                await ctx.send("Prefix must be 4 characters or less")
        else:
            await ctx.send("Prefix cannot contain quotation marks or a number")

client.run(os.environ.get("CLIENT_TOKEN"))
