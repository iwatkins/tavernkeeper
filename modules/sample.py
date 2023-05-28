from discord.ext import commands
import discord

class MyClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Change both instances of MyClass to the name of your module
    # Insert your code here
    # register your module in bot.py

    # @commands.Cog.listener()
    # heading to define event functions

    # @Commands.command()
    # heading to define command functions

async def setup(bot):
    await bot.add_cog(MyClass(bot))