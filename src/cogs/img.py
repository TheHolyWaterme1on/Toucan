from nextcord.ext import commands
from nextcord import Embed
import random
import aiohttp

class img(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    async def fetch(link):
        async with aiohttp.ClientSession() as s:
            get = await s.get(link); return await get.json()
            
    def createEmbed(animal, image):
        return Embed(title = "Here is your " + animal + " picture:", color = random.randint(0, pow(16, 6))).set_image(url = image)
    
    @commands.command()
    async def david(self, ctx):
        embed = Embed(title = "David", color = random.randint(0, pow(16, 6))
        ).set_image(url = 'https://cdn.discordapp.com/attachments/802681841864802355/802689768755953704/20210122_175225.jpg')
        await ctx.send(embed = embed)

    @commands.command(name = "dog", aliases = ["dogs", "doggo"])
    async def dog(self, ctx):
        dog = await img.fetch('https://dog.ceo/api/breeds/image/random')
        await ctx.send(embed = img.createEmbed("dog", dog['message']))

    @commands.command(name = "cat", aliases = ["meow", "cats"])
    async def cat(self, ctx):
        cat = await img.fetch('https://api.thecatapi.com/v1/images/search')
        await ctx.send(embed = img.createEmbed('cat', cat[0]['url']))

    @commands.command(name = "duck", aliases = ["quack", "ducks", "ducc"])
    async def duck(self, ctx):
        duck = await img.fetch('https://random-d.uk/api/v2/random')
        await ctx.send(embed = img.createEmbed('duck', duck['url']))

def setup(client):
    client.add_cog(img(client))
