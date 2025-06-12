from .tickets import TicketSystem

async def setup(bot):
    await bot.add_cog(TicketSystem(bot)) 