from .creationvoc import CreationVoc

async def setup(bot):
    await bot.add_cog(CreationVoc(bot)) 