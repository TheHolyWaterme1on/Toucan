import nextcord
from nextcord import Interaction, Embed
from nextcord.ext import commands
import aiohttp
import re
import random

class slash(commands.Cog):
    ids = [766423223595696198, 921103309526433843, 701127612243902504, 959517813586923590]
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name = "ping", description = "Sends ping", guild_ids = ids)
    async def ping(self, interaction : Interaction):
        await interaction.response.send_message("Ping: " + (str(round(self.client.latency * 1000))) + "ms")

    @nextcord.slash_command(name = "prefix", description = "Sends bot prefix", guild_ids = ids)
    async def prefix(self, interaction : Interaction):
        await interaction.response.send_message("The bot's prefix is `?`")

    @nextcord.slash_command(name = "country", description = "Sends data about a country", guild_ids = ids)
    async def country(self, interaction : Interaction, inp = None):
        async with aiohttp.ClientSession() as s:
            get = await s.get('https://restcountries.com/v3.1/name/' + inp.lower()); fj = await get.json()
            try:
                fj = fj[0]
                await interaction.response.send_message(embed = 
                    Embed(title = fj["name"]["official"], description = "[Flag](" + fj["flags"]["png"] + ") | [Coat of Arms](" + fj["coatOfArms"]["png"] + ") | [Google Maps](" + fj["maps"]["googleMaps"] + ")"
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
                )
            except:
                await interaction.response.send_message("Something went wrong, make sure you spelled the country name correctly.\nDue to API issues, some countries are unavailable.")

    @nextcord.slash_command(name = "joe", description = "...", guild_ids = ids)
    async def joe(self, interaction : Interaction, target : nextcord.User):
        async def get(self = self):
            reddit = self.client.reddit; get_sub = await reddit.subreddit("copypasta"); rand = None
            while rand == None:
                try: 
                    rand = await get_sub.random()
                except Exception:
                    continue
            return Embed(title = rand.title, description = rand.selftext, color = nextcord.Color.random())
        try: 
            await target.send(embed = await get())
            await interaction.response.send_message("Message sent")
        except:
            await interaction.response.send_message("Message failed to send, target might have their DMs closed.")
            
    @nextcord.slash_command(name = "roman", description = "Converts Roman numerals to integers", guild_ids = ids)
    async def roman(self, interaction : Interaction, numeral : str):
        conv = {
            "i" : 1, "v" : 5, "x" : 10, "l" : 50, "c" : 100, "d" : 500, "m" : 1000
        }
        num = 0; tl = numeral.lower()
        if not re.search('(?=(.)\1{3})[ivxlcdm]{4}', tl):
            try:
                for i in range(0, len(tl)):
                    char = tl[i]
                    if i > 0 and conv[char] > conv[tl[i - 1]]:
                        num += conv[char] - 2*conv[tl[i - 1]]
                    else:
                        num += conv[char]
                if num > 4000:
                    raise BaseException
                await interaction.response.send_message("Equals: `" + str(num) + "`")
            except:
                await interaction.response.send_message("Error: `" + numeral + "` is not a valid numeral")
        else:
            await interaction.response.send_message("`" + numeral + "` is not a valid numeral")
            
    @nextcord.slash_command(name = "reddit", description = "Gets a random post from a subreddit", guild_ids = ids)
    async def reddit(self, interaction : Interaction,  sub = nextcord.SlashOption(name = "subreddit", description = "Subreddit name", required = True)):
        reddit = self.client.reddit
        try:
            get_sub = await reddit.subreddit(sub); rand = await get_sub.random()
            try: rand.url
            except:
                l = []
                async for i in get_sub.hot(limit = 50): l.append(i); rand = random.choice(l)
        except:
            await interaction.response.send_message("`" + sub + "` is not a valid subreddit")
        else:
            description = "[Post](" + rand.url + ") from r/" + sub
            if hasattr(rand, "post_hint") and ('video' in rand.post_hint): 
                await interaction.response.send_message(rand.title + ":\n" + rand.url)
            else:
                if rand.selftext: description = description + "\n" + rand.selftext
                try:
                    embed = Embed(title = rand.title, description = description, color = nextcord.Color.yellow())
                    if re.search("\\.(png|jpg|gif)", rand.url): embed.set_image(url = rand.url)
                    await interaction.response.send_message(embed = embed)
                except:
                    await interaction.response.send_message("Something went wrong with this post, please try again")
                      
    @nextcord.slash_command(name = "xkcd", description = "Sends an XKCD comic", guild_ids = ids)
    async def xkcd(self, interaction : Interaction, num = nextcord.SlashOption(name = "num", description = "Comic number", required = False, default = 0)):
        async with aiohttp.ClientSession() as s:
            if not num:
                num = random.randint(0, 2000)
        try:
            get = await s.get("https://xkcd.com/" + str(num) + "/info.0.json")
            j = await get.json()
            embed = Embed(title = "XKCD Number " + str(num) + ": " + j["title"]).set_image(url = j["img"])
            await interaction.response.send_message(embed = embed)
        except commands.errors.BadArgument:
            await interaction.response.send_message("Proper usage is `?xkcd <comic number>`")
        except aiohttp.ContentTypeError:
            await interaction.response.send_message("Invalid comic number")

def setup(client):
    client.add_cog(slash(client))
