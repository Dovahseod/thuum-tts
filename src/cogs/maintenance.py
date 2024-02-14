from discord.ext import commands

from commands.maintenance.sync import _sync
from commands.maintenance.shutdown import _shutdown


class Maintenance(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
            
    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, clear: str | None = None):
        """Sync all application commands to Discord or clear them."""
        await _sync(ctx, clear)
        
    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx: commands.Context):
        """Shut the bot down."""
        await _shutdown(ctx)


async def setup(bot: commands.Bot):
    await bot.add_cog(Maintenance(bot))
    print("Cog loaded: Maintenance")
