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

# load all modules - will load all .py scripts in the selected folder as a module.  Use Cog formats
async def load():
    module_folder = 'modules' # set your modules folder name here
    for filename in os.listdir(module_folder):
        if filename.endswith('.py') and filename != 'sample.py': # ignore the sample plugin
            module_name = filename[:-3] # remove .py from file_name
            module_path = f'{module_folder}.{module_name}'
            try:
                await bot.load_extension(module_path)
                print(f'Successfully loaded module: {module_name}')
            except Exception as e:
                print(f'Failed to load module {module_name}: {str(e)}')

async def main():
    await load()
    await bot.start(config['discord_token'])

asyncio.run(main())