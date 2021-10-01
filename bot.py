from os import environ
from random import choice

import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand

from keep_alive import keep_alive

__author__ = "Shivram S"

__license__ = "GNU GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Shivram S"
__email__ = "shivrams.2006@gmail.com"
__status__ = "Production"

# creates the bot, with default intents.
# custom help command will be added in cogs.utility
bot = commands.Bot(
    command_prefix = ".",
    intents = discord.Intents.default(),
    help_command = None
)

# for slashcommand support
slash = SlashCommand(bot)

statuses = [
    "with the Mojang API",
    "with Minecraft Skins",
    "with Minecraft Profiles",
    "with Crafatar",
    "with other Bots",
    "with the Internet",
    "with Slash Commands. Type / to get started!"
]

extensions = [
    'cogs.utility',
    'cogs.playerdata'
]

# keep bot running by running a task constantly
@tasks.loop(seconds=30)
async def change_status():
    # change the status of the bot with a random option from statuses
    await bot.change_presence(activity=discord.Game(choice(statuses)))

@bot.event
async def on_ready():
    print(bot.user, " is online!")
    for ex in extensions: bot.load_extension(ex) # load cogs
    change_status.start() # start status change loop

# start flask keep_alive server
keep_alive()

# get token and run bot
token = environ.get('BOT_TOKEN')
bot.run(token)