import typing

from discord.ext import commands

from main import Bot
import utils.embed_maker as em
from utils.pages_ui import pages_factory


async def _voices(ctx: commands.Context, query: typing.Optional[str] = None):
    bot = typing.cast(Bot, ctx.bot)
    if not query:
        query = ''
        title = 'Available voices'
        if bot.tts.enable_mbrola:
            await ctx.send(embed=mbrola_embed())
    elif query == 'mb':
        title = 'Available MBROLA voices'
    else:
        title = f'Available voices for `{query}`'
    
    results = await bot.tts.list_voices(query)
    title_row = "`eSpeak Identifier` - Language/Gender - Voice Name"
    results_display = [
        f"`{voice_info[-1]}` - {voice_info[1]}/{voice_info[3]} - {voice_info[4]}"
        for voice_info in results]
    first_page, page_control_ui = pages_factory(results_display, 10, 0x00AAAA, title, title_row)
    await ctx.send(embed=first_page, view=page_control_ui)


def mbrola_embed():
    return em.regular(
        "This bot provides the option to use (MBROLA)[https://github.com/numediart/MBROLA] to produce better speech from the text.\n\nUse `mb` as the query for the `voices` command to filter for the available MBROLA voices."
    )
