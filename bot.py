import os
import requests
from functools import lru_cache
from datetime import datetime

import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
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
        self.full_uuid = '-'.join([uuid[0:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:]])
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
                name_history[change_time] = dictionary['name']

            name_history[data[0]['name']] = 'Initial Name'
            self.name_history = name_history
        return self.name_history

    def skinURL(self, subURL: str):
        skinType = skinModes[subURL] if subURL in skinModes else skinModes['body']
        URL = f"https://crafatar.com/{skinType}/{self.uuid}?scale=10&overlay"
        return URL
    
    def profile(self):
        name_history = self.getNameHistory()
        embed = discord.Embed(title="Profile", description=f"UUID: \n`{self.uuid}`\n`{self.full_uuid}`")
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

    def id(self):
        embed = discord.Embed(title="UUID", description=f"`{self.uuid}`\n`{self.full_uuid}`")
        embed.set_author(name=self.name, icon_url=self.skinURL('avatar'))
        return embed

    def history(self):
        name_history = self.getNameHistory()
        embed = discord.Embed(title="Name History")
        embed.set_author(name=self.name, icon_url=self.skinURL('avatar'))
        embed.add_field(name="\u200b", value='\n'.join([key for key,value in name_history.items()]), inline=True)
        embed.add_field(name="\u200b", value='\n'.join([value for key,value in name_history.items()]), inline=True)
        return embed


@lru_cache(maxsize=128)
def getPlayer(player: str):
    if len(player) == 32 or len(player) == 35:
        uuid = player
        request = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names")

        if request.status_code != 200:
            return None
        else:
            name = request.json()[0]['name']
            player = Player(uuid, name)

    else:
        name = player
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
client = commands.AutoShardedBot(command_prefix = '.', intents = intents)
slash = SlashCommand(client, sync_commands=True)

missingEmbed = discord.Embed(title="Player Not Found", color=0xd50101)
missingEmbed.set_author(name="Error")

client.remove_command('help')

@slash.slash(name = "help", 
            description = "Get some help!", 
            options = []
            )
@client.command()
async def help(ctx):
    embed=discord.Embed(title="Help", description="Minecrafter is a bot which can show you a player's Profile, Skin, UUID, or Name History!")
    embed.add_field(name="**`.profile <username|UUID>`**", value="Get the profile of the player. This includes skin, name history, and UUID.", inline=True)
    embed.add_field(name="**`.skin <username|UUID> [body|head|uv|cape|avatar]`**", value="Get the skin of a player. You can choose from their head, body, avatar, cape, or skin texture.", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="**`.uuid <username|UUID>`**", value="Get the UUID of a player.", inline=True)
    embed.add_field(name="**`.history <username|UUID>`**", value="Get the name history of a player.", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="**`.ping`**", value="Get the bot's latency.", inline=True)
    embed.add_field(name="**`.status`**", value="Get the Mojang API status.", inline=True)
    embed.add_field(name="**`.invite`**", value="Get the bot's invite link!", inline=True)
    embed.set_footer(text="A bot by TheNightHawk#5516")
    await ctx.send(embed=embed)

@slash.slash(name="profile", 
            description="Get the profile of a player", 
            options = [
                create_option(
                    name = "player",
                    description = "The Name or UUID of the player",
                    option_type= 3,
                    required = True
                )
            ]
            )
@client.command()
async def profile(ctx, player:str):
    player = getPlayer(player)
    if not player:
        await ctx.send(embed = missingEmbed)
    else:
        await ctx.send(embed = player.profile())

@slash.slash(name="skin", 
            description="Get the skin of a player", 
            options = [
                create_option(
                    name = "player",
                    description = "The Name or UUID of the player",
                    option_type= 3,
                    required = True
                ), 
                create_option(
                    name = "skin_type", 
                    description = "The type of player skin to get.",
                    option_type = 3,
                    required = False,
                    choices = [
                        create_choice(
                            name="body", 
                            value = "head"
                        ), 
                        create_choice(
                            name="body", 
                            value = "body"
                        ), 
                        create_choice(
                            name="uv", 
                            value = "uv"
                        ), 
                        create_choice(
                            name="cape", 
                            value = "cape"
                        ), 
                        create_choice(
                            name="avatar", 
                            value = "avatar"
                        )
                    ]
                )
            ]
            )
@client.command()
async def skin(ctx, player: str, skin_type: str = 'body'):
        player = getPlayer(player)
        if not player:
            await ctx.send(embed = missingEmbed)
        else:
            await ctx.send(embed = player.skin(skin_type))

@slash.slash(name="uuid", 
            description="Get the uuid of a player", 
            options = [
                create_option(
                    name = "player",
                    description = "The Name or UUID of the player",
                    option_type= 3,
                    required = True
                )
            ]
            )
@client.command()
async def uuid(ctx, player: str):
        player = getPlayer(player)
        if not player:
            await ctx.send(embed = missingEmbed)
        else:
            await ctx.send(embed = player.id())


@slash.slash(name="history", 
            description="Get the name history of a player", 
            options = [
                create_option(
                    name = "player",
                    description = "The Name or UUID of the player",
                    option_type= 3,
                    required = True
                )
            ]
            )
@client.command()
async def history(ctx, player: str):
        player = getPlayer(player)
        if not player:
            await ctx.send(embed = missingEmbed)
        else:
            await ctx.send(embed = player.history())

@slash.slash(name = "status", 
            description = "Get the latency of the bot.", 
            options = []
            )
@client.command()
async def status(ctx):
    r = requests.get("https://status.mojang.com/check")
    embed = discord.Embed(title="Mojang API Status")
    result = {}
    for d in r.json():
        result.update(d)

    for x, y in result.items():
        embed.add_field(name=x, value=f":{y}_square:", inline=False)
    await ctx.send(embed=embed)

@slash.slash(name = "clearcache", 
            description = "Clear the bot cache.", 
            options = []
            )
@client.command()
async def clearcache(ctx):
    getPlayer.cache_clear()
    await ctx.send("Cache Cleared!")

@slash.slash(name = "ping", 
            description = "Get the latency of the bot.", 
            options = []
            )
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! in {round(client.latency * 1000)}ms")

@slash.slash(name = "invite", 
            description = "Get an invite link for the bot!", 
            options = [] 
            )
@client.command()
async def invite(ctx):
    await ctx.send("Here's the invite link: https://discord.com/api/oauth2/authorize?client_id=781349890944270366&permissions=2147503104&scope=bot%20applications.commands")

client.run(token)
