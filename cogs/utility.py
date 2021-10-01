from discord.ext import commands
from requests import get

from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

from cogs.embeds import Embeds

class Utility(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    
    @commands.command()
    async def ping(self, ctx):
        """
        Usage: `.ping`
        Get the bot's latency
        """
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! in {latency}ms")


    @commands.command()
    async def status(self, ctx):
        """
        Usage: `.status`
        Get the status of different Mojang services
        """
        # get status of all services
        # returns list of dictionaries, with each dictinonary
        # containing name of service as key, and status as value
        r = get("https://status.mojang.com/check")
        data = r.json()

        # combine data into single dict
        services = {}
        for service in data: services.update(service)

        await ctx.send(embed = await Embeds.api_status(services))


    @commands.command()
    async def invite(self, ctx):
        """
        Usage: `.invite`
        Invite the bot to your server!
        """
        # send invite link for bot
        invite = 'https://discord.com/api/oauth2/authorize?client_id=781349890944270366&permissions=2147503104&scope=bot%20applications.commands'
        await ctx.send(f"Here's the invite link: {invite}")

    
    @commands.command()
    async def help(self, ctx, command: str = ""):
        """
        Usage: `.help [command]`
        `command`: Tne command to get help about

        Get general help, or help about a command!
        """
        if not command:
            await ctx.send(embed = await Embeds.general_help())
            return

        for cmd in self.bot.commands:
            if cmd.name == command:
                await ctx.send(embed = await Embeds.command_help(cmd.name, cmd.help))
                return

        await ctx.send(embed = await Embeds.no_command(command))
    

    # slash command functions

    @cog_ext.cog_slash(
        name = 'ping',
        description = "Get the bot's latency!",
        options = []
    )
    async def _ping(self, ctx):
        await self.ping(ctx)


    @cog_ext.cog_slash(
        name = 'status',
        description = "Get the status of Mojang's APIs!",
        options = []
    )
    async def _status(self, ctx):
        await self.status(ctx)


    @cog_ext.cog_slash(
        name = 'invite',
        description = "Invite the bot to your server!",
        options = []
    )
    async def _invite(self, ctx):
        await self.invite(ctx)


    @cog_ext.cog_slash(
        name = 'help',
        description = "Get some help!",
        options = [
            create_option(
                name = 'command',
                description = "Command to get help about",
                option_type = 3,
                required = False
            ),
        ]
    )
    async def _help(self, ctx, command = ""):
        await self.help(ctx, command)


def setup(bot):
    bot.add_cog(Utility(bot))