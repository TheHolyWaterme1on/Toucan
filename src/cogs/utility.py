import nextcord
from nextcord.ext import commands

class utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "ping", aliases = ["pong"])
    async def ping(self, ctx):
        await ctx.send("Ping: " + (str(round(self.client.latency * 1000))) + "ms")

    @commands.command(name = "setstatus", aliases = ["status"])
    async def setstatus(self, ctx, *, msg):
        if await self.client.is_owner(ctx.author):
            await self.client.change_presence(activity = nextcord.Game(msg))
            await ctx.send("Set status to " + msg)

    @commands.command(name = "invite", aliases = ["inv", "createinvite"])
    async def invite(self, ctx, guild_id : int):
        async def get_invite(guild_id) -> str:
            for i in self.client.get_guild(int(guild_id)).channels:
                if isinstance(i, nextcord.channel.TextChannel):
                    link = await i.create_invite(max_age = 0, max_uses = 0)
                    return str(link)
        if await self.client.is_owner(ctx.author):
            try:
                fetched_invite = await get_invite(guild_id)
                await ctx.send(fetched_invite)
            except AttributeError:
                await ctx.send("Invalid guild ID, bot must be in the server")
            except nextcord.HTTPException:
                await ctx.send("Bot could not create invite, guild has no text channels")

    @commands.command(name = "senddm", aliases = ["dm"])
    async def senddm(self, ctx, target : nextcord.User, *, msg):
        if await self.client.is_owner(ctx.author):
            try:
                await target.send(msg)
                await ctx.send("DM sent")
            except:
                await ctx.send("DM failed to send")

def setup(client):
    client.add_cog(utility(client))
