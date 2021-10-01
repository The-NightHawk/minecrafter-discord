from discord import Embed

class Embeds:
    # embed sent if no player is found
    @staticmethod
    async def no_player():
        embed = Embed(title="Player Not Found", color=0xed4245)
        embed.set_author(name="Error")
        return embed

    # embed sent when using API status command
    @staticmethod
    async def api_status(services):
        embed = Embed(title="Mojang API Status", color=0x5865f2)
        for service, status in services.items():
            embed.add_field(name=service, value=f":{status}_square:", inline=False)
            
        return embed

    # embed sent when using uuid command
    @staticmethod
    async def uuid(player):
        name, uuid, full_uuid = player.name, player.uuid, player.full_uuid
        avatar = await player.get_skin_url('avatar')
        
        embed = Embed(title="UUID", description=f"`{uuid}`\n`{full_uuid}`", color=0x5865f2)
        embed.set_author(name=name, icon_url=avatar)
        return embed

    # embed sent when using name history command
    @staticmethod
    async def name_history(player):
        name = player.name
        avatar = await player.get_skin_url('avatar')
        history = await player.get_name_history()

        embed = Embed(title="Name History", color=0x5865f2)
        embed.set_author(name=name, icon_url=avatar)
        
        embed.add_field(name="\u200b", value='\n'.join(history.keys()), inline=True)
        embed.add_field(name="\u200b", value='\n'.join(history.values()), inline=True)

        return embed

    # embed sent when using profile command
    @staticmethod
    async def playerhead(player):
        name = player.name
        head = await player.get_skin_url('head')

        command = f"`/give @p minecraft:player_head{{SkullOwner: \"{name}\"}}`"

        embed = Embed(title="", url=head, color=0x5865f2)
        embed.set_thumbnail(url=head)
        embed.add_field(
            name="Player's Head",
            value="Use this command to get this head in Minecraft:",
            inline=False)
        embed.add_field(
            name="Java Edition Only",
            value=command,
            inline=False)

        return embed

    # embed sent when using skin command
    @staticmethod
    async def skin(player, skin_url):
        name = player.name        
        avatar = await player.get_skin_url('avatar')

        embed = Embed(title=" ", url=skin_url, description=" ", color=0x5865f2)
        embed.set_author(name=name, icon_url=avatar)
        embed.set_image(url=skin_url)
        return embed

    # embed sent when using profile command
    @staticmethod
    async def profile(player):
        name, uuid, full_uuid = player.name, player.uuid, player.full_uuid
        avatar = await player.get_skin_url('avatar')
        body = await player.get_skin_url('body')
        history = await player.get_name_history()
        
        embed = Embed(
            title="Profile",
            description=f"UUID: \n`{uuid}`\n`{full_uuid}`",
            color=0x5865f2
        )

        embed.set_author(name=name, icon_url=avatar)
        embed.set_thumbnail(url=body)

        embed.add_field(name="\u200b", value='\n'.join(history.keys()), inline=True)
        embed.add_field(name="\u200b", value='\n'.join(history.values()), inline=True)

        return embed

    # embed used for general help command
    @staticmethod
    async def general_help():
        embed = Embed(title="Minecrafter Help", description="A handy bot who can show you Minecraft Skins and Profiles!", color=0x5865f2)
        embed.add_field(
            name="Command Prefix: `.`",
            value="Also supports Slash Commands!", inline=False)
        embed.add_field(
            name="Commands",
            value="`help` `ping` `status` `profile` `skin`\n `playerhead` `history` `profile`  `uuid`", inline=True)
        embed.add_field(
            name="Advanced Help:",
            value="Use `.help <command>` (Without the <angle brackets>) for detailed help.", inline=True)
        embed.set_footer(text="A bot by `Shivram S#0368`")
        
        return embed

    @staticmethod
    async def command_help(name, desc):
        embed = Embed(title="Minecrafter Help", color=0x5865f2)
        embed.add_field(name = name, value = desc, inline=False)
        embed.set_footer(text="Arguments in `<angle brackets>` are necessary. \nArguments in [square brackets] are optional. \nDo not include the bracket in the command.")
        return embed

    @staticmethod
    async def no_command(name):
        embed = Embed(title=f"{name} could not be found in the command list", color=0xed4245)
        embed.set_author(name="Error")
        return embed
