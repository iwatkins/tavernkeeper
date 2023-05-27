from discord.ext import commands
import discord, requests, json

# using dnd5eapi.co
class Codex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Codex loaded")

    def filter(expression):
        expression = expression.lower().replace(" ","-") # match RESTapi format
        return expression
    
    def spell_format(self, data):
        
        print("build variables")
        # build variables
        level = data['level']
        print("built level")
        desc = str(data['desc'])[2:-2]
        print("built desc")
        higher_level = str(data['higher_level'])[1:-1]
        print("built higher_level")
        range = data['range']
        print("built range")
        components = str(data['components'])[1:-1].replace("'","")
        print("built components")
        material = data['material'] if 'material' in data else None
        print("built material")
        ritual = data['ritual']
        print("built ritual")
        casting_time = data['casting_time']
        print("built casting_time")
        concentration = data['concentration']
        print("built concentration")
        duration = data['duration']
        print("built duration")
        school = data['school']['name']
        print("built school")
        classes = str([class_data['name'] for class_data in data['classes']])[1:-1].replace("'","")
        print("built classes")
        subclasses = str([subclass_data['name'] for subclass_data in data['subclasses']])[1:-1].replace("'","")
        print("built subclasses")
        print("built all")

        print("construct string")
        # construct string
        string = ""
        string += f"*Level {level} {school}: "
        string += f"{classes}"
        if len(subclasses) > 0:
            string += f", {subclasses}"
        string +="*\n\n"
        string += f"**Casting time:** {casting_time} "
        if len(range) > 0:
            string += f"\n**Range:** {range} "
        if len(duration) > 0:
            string += f"\n**Duration:** {duration} "
        string += "\n"
        string += f"**Components:** {components} "
        if material is not None:
            string += f"  **Material:** {material} "
        if concentration is True:
            string += "\n**Concentration** "
        if ritual is True:
            string += "\n**Ritual** "
        string += "\n\n"
        string += f"**Description:** {desc} "
        if len(higher_level) > 0:
            string += "\n\n"
            string += f"**At higher levels:** {higher_level} "
        print(string)
        return string

    @commands.command(aliases=['spell'])
    async def spells(self, ctx, *, expression):
        expression = Codex.filter(expression)
        url = f"https://www.dnd5eapi.co/api/spells/{expression}"
        print(f"attempt fetching spell from: {url}")
        response = requests.get(url, headers={'Accept': 'application/json'})
        print(response)
        data = response.json()
        if 'error' in data:
            await ctx.channel.send(f"Unable to find spell {expression}. Check your 'spelling'?")
            return
        # print(data)
        message = Codex.spell_format(self, data)
        print("post-message")
        embed = discord.Embed(description=message, title=data['name'], color=discord.Color.blue())
        embed.set_author(name="Spell Card", icon_url=self.bot.user.avatar.url)
        await ctx.channel.send(embed=embed)

# To Do
# /conditions/{condition}
# /classes/{class}/levels/{level}
# /subclasses/{subclass}/levels/{level}
# /equipment/{item}
# /feats/{feats}
# /magic-items/{item}
# /rules/{rules}
# /rule-sections/{rules}

async def setup(bot):
    await bot.add_cog(Codex(bot))