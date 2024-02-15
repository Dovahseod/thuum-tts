import typing

import discord
from discord import app_commands
from discord.ext import commands

from main import Bot
import utils.embed_maker as em
from utils.espeak_ng import TTSParameterError


async def _preference_update(ctx: commands.Context, key: str, value: int | str):
    if not ctx.guild:
        raise commands.NoPrivateMessage
    bot = typing.cast(Bot, ctx.bot)
    db = bot.preferences

    if ctx.interaction and not ctx.interaction.response.is_done():
        await ctx.defer()

    # Sanitize input
    key = key.lower()

    # Illegal key
    if not key in {'wpm', 'wordgap', 'pitch', 'amplitude', 'voice'}: 
        return await ctx.send(embed=em.warning(
            f"Key {key} not recognized."
            ), ephemeral=True)
    
    # Bad value type for the parameter
    if ((key in {'wpm', 'wordgap', 'pitch', 'amplitude'}
            and not isinstance(value, int))                  # str where int is expected
        or (key == 'voice' and not isinstance(value, str))): # int where str is expected
        return await ctx.send(embed=em.warning(
            f"Illegal value type for {key}, check inputs."
            ), ephemeral=True)
    
    # Value exceeding limits for the parameter
    try:
        bot.tts.verify_parameters({key: value})
    except TTSParameterError as e:
        return await ctx.send(embed=em.warning(
            f"Parameter {key} out of bounds: {value} given, expected within [{e.limits[0]}, {e.limits[1]}]."
            ), ephemeral=True)
    
    # Upsert the config
    await db.execute(
        f"""INSERT INTO preferences (guild, user, {key})
            VALUES (?, ?, ?)
            ON CONFLICT(guild, user) DO UPDATE
            SET {key} = excluded.{key}""",
            (ctx.guild.id, ctx.author.id, value))
    await db.commit()

    await ctx.send(embed=em.success(f"Updated `{key}` to `{value}`."))


async def _tts_parameter_autocomplete(
        interaction: discord.Interaction,
        current: str
        ) -> list[app_commands.Choice[str]]:
    valid_parameters = {'wpm', 'wordgap', 'pitch', 'amplitude', 'voice'}
    return [
        app_commands.Choice(name=parameter, value=parameter)
        for parameter in valid_parameters if current.lower() in parameter
    ]
