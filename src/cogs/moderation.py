from main import q
import nextcord
from nextcord.ext import commands

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "setmuterole", aliases = ["muterole"])
    async def setmuterole(self, ctx, role : nextcord.Role):
        if ctx.guild.get_role(role.id) is not None and role.managed == False:
            q.db_set("mutedRoles", str(ctx.guild.id), str(role.id))
            await ctx.send("Mute role set as <@&{}>".format(role.id))

    @commands.command()
    async def mute(self, ctx, user : nextcord.User):
        r = q.db_get('mutedRoles', str(ctx.guild.id))
        if r is not None:
            m = await ctx.guild.fetch_member(user.id)
            if m is not None:
                await m.add_roles(ctx.guild.get_role(r[1]))
            else:
                await ctx.send("User not in server")
        else:
            await ctx.send("No muted role set")

def setup(client):
    client.add_cog(moderation(client))
