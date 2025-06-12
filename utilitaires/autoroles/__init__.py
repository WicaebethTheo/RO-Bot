from .autoroles import AutoRoles

async def setup(bot):
    await bot.add_cog(AutoRoles(bot)) 