from .reglementpp import ReglementPP

async def setup(bot):
    await bot.add_cog(ReglementPP(bot)) 