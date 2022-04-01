import nextcord
from nextcord.ext import commands
from nextcord import Embed
import random, re, aiohttp

class misc(commands.Cog): 
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clean(self, ctx, amount = 5):
        if int(amount) < 100:
            await ctx.channel.purge(limit = int(amount) + 1)
            await ctx.send("Purged `" + str(amount) + "` messages", delete_after = 3)
        else:
            await ctx.send("Amount must be smaller than 100")

    @commands.command()
    async def avatar(self, ctx, *,  target : nextcord.User = None):
        if target:
            await ctx.send(target.display_avatar)
        else:
            await ctx.send(ctx.message.author.display_avatar)

    @commands.command()
    async def poll(self, ctx, *args):
        if len(args) < 10 and len(args) > 2:
            react = {
                0 : "1️⃣", 1 : "2️⃣", 2 : "3️⃣", 3 : "4️⃣", 4 : "5️⃣", 5 : "6️⃣", 6 : "7️⃣", 7 : "8️⃣", 8 : "9️⃣",
            }
            args = list(args); q = args[0]; del args[0]
            desc = ""
            for i in range(len(args)):
                desc = desc + "\n" + react[i] + " " + args[i]
            embed = Embed(title = "**" + q + "**", description = desc, color = 0xfffb00).set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar)
            message = await ctx.send(embed = embed)
            for i in range(len(args)):
                await message.add_reaction(react[i])
        else:
            await ctx.send("Proper usage is `?poll <question> <args (maximum of 10)>`")

    @commands.command()
    async def reddit(self, ctx, sub = None):
        reddit = self.client.reddit
        if sub:
            try:
                get_sub = await reddit.subreddit(sub); rand = await get_sub.random()
                try: rand.url
                except:
                    l = []
                    async for i in get_sub.hot(limit = 50): l.append(i); rand = random.choice(l)
            except:
                await ctx.send("`" + sub + "` is not a valid subreddit")
            else:
                description = "[Post](" + rand.url + ") from r/" + sub
                if hasattr(rand, "post_hint") and ('video' in rand.post_hint): 
                    await ctx.send(rand.title + ":\n" + rand.url)
                else:
                    if rand.selftext: 
                        description = description + "\n" + rand.selftext
                    try:
                        embed = Embed(title = rand.title, description = description, color = nextcord.Color.yellow())
                        if re.search("\.(png|jpg|gif)", rand.url): embed.set_image(url = rand.url)
                        await ctx.send(embed = embed)
                    except:
                        await ctx.send("Something went wrong with this post, please try again")
        else:
            await ctx.send("Proper usage is `?reddit <subreddit>`")

    @commands.command(name = "roman", aliases = ["rn", "romannumeral"])
    async def roman(self, ctx, inp):
        conv = {
            "i" : 1, "v" : 5, "x" : 10, "l" : 50, "c" : 100, "d" : 500, "m" : 1000
        }
        num = 0; tl = inp.lower()
        if not re.search('i{4}|v{4}|x{4}|l{4}|c{4}|d{4}|m{4}', tl):
            try:
                for i in range(0, len(tl)):
                    char = tl[i]
                    if i > 0 and conv[char] > conv[tl[i - 1]]:
                        num += conv[char] - 2*conv[tl[i - 1]]
                    else:
                        num += conv[char]
                if num > 4000:
                    raise Exception
                await ctx.send("Equals: `" + str(num) + "`")
            except:
                await ctx.send("Error: `" + inp + "` is not a valid numeral")
        else:
            await ctx.send("`" + inp + "` is not a valid numeral")

    @commands.command(name = "country", aliases = ["getcountry", "co"] )
    async def country(self, ctx, inp = None):
        if inp:
            async with aiohttp.ClientSession() as s:
                get = await s.get('https://restcountries.com/v3.1/name/' + inp.lower()); fj = await get.json(); 
                try:
                    fj = fj[0]
                    embed = Embed(title = fj["name"]["official"], description = "[Flag](" + fj["flags"]["png"] + ") | [Coat of Arms](" + fj["coatOfArms"]["png"] + ") | [Google Maps](" + fj["maps"]["googleMaps"] + ")"
                    ).add_field(name = "Capital", value = fj["capital"][0]
                    ).add_field(name = "Continent", value = fj["continents"][0]
                    ).add_field(name = "Currency", value = fj["currencies"][list(fj["currencies"])[0]]["name"]
                    ).add_field(name = "Symbol", value = "`" + fj["cca2"] + "`"
                    ).add_field(name = "Population", value = "`" + "{:,}".format(fj["population"]) + "`"
                    ).add_field(name = "URL Extension", value = "`" + fj["tld"][0] + "`"
                    ).add_field(name = "GINI", value = "`" + str(fj["gini"][list(fj["gini"])[-1]]) + "%`"
                    ).add_field(name = "Postal Code", value = "`" + fj["postalCode"]["format"] + "`"
                    ).add_field(name = "Is UN Member:", value = str(fj["unMember"])
                    ).set_thumbnail(url = fj["flags"]["png"]).set_footer(text = "Demonyms: Male: " + fj["demonyms"]["eng"]["m"] + " | Female: " + fj["demonyms"]["eng"]["f"])
                    await ctx.send(embed = embed)
                except:
                    await ctx.send("Something went wrong, make sure you spelled the country name correctly.\nDue to API issues, some countries are unavailable.")
        else:
            await ctx.send("Proper usage is `?country <country name>`")
        
def setup(client):
    client.add_cog(misc(client))