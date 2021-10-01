from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

from cogs.shared import get_player
from cogs.embeds import Embeds

class PlayerData(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def uuid(self, ctx, id: str):
        """
        Usage: `.uuid <id>`
        id: Username or UUID of the player

        Get the UUID of a player!
        """
        player = await get_player(id)

        if not player:
            await ctx.send(embed = await Embeds.no_player())
            return

        await ctx.send(embed = await Embeds.uuid(player))


    @commands.command()
    async def history(self, ctx, id: str):
        """
        Usage: `.history <id>`
        id: Username or UUID of the player

        Get the name history of a player!
        """
        player = await get_player(id)

        if not player:
            await ctx.send(embed = await Embeds.no_player())
            return
        
        await ctx.send(embed = await Embeds.name_history(player))
            

    @commands.command()
    async def playerhead(self, ctx, id: str):
        """
        Usage: `.playerhead <id>`
        id: Username or UUID of the player

        Get the head of a player as an item!
        """
        player = await get_player(id)

        if not player:
            await ctx.send(embed = await Embeds.no_player())
            return
        
        await ctx.send(embed = await Embeds.playerhead(player))

   
    @commands.command()
    async def skin(self, ctx, id: str, skin_type: str = 'body'):
        """
        Usage: `.skin <id> [skin_type]`
        `id`: Username or UUID of the player
        `skin_type`: The type of skin to get (
            `body`: A full body image of the player
            `head`: An image of the player's head
            `uv`: The player's skin texture
            `cape`: The cape of the player
            `avatar`: The player's avatar (head)
        )

        Get the skin of a player!
        """
        player = await get_player(id)

        if not player:
            await ctx.send(embed = await Embeds.no_player())
            return
        
        skin_url = await player.get_skin_url(skin_type)

        await ctx.send(embed = await Embeds.skin(player, skin_url))

    
    @commands.command()
    async def profile(self, ctx, id: str):
        """
        Usage: `.profile <id>`
        id: Username or UUID of the player

        Get the profile of a player, including skin, UUID, and name history!
        """
        player = await get_player(id)

        if not player:
            await ctx.send(embed = await Embeds.no_player())
            return

        await ctx.send(embed = await Embeds.profile(player))


    # slash command functions

    @cog_ext.cog_slash(
        name = 'uuid',
        description = "Get a player's UUID!",
        options = [
            create_option(
                name = 'id',
                description = "The name or UUID of the player",
                option_type = 3,
                required = True
            )
        ]
    )
    async def _uuid(self, ctx, id):
        await self.uuid(ctx, id)

    @cog_ext.cog_slash(
        name = 'history',
        description = "Get a player's Name History!",
        options = [
            create_option(
                name = 'id',
                description = "The name or UUID of the player",
                option_type = 3,
                required = True
            )
        ]
    )
    async def _history(self, ctx, id):
        await self.history(ctx, id)


    @cog_ext.cog_slash(
            name = 'playerhead',
            description = "Get a player's head as an item!",
            options = [
                create_option(
                    name = 'id',
                    description = "The name or UUID of the player",
                    option_type = 3,
                    required = True
                )
            ]
        )
    async def _playerhead(self, ctx, id):
        await self.playerhead(ctx, id)


    @cog_ext.cog_slash(
        name = 'skin',
        description = "Get a player's skin!",
        options = [
            create_option(
                name = 'id',
                description = "The name or UUID of the player",
                option_type = 3,
                required = True
            ),
            create_option(
                name= " skin_type",
                description = "The type of player skin to get.",
                option_type = 3,
                required = False,
                choices = [
                    create_choice(name = "head",    value = "head"),
                    create_choice(name = "body",    value = "body"),
                    create_choice(name = "uv",      value = "uv"),
                    create_choice(name = "cape",    value = "cape"),
                    create_choice(name = "avatar",  value = "avatar")
                ])
        ]
    )
    async def _skin(self, ctx, id: str, skin_type: str = 'body'):
        await self.skin(ctx, id, skin_type)


    @cog_ext.cog_slash(
        name = 'profile',
        description = "Get a player's [rofile!",
        options = [
            create_option(
                name = 'id',
                description = "The name or UUID of the player",
                option_type = 3,
                required = True
            )
        ]
    )
    async def _profile(self, ctx, id: str):
        await self.profile(ctx, id)

def setup(bot):
    bot.add_cog(PlayerData(bot))