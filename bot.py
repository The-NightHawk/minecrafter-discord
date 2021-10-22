from os import environ
from random import choice
from datetime import timedelta

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
    command_prefix = "!",
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
    'cogs.playerdata',
    'cogs.render'
]

messages_received = 0
commands_processed = 0
bot_uptime = 0

# keep bot running by running a task constantly
@tasks.loop(seconds=30)
async def change_status():
    # change the status of the bot with a random option from statuses
    await bot.change_presence(activity=discord.Game(choice(statuses)))

@tasks.loop(seconds=10)
async def logger():
    global bot_uptime
    uptime = timedelta(seconds=bot_uptime)
    print(f"Bot Name: {bot.user}")
    print(f"Uptime: {str(uptime)}")
    print(f"Messages Received: {messages_received}")
    print(f"Commands Processed: {commands_processed}\n")
    bot_uptime += 10
    
@bot.event
async def on_message(message):
    global messages_received, commands_processed
    if message.author == bot.user:
        return
    
    messages_received += 1
    context = await bot.get_context(message)
    
    if not context.valid:
       return
    
    commands_processed += 1
    await bot.invoke(context)
    

@bot.event
async def on_ready():
    
    print(f"{bot.user} is online!")
    for ex in extensions: bot.load_extension(ex) # load cogs
    change_status.start() # start status change loop
    logger.start()

# start flask keep_alive server
#keep_alive()

# get token and run bot
token = environ.get('BOT_TOKEN')
bot.run(token)