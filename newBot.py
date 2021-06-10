import asyncio
import os
import requests
from functools import lru_cache
from datetime import datetime
from mcstatus import MinecraftServer
from binascii import a2b_base64
from io import BytesIO

import discord
from discord.ext import commands
import requests

skinModes = {
    'head': 'renders/head',
    'body': 'renders/body',
    'uv': 'skins',
    'cape': 'capes',
    'avatar': 'avatars'
}

class Player:
    def __init__(self, uuid:str, name:str):
        self.uuid = uuid
        self.name = name

    def getNameHistory(self):
        request = requests.get(f"https://api.mojang.com/user/profiles/{self.uuid}/names")
        if request.status_code != 200:
            self.name_history = None
        else:
            data = request.json()
            name_history = {}

            for dictionary in data[1:][::-1]:
                dt_object = datetime.fromtimestamp(int(dictionary['changedToAt'])/1000)
                change_time = dt_object.strftime("%d-%m-%y")
                name_history[dictionary['name']] = change_time

            name_history[data[0]['name']] = 'Initial Name'
            self.name_history = name_history
        return self.name_history

    def skinURL(self, subURL: str):
        skinType = skinModes[subURL] if subURL in skinModes else skinModes['body']
        URL = f"https://crafatar.com/{skinType}/{self.uuid}?overlay"
        return URL
    
    def profile(self):
        name_history = self.getNameHistory()
        embed = discord.Embed(title="Profile", description=f"UUID: `{self.uuid}`")
        embed.set_author(name=self.name, icon_url=self.skinURL('avatar'))
        embed.set_thumbnail(url=self.skinURL('body'))
        
        if name_history:
            embed.add_field(name="Name History", value='\n'.join([key for key,value in name_history.items()]), inline=True)
            embed.add_field(name="\u200b", value='\n'.join([value for key,value in name_history.items()]), inline=True)

        return embed

    def skin(self, subURL: str = None):
        embed=discord.Embed(title=" ", url=self.skinURL(subURL), description=" ")
        embed.set_author(name=self.name, icon_url=self.skinURL('avatar'))
        embed.set_image(url=self.skinURL(subURL))
        return embed

@lru_cache(maxsize=64)
def getPlayer(name_or_uuid: str):
    if len(name_or_uuid) == 32 or len(name_or_uuid) == 35:
        uuid = name_or_uuid
        request = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names")

        if request.status_code != 200:
            return None
        else:
            name = request.json()['name']
            player = Player(uuid, name)

    else:
        name = name_or_uuid
        request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
        if request.status_code != 200:
            return None
        else:
            uuid = request.json()['id']
            name = request.json()['name']
            player = Player(uuid, name)
    
    return player
        
token = os.environ['BOT_TOKEN']

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '.', intents = intents)

missingEmbed = discord.Embed(title="Player Not Found", color=0xd50101)
missingEmbed.set_author(name="Error")

@client.command()
async def profile(ctx, name_or_uuid:str):
    player = getPlayer(name_or_uuid)
    if not player:
        await ctx.send(embed = missingEmbed)
    else:
        await ctx.send(embed = player.profile())

@client.command()
async def skin(ctx, name_or_uuid: str, subURL: str = 'body'):
    player = getPlayer(name_or_uuid)
    if not player:
        await ctx.send(embed = missingEmbed)
    else:
        await ctx.send(embed = player.skin(subURL))

@client.command()
async def server(ctx):
    server = MinecraftServer('thehawksmp.aternos.me')
    status = server.status()
    if status.favicon:
        favicon = a2b_base64(status.favicon.split(',')[1])
    await ctx.send("HI", file=discord.File(BytesIO(favicon), filename='icon.png'))

client.run(token)