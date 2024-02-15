import typing

import discord
from discord.ext import commands

from utils.attempt_reconnect import attempt_reconnect
import utils.embed_maker as em


async def _stop(ctx: commands.Context):
    if not ctx.guild:
        raise commands.NoPrivateMessage
    if not ctx.voice_client:
        return await ctx.send(embed=em.warning(
            "Bot is not connected to a voice channel."
            ), ephemeral=True)
    await attempt_reconnect(ctx)

    vc = typing.cast(discord.VoiceClient, ctx.voice_client)
    assert isinstance(ctx.author, discord.Member)
    if not ctx.author.voice or vc.channel != ctx.author.voice.channel:
        return await ctx.send(embed=em.warning(
            "You cannot stop the TTS Speech outside the voice channel."
            ), ephemeral=True)
    if vc.is_playing():
        vc.stop()
        return await ctx.send(embed=em.caution("TTS Speech stopped."))
    await ctx.send(embed=em.warning(
        "There is nothing to stop."
        ), ephemeral=True)
