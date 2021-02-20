import discord
from discord.ext import commands

from mcuuid.tools import is_valid_minecraft_username

token = 'Your Token Here'

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '.', intents = intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Minecraft Skins'))

@client.command()
async def skin(ctx, name):
    valid = is_valid_minecraft_username(name)

    if valid is False:
        await ctx.send("The Player you are looking for doesn't exist")
    
    else:
        embed=discord.Embed(title=" ", url=f"https://mc-heads.net/body/{name}", description=" ")
        embed.set_author(name=name, icon_url=f"https://www.mc-heads.net/avatar/{name}")
        embed.set_image(url=f"https://mc-heads.net/body/{name}")
        
        await ctx.send(embed=embed)

client.run(token)