import discord, json, os, asyncio
from discord.ext import commands

#load configs
with open('bot_config.json') as config_file:
    config = json.load(config_file)

# declare intents and init commands
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True
intents.dm_messages = True
intents.guild_messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Gotta log logins, ya know?
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

# load all modules
async def load():
    # for filename in os.listdir(f'./modules'): #this is killing asyncio and the initialization
    #     if filename.endswith('py'):
    #         bot.load_extension(f'modules.{filename[:-3]}')
    await bot.load_extension('modules.greetings')
    await bot.load_extension('modules.roller')
    await bot.load_extension('modules.codex')

async def main():
    await load()
    await bot.start(config['discord_token'])

asyncio.run(main())