from discord import app_commands
from discord.ext import commands

from commands.info.help import _help, _help_autocomplete
from commands.info.ping import _ping


class Information(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
            
    @commands.hybrid_command(name="help", aliases=['h'])
    @app_commands.autocomplete(command=_help_autocomplete)
    @app_commands.describe(
        command="The command to display details of. Leave empty to display all commands."
        )
    async def help(
            self,
            ctx: commands.Context,
            command: str | None = None
        ):
        """Display the commands of the bot or the details of a specific command."""
        await _help(ctx, command)

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Checks the WebSocket Protocol latency and the effective latency of the bot."""
        await _ping(ctx)


async def setup(bot: commands.Bot):
    await bot.add_cog(Information(bot))
    print("Cog loaded: Information")
