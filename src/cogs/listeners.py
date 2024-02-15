from discord.ext import commands

from listeners.command_error_handler import _on_command_error


class Listeners(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        await _on_command_error(ctx, error)


async def setup(bot: commands.Bot):
    await bot.add_cog(Listeners(bot))
    print("Cog loaded: Listeners")
