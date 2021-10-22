from discord.ext import commands

class Servers(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        
    def server(self, ip):
    
def setup(bot):
    bot.add_cog(Servers(bot))