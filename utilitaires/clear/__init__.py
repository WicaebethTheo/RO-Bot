from .clear import Clear

async def setup(bot):
    await bot.add_cog(Clear(bot)) 