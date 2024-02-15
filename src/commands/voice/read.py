import io
import sys
import typing

import discord
from discord.ext import commands

from main import Bot
from utils.attempt_reconnect import attempt_reconnect
import utils.embed_maker as em


FFMPEG_OPTIONS = {'options': '-vn'}

async def _read(ctx: commands.Context, phrase: str, voice: typing.Optional[str] = None):
    if not ctx.guild:
        raise commands.NoPrivateMessage
    if not phrase:
        return await ctx.send(embed=em.warning(
            "Cannot read an empty message."
            ), ephemeral=True)
    
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
        vc = typing.cast(discord.VoiceClient, ctx.voice_client)
    else:
        vc = await member.voice.channel.connect(
            timeout=20, reconnect=True, self_deaf=True
            )
    
    if vc.channel != member.voice.channel:
        return await ctx.send(embed=em.warning(
            "You're not in the same voice channel as the bot."
            ), ephemeral=True)

    if vc.is_playing():
        return await ctx.send(embed=em.warning(
            "Please wait for the previous speech to finish."
            ), ephemeral=True)
    
    if ctx.interaction and not ctx.interaction.response.is_done():
        await ctx.defer()

    # Grab preferences
    bot = typing.cast(Bot, ctx.bot)
    cursor = await bot.preferences.execute(
        f"""SELECT voice, wpm, gap, pitch, amplitude
            FROM preferences
            WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}"""
        )
    user_preferences = await cursor.fetchone()

    # make audio
    if user_preferences is None:
        audio = await bot.tts.read(phrase, voice=voice)
    else:
        user_preferences_dict = {
            key: user_preferences[key] for key in user_preferences.keys()
            }
        user_preferences_dict['voice'] = voice or user_preferences_dict['voice']
        audio = await bot.tts.read(phrase, **user_preferences_dict)

    # play audio
    audio_io = io.BytesIO(audio)
    await ctx.send(embed=em.regular("Reading"), ephemeral=True)
    vc.play(discord.FFmpegPCMAudio(audio_io, pipe=True, stderr=sys.stderr, **FFMPEG_OPTIONS))
