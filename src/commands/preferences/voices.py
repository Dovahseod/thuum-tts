import typing

from discord.ext import commands

from main import Bot
import utils.embed_maker as em
from utils.pages_ui import pages_factory


async def _voices(ctx: commands.Context, query: typing.Optional[str] = None):
    bot = typing.cast(Bot, ctx.bot)
    if not query:
        query = ''
        title = 'Available eSpeak voices'
        if bot.tts.enable_mbrola:
            await ctx.send(embed=mbrola_embed())
        await ctx.send(embed=variants_embed())
    elif query == 'mb':
        title = 'Available MBROLA voices'
    elif query == 'variant':
        title = 'Available voice variants'
    else:
        title = f'Available voices for `{query}`'
        await ctx.send(embed=variants_embed())
    
    results = await bot.tts.list_voices(query)
    if not results:
        if query:
            return await ctx.send(embed=em.warning(
                "No voices available for the given query."
                ))
        else:
            return await ctx.send(embed=em.warning(
                "No voices available."
                ))
        
    title_row = "**eSpeak Identifier - Language/Gender - Voice Name**"
    results_display = [
        f"`{voice_info[-1]}` - {voice_info[1]}/{voice_info[3]} - {voice_info[4]}"
        for voice_info in results]
    first_page, page_control_ui = pages_factory(results_display, 10, 0x00AAAA, title, title_row)
    if page_control_ui is not None:
        await ctx.send(embed=first_page, view=page_control_ui)
    else:
        await ctx.send(embed=first_page)


def mbrola_embed():
    return em.regular(
        "This bot provides the option to use [MBROLA](https://github.com/numediart/MBROLA) generate speech.\n\nUse `mb` as the query for the `voices` command to list all the available MBROLA voices.\n\nNote that voice variants do not work well on MBROLA voices."
    )


def variants_embed():
    return em.regular(
        "By suffixing `+xx` to the voice identifier, where xx is the identifier of the variant (example: `en+m2`), you can alter the voice for potentially better results.\n\nUse `variant` as the query for the `voices` command to list all the available variants.\n\nNote that voice variants do not work well on MBROLA voices."
    )

