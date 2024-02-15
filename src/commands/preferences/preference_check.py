import typing

import discord
from discord import app_commands
from discord.ext import commands

from main import Bot
import utils.embed_maker as em


async def _preference_check(ctx: commands.Context, key: str):
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
    
    # Get value
    cursor = await db.execute(
        f"""SELECT {key} from preferences WHERE guild = ? AND user = ?""",
            (ctx.guild.id, ctx.author.id))
    result = await cursor.fetchone()

    if not result or result[key] is None:
        value = bot.tts.__getattribute__(key)
    else:
        value = result[key]

    if key == 'wordgap' and value != 0:
        await ctx.send(embed=em.regular(
            f"Your `{key}` is set to `{value}` ({value}0ms)."
            ), ephemeral=True)
    else:
        await ctx.send(embed=em.regular(
            f"Your `{key}` is set to `{value}`."
            ), ephemeral=True)
