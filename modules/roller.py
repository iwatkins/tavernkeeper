from discord.ext import commands
import re, random

class Roller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Roller loaded")

    #clean up the expression before processing
    def sanitize(expression):
        expression = expression.lower().replace(" ","")
        while "+-" in expression: # using +- before sanitization actually results in adding 1 to the result.  This fixes that.
            expression = expression.replace("+-","-") # don't ask why I know this is necessary
        print(f"{expression}")
        expression = expression.replace("-","+-") # preserve the negative sign in the expression
        return expression

    # check if total expression is valid
    def check(string):
        pattern = r"[^ +dkl\-0-9]" # while I could modify the roll sanitize function to replace other characters, it's useful for user feedback to know at this stage. (but only if I build the help feedback)
        matches = re.search(pattern, string)
        if matches is None:
            return True
        return False

    # check if individual rolls are valid then calc
    async def calc(string):
        pattern = r'^(?:-?)(\d*)(?:d(\d+)(?:(?:k|l)(\d+))?)?$' # validate roll
        matches = re.match(pattern, string)
        if matches is None: # exit if invalid
            print("ERROR: roll_calc failed pattern validation")
            return False
        subtract = False
        if string.startswith('-'): # determine if addition or subtraction
            subtract = True # indicate to subtract the results of this roll from the total
            string = string[1:]
        order = True # keep the highest if keeping by default
        if 'l' in string: # determine if keeping lowest before engaging regular pattern
            order = False # keep the lowest
        num_die = abs(int(matches.group(1))) if matches.group(1) else 1 # presume rolling 1 die if not specified, remove '-' captured by subtract
        print(f"num_die: {num_die}")
        if num_die > 30 and num_sides is not None:
            print("ERROR: Number of die exceeds safe limits")
            return False # exceeds safe limit, not imposed on integers
        num_sides = int(matches.group(2)) if matches.group(2) else 0
        print(f"num_sides: {num_sides}")
        if num_sides > 100:
            print("ERROR: Number of sides exceeds safe limits")
            return False # exceeds safe limit
        num_keep = int(matches.group(3)) if matches.group(3) else 0
        print(f"num_keep: {num_keep}")
        if num_keep and num_keep >= num_die:
            print("ERROR: attempting to keep all dice or more dice than rolled")
            return False # exit if trying to keep all dice or more dice than rolled
        
        # Validation complete, calculate roll value
        if num_sides == 0: # indicates that the roll is an integer, not a die roll
            if subtract:
                return -num_die
            return num_die
        results = [random.randint(1,num_sides) for _ in range(num_die)] # roll the dice
        if num_keep == 0:
            result = sum(results) # straight roll
        else:
            ordered_results = sorted(results, reverse=order) # keep highest or lowest
            result = sum(ordered_results[:num_keep])
        if subtract:
            return -result # invert the value if subtracting
        return result

    # run this if the input is invalidated at any step. Create guide later and link to it.
    async def help(): # consider contextual help messages?  Maybe v2.
        response = "Roll command not recognized. Please check your format. Guide creation pending, but if you know - you know."
        return response

    # Use '!r {expression}' or '!roll {expression}'
    @commands.command(aliases=['r'])
    async def roll(self, ctx, *, expression):
        if not Roller.check(expression): # exit early with help msg if invalid expression
            await Roller.help() # send help message, hopefully it's helpful
            print("ERROR: roll_check_exp returned False")
            return
        expression = Roller.sanitize(expression) # filter the expression before processing
        roll_array = expression.split("+") # separate rolls
        print(roll_array)
        results = []
        for dieroll in roll_array:
            result = await Roller.calc(dieroll)
            if result is False:
                await Roller.help() # send help message, hopefully it's helpful
                print("ERROR: roll_calc returned False")
                return
            results.append(result)
        response = sum(results) # just return the number, expand to indicate what you were rolling later on.
        await ctx.send(response)

    # Use '!stats {expression} {optional: number of scores, defaults to 6}', ie: '!stats 4d6k3' or '!stats 3d6 8'
    @commands.command()
    async def stats(self, ctx, *expression):
        if expression[-1].isnumeric():
            count = int(expression[-1]) # clean the count
            expression = expression[:-1] # remove count from the expression
        else:
            count = 6 # default to 6 abilities unless specified otherwise
            print("Count not detected, defaulting")
        expression = " ".join(expression)
        if not Roller.check(expression): # exit early with help msg if invalid expression
            await Roller.help() # send help message, hopefully it's helpful
            print("ERROR: roll_check_exp returned False")
            return
        expression = Roller.sanitize(expression) # filter the expression before processing, do this after count is set
        roll_array = expression.split("+") # separate rolls, who knows: may be necessary
        print(roll_array)
        response = []
        for ability in range(count):
            results = []
            for dieroll in roll_array:
                result = await Roller.calc(dieroll)
                if result is False:
                    await Roller.help() # send help message, hopefully it's helpful
                    print("ERROR: roll_calc returned False")
                    return
                results.append(result)
            ability = str(sum(results)) # just return the number, expand to indicate what you were rolling later on.
            response.append(ability)
        await ctx.send(response)

# setup the module
async def setup(bot):
    await bot.add_cog(Roller(bot))
