import typing

import discord
from discord.ext import commands

from utils.attempt_reconnect import attempt_reconnect
import utils.embed_maker as em


async def _join(ctx: commands.Context):
    if not ctx.guild:
        raise commands.NoPrivateMessage
    
    member = typing.cast(discord.Member, ctx.author)
    if not member.voice or not member.voice.channel:
        return await ctx.send(embed=em.warning(
            "You're not in a voice channel."
            ), ephemeral=True)
    if ctx.voice_client is not None:
        if not isinstance(ctx.voice_client, discord.VoiceClient):
            await ctx.voice_client.disconnect(force=True)
        else:
            await attempt_reconnect(ctx)
            return await ctx.send(embed=em.regular(
            "Reconnect attempted."
            ), ephemeral=True)
    else:
        await attempt_reconnect(ctx)
    
    vc = await member.voice.channel.connect(
        timeout=20, reconnect=True, self_deaf=True
        )
    await ctx.send(embed=em.success(f'Joined {vc.channel.mention}.'))
