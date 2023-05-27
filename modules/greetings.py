from discord.ext import commands
import random, discord

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Greetings loaded")

    greetings_list = [
        "Welcome to {server}, {user}! May the dice be in your favor!",
        "Welcome to {server}, {user}! Now with fewer mimics!",
        "Hello {user}! Welcome to {server}!",
        "{user}, Roll for Initiative!\nNatural 20! Welcome to {server}!",
        "Welcome to {server}, {user}! Did you prepare 'Remove Curse' by chance?",
        "Roll stealth. Natural 1?\nEveryone in {server} notices {user} enter the room.\nRoll for initiative!"
    ]

    async def send_welcome_message(self, channel, member):
        if channel is None:
            return
        greeting = random.choice(Greetings.greetings_list).format(server=member.guild.name, user=member.mention)
        embed = discord.Embed(description=greeting, color=discord.Color.green())
        embed.set_author(name="Welcome Message", icon_url=self.bot.user.avatar.url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        await Greetings.send_welcome_message(self, channel, member)

    @commands.command()
    async def test_greeting(self, ctx):
        channel = ctx.channel
        if "bot" in channel.name.lower():
            member = ctx.author
            await Greetings.send_welcome_message(self, channel, member)
        else:
            ctx.send("That can't be used here.")

async def setup(bot):
    await bot.add_cog(Greetings(bot))