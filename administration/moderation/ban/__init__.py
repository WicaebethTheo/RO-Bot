from .ban import BanSystem

async def setup(bot):
    await bot.add_cog(BanSystem(bot)) 