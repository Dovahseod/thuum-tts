from typing import Optional

from discord import app_commands
from discord.ext import commands

from commands.preferences.voices import _voices
from utils.pages_ui import PagesUI


class Preferences(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="voices")
    @app_commands.describe(
        query="The language code to search voices of. Use 'mb' to list all MBROLA voices."
        )
    async def voices(self, ctx: commands.Context, query: Optional[str] = None):
        """Lists the available voices of the bot."""
        await _voices(ctx, query)


async def setup(bot: commands.Bot):
    await bot.add_cog(Preferences(bot))
    print("Cog loaded: Preferences")
