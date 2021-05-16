import asyncio
import os
import requests

import discord
from discord.ext import commands
from requests.api import get

token = os.environ['BOT_TOKEN']

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '.', intents = intents)

skinModes = {
    'head': 'renders/head',
    'body': 'renders/body',
    'uv': 'skins',
    'cape': 'cape',
    'avatar': 'avatar'
}

async def getUUID(name):
    r = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{name}')
    if r.status_code == 204:
        return None
    r = r.json()
    uuid = r['id']
    return uuid

async def skinCheck(uuid, subURL):
    r = requests.get(f"https://crafatar.com/{subURL}/{uuid}")
    if r.status_code == 200:
        return True
    else:
        return False

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Minecraft Skins'))

client.remove_command('help')
@client.command()
async def help(ctx):
    embed=discord.Embed(title="Help", description="Minecraft Skins is a bot which can show you a specific player's skin based on their username")
    embed.add_field(name=".skin <username/UUID> [body|head|uv|cape|avatar]", value="Use this command to find the skin of a\n specific player. You can use UUIDs too!", inline=True)
    embed.add_field(name=".help", value="Shows this command", inline=True)
    embed.set_footer(text="A bot by TheNightHawk#5516")
    await ctx.send(embed=embed)

@client.command()
async def skin(ctx, name: str, mode: str = 'body'):

    async with ctx.typing():
        await asyncio.sleep(3)

    mode = mode.lower()
    if mode not in skinModes:
        mode = 'body'

    subURL = skinModes[mode]

    UUID = await getUUID(name)
    if not UUID:
        await ctx.send("The player you are looking for does not exist.")
        return

    if not await skinCheck(UUID, subURL):
        await ctx.send("Could not retrieve skin.")
        return

    embed=discord.Embed(title=" ", url=f"https://crafatar.com/{subURL}/{UUID}?overlay", description=" ")
    embed.set_author(name=name, icon_url=f"https://crafatar.com/avatars/{UUID}")
    embed.set_image(url=f"https://crafatar.com/{subURL}/{UUID}?overlay")
        
    await ctx.send(embed=embed)

client.run(token)