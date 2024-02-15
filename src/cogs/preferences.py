from typing import Optional

from discord import app_commands
from discord.ext import commands

from commands.preferences.voices import _voices
from commands.preferences.preference_check import _preference_check
from commands.preferences.preference_update import _preference_update, _tts_parameter_autocomplete


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

    @commands.hybrid_command(name='preference', aliases = ['update'])
    @app_commands.guild_only()
    @commands.guild_only()
    @app_commands.describe(
        key='Name of the parameter. \'wpm\', \'wordgap\' (word gap, *10ms), \'pitch\', or \'amplitude\'.',
        value='Value to update the parameter to. Leave empty to check current setting.'
        )
    @app_commands.autocomplete(key=_tts_parameter_autocomplete)
    async def preference(self, ctx: commands.Context, key: str, value: Optional[int]):
        """Checks or update a parameter of the TTS, for you, in this server."""
        if value is not None:
            await _preference_update(ctx, key, value)
        else:
            await _preference_check(ctx, key)

    @commands.hybrid_command(name='wpm', aliases = ['s', 'speed', 'w'])
    @app_commands.guild_only()
    @commands.guild_only()
    @app_commands.describe(
        value='Accept values in [20, 500]. Leave empty to check current setting.'
        )
    async def wpm(self, ctx: commands.Context, value: Optional[int]):
        """Checks or update the WPM (words per minute) of the TTS, for you, in this server."""
        if value is not None:
            await _preference_update(ctx, 'wpm', value)
        else:
            await _preference_check(ctx, 'wpm')

    @commands.hybrid_command(name='wordgap', aliases = ['g', 'wgap', 'gap'])
    @app_commands.guild_only()
    @commands.guild_only()
    @app_commands.describe(
        value='Accept values in [0, 500]. Value * 10ms is the gap. Leave empty to check current setting.'
        )
    async def wordgap(self, ctx: commands.Context, value: Optional[int]):
        """Checks or update the word gap (extra time between words) of the TTS, for you, in this server."""
        if value is not None:
            await _preference_update(ctx, 'wordgap', value)
        else:
            await _preference_check(ctx, 'wordgap')

    @commands.hybrid_command(name='pitch', aliases = ['p'])
    @app_commands.guild_only()
    @commands.guild_only()
    @app_commands.describe(
        value='Accept values in [0, 99]. Leave empty to check current setting.'
        )
    async def pitch(self, ctx: commands.Context, value: Optional[int]):
        """Checks or update the pitch of the TTS, for you, in this server."""
        if value is not None:
            await _preference_update(ctx, 'pitch', value)
        else:
            await _preference_check(ctx, 'pitch')

    @commands.hybrid_command(name='amplitude', aliases = ['a', 'volume', 'vol', 'amp'])
    @app_commands.guild_only()
    @commands.guild_only()
    @app_commands.describe(
        value='Accept values in [0, 200], in %. Leave empty to check current setting.'
        )
    async def amplitude(self, ctx: commands.Context, value: Optional[int]):
        """Checks or update the amplitude (volume) of the TTS, for you, in this server."""
        if value is not None:
            await _preference_update(ctx, 'amplitude', value)
        else:
            await _preference_check(ctx, 'amplitude')

    @commands.hybrid_command(name='voice', aliases = ['v'])
    @app_commands.guild_only()
    @commands.guild_only()
    @app_commands.describe(
        value='Leave empty to check current setting.'
        )
    async def voice(self, ctx: commands.Context, value: Optional[str]):
        """Checks or update the voice of the TTS, for you, in this server."""
        if value is not None:
            await _preference_update(ctx, 'voice', value)
        else:
            await _preference_check(ctx, 'voice')


async def setup(bot: commands.Bot):
    await bot.add_cog(Preferences(bot))
    print("Cog loaded: Preferences")
