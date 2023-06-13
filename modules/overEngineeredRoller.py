from discord.ext import commands
import discord
import modules.grammar.rollerResolver as rollerResolver


class OverEngineeredRoller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['r2'])
    async def roll2(self, ctx, *, expression):
        response = rollerResolver.run(expression)
        await ctx.send(response)


async def setup(bot):
    await bot.add_cog(OverEngineeredRoller(bot))
