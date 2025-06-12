from .track import Track

async def setup(bot):
    await bot.add_cog(Track(bot)) 