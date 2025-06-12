from .saloncreator import SalonCreator

async def setup(bot):
    await bot.add_cog(SalonCreator(bot)) 