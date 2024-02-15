from typing import Optional

from discord import app_commands
from discord.ext import commands

from commands.voice.join import _join
from commands.voice.leave import _leave
from commands.voice.move import _move
from commands.voice.stop import _stop
from commands.voice.read import _read


class Voice(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
            
    @commands.hybrid_command(name="join", aliases=['j'])
    @app_commands.guild_only()
    @commands.guild_only()
    async def join(self, ctx: commands.Context):
        """Asks the bot to join your voice channel."""
        await _join(ctx)

    @commands.hybrid_command(name="move", aliases=['m', 'mv'])
    @app_commands.guild_only()
    @commands.guild_only()
    async def move(self, ctx: commands.Context):
        """Asks the bot to move to your voice channel."""
        await _move(ctx)

    @commands.hybrid_command(name="leave", aliases=['l'])
    @app_commands.guild_only()
    @commands.guild_only()
    async def leave(self, ctx: commands.Context):
        """Asks the bot to leave the voice channel."""
        await _leave(ctx)

    @commands.hybrid_command(name="stop")
    @app_commands.guild_only()
    @commands.guild_only()
    async def stop(self, ctx: commands.Context):
        """Stops the speech."""
        await _stop(ctx)

    @commands.hybrid_command(name='read', aliases = ['r', '', 'tts'])
    @app_commands.guild_only()
    @commands.guild_only()
    @app_commands.describe(
        phrase="The \"text\" part of \"text-to-speech\"."
        )
    async def read(self, ctx: commands.Context, *, phrase: str):
        """Reads something with text-to-speech."""
        await _read(ctx, phrase)

    @commands.hybrid_command(name='readvoice', aliases = ['rv'])
    @app_commands.guild_only()
    @commands.guild_only()
    @app_commands.describe(
        voice="The eSpeak identifier for the voice to use.",
        phrase="The \"text\" part of \"text-to-speech\"."
        )
    async def readvoice(self, ctx: commands.Context, voice: str, *, phrase: str):
        """Reads something with text-to-speech in a specified voice."""
        await _read(ctx, phrase, voice)


async def setup(bot: commands.Bot):
    await bot.add_cog(Voice(bot))
    print("Cog loaded: Voice")
