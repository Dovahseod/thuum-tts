from discord.ext import commands

import utils.embed_maker as em


async def _leave(ctx: commands.Context):
    if not ctx.guild:
        raise commands.NoPrivateMessage
    if not ctx.voice_client:
        return await ctx.send(embed=em.warning(
            "Bot is not in a voice channel."
            ), ephemeral=True)
    await ctx.voice_client.disconnect(force=True)
    await ctx.send(embed=em.caution("Bot disconnected."))
