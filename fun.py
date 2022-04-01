import nextcord
from nextcord.ext import commands
from nextcord import Embed
import random, aiohttp

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def say(self, ctx, *, msg = None):
        if msg:
            await ctx.message.delete()
            await ctx.send(msg)
        else:
            await ctx.send("Proper usage is `?say <message>`")
    
    @commands.command(name = "dice", aliases = ["roll"])
    async def dice(self, ctx, num : int = 6):
        await ctx.send("You rolled a `" + str(random.randint(1,num)) + "`")
    
    @commands.command(name = "meme", aliases = ["memes"])
    async def meme(self, ctx):
        reddit = self.client.reddit
        get_sub = await reddit.subreddit("memes"); rand = await get_sub.random()
        embed = Embed(title = rand.title,  description = "[Post URL](" + rand.url + ")", color = nextcord.Color.yellow()).set_image(url = rand.url
        ).set_footer(text = "Score: " + str(rand.score) + " | Upvote ratio: " + str(int(rand.upvote_ratio * 100)) + "% | Number of comments: " + str(rand.num_comments))
        if hasattr(rand, "post_hint") and ('video' in rand.post_hint):
            await ctx.send(rand.title + ":\n" + rand.url)
        else:
            await ctx.send(embed = embed)

    # @commands.command()
    # async def flag(self, ctx):
    #     async with aiohttp.ClientSession() as s:
    #         get = await s.get('https://flagcdn.com/en/codes.json'); fj = await get.json()
    #         x = random.choice(list(fj))
    #         await ctx.send(embed = Embed(title = "Which territory's flag is this?").set_image(url = "https://flagcdn.com/w320/" + x + ".png"))
    #         def c(m):
    #             return m.author.id == ctx.author.id
    #         fj = await get.json()
    #         def checkAnswer(m):
    #              for i in fj:
    #                 if re.search("(?i)" + fj[i] + "$", m.content):
    #                     return i, fj[i]
    #         msg = await self.client.wait_for("message", check = c)
    #         if re.search("(?i)" + fj[x] + "$", msg.content):
    #             await ctx.send("That is correct!")
    #         else:
    #             if checkAnswer(msg):
    #                 a,b = checkAnswer(msg)
    #                 await ctx.send(embed = Embed(title = "That is incorrect", description = "The correct answer was `" + fj[x] +"`, the flag of " + b + " is: "
    #                 ).set_image(url = "https://flagcdn.com/w320/" + a + ".png"))
    #             else:
    #                 await ctx.send("That is incorrect, the answer is `" + fj[x] + "`")

    @commands.command()
    async def joe(self, ctx, target : nextcord.User = None):
        async def get(self = self):
            reddit = self.client.reddit; get_sub = await reddit.subreddit("copypasta"); rand = await get_sub.random()
            return Embed(title = rand.title, description = rand.selftext, color = nextcord.Color.random())
        if not target:
            target = ctx.message.author
        embed = None
        while embed == None:
            try: 
                embed = await get()
            except:
                continue
        try: 
            await target.send(embed = embed)
            await ctx.send("Message sent")
        except:
            await ctx.send("Message failed to send, target might have their DMs closed.")

    @commands.command()
    async def xkcd(self, ctx, num = random.randint(0, 2000)):
        async with aiohttp.ClientSession() as s:
            get = await s.get("https://xkcd.com/" + str(num) + "/info.0.json"); 
        try:
            j = await get.json()
            embed = Embed(title = "XKCD Number " + str(num) + ": " + j["title"]).set_image(url = j["img"])
            await ctx.send(embed = embed)
        except:
            await ctx.send("Invalid comic number")

def setup(client):
    client.add_cog(fun(client))