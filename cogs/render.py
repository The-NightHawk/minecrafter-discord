from discord.ext import commands
from urllib.parse import urlencode

from cogs.shared import get_player
from cogs.embeds import Embeds

poses = {
        'walk': "vr=-25&hr=52&hrh=-8&vrll=22&vrrl=-6&vrla=23&vrra=-31",
        'sprint': "vr=-25&hr=52&hrh=-8&vrll=70&vrrl=-68&vrla=72&vrra=-72",
        'flat': "vr=0&hr=35&hrh=0&vrll=0&vrrl=0&vrla=0&vrra=0",
        'mario': "vr=-7&hr=35&hrh=0&vrll=33&vrrl=-27&vrla=135&vrra=-27",
        'wave': "vr=-7&hr=35&hrh=0&vrll=4&vrrl=-8&vrla=160&vrra=-10",
        'zombie': "vr=-25&hr=52&hrh=-8&vrll=62&vrrl=-6&vrla=84&vrra=88"
    }

class Render(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def pose(self, ctx, id, pose):
        player = await get_player(id)

        if not player:
            await ctx.send(embed = await Embeds.no_player())
            return
        
        if pose.lower() not in poses:
            await ctx.send(embed = await Embeds.no_pose(pose))
            return
             
        url = f"http://photopass.appspot.com/3d.php?user={id}&"
        url += poses[pose.lower()]
        print(url)
        await ctx.send(embed = await Embeds.skin(player, url))

    @commands.command()
    async def render(self, ctx, id, vr=-25, hr=35, hrh=0, vrll=0, vrrl=0, vrla=0, vrra=0):
        player = await get_player(id)

        if not player:
            await ctx.send(embed = await Embeds.no_player())
            return

        params = {
            'user': player.name,
            'vr': vr,
            'hr': hr,
            'hrh': hrh,
            'vrll': vrll,
            'vrrl': vrrl,
            'vrla': vrla,
            'vrra': vrra,
            'ratio': 30,
            'displayHair': False,
            'aa': True
        }
        
        url = "http://photopass.appspot.com/3d.php?" + urlencode(params)
        await ctx.send(embed = await Embeds.skin(player, url))

def setup(bot):
    bot.add_cog(Render(bot))