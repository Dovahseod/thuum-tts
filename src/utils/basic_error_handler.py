import time
import sys
import traceback

import discord

from main import Bot
from utils.embed_sender import send_embed_id
from utils.timestamp import timestamp

async def basic_error_handler(error, context: str, bot: Bot):
    """For when exceptions can't be handled by the command error handler."""

    if error is not None:
        signed_time = time.gmtime()
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", signed_time)}] [ERROR   ] Ignoring exception in {context}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        traceback_embed = discord.Embed(
            color=discord.Color.red(),
            title=f"Ignored exception in `{context}`:`")
        traceback_lines = traceback.format_exception(type(error), error, error.__traceback__)
        traceback_embed.add_field(name=traceback_lines[0], value="")
        for traceback_line in traceback_lines[1:-2]:
            traceback_embed.add_field(name="",value=traceback_line, inline=False)
        traceback_embed.add_field(name="",value=f"**{traceback_lines[-1]}**", inline=False)
        traceback_embed.set_footer(text=timestamp(signed_time))
        
        await send_embed_id(bot, bot.bot_configs['debug_channel_id'], traceback_embed)
