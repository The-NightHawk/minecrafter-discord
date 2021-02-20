import discord
from discord.ext import commands

from mcuuid.tools import is_valid_minecraft_username

token = 'Insert Token Here'

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '.', intents = intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Minecraft Skins'))

client.remove_command('help')
@client.command()
async def help(ctx):
    embed=discord.Embed(title="Help", description="Minecraft Skins is a bot which can show you a specific player's skin based on their username")
    embed.add_field(name=".skin <username/UUID>", value="Use this command to find the skin of a\n specific player. You can use UUIDs too!", inline=True)
    embed.add_field(name=".help", value="Shows this command", inline=True)
    embed.set_footer(text="A bot by TheNightHawk#5516")
    await ctx.send(embed=embed)

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