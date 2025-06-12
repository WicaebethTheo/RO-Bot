from .tracking import Tracking

async def setup(bot):
    await bot.add_cog(Tracking(bot)) 