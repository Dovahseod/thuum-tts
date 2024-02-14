from discord.ext import commands

import utils.embed_maker as em
from utils.embed_sender import send_embed_id
from utils.timestamp import timestamp

async def _shutdown(ctx: commands.Context):
    embed = em.warning("Shutting down.")
    await ctx.reply(embed=embed, ephemeral=True)
    startup_embed = em.warning(f"Bot shut down by {ctx.author.mention} at {timestamp()}.")
    await send_embed_id(ctx.bot, ctx.bot.bot_configs['debug_channel_id'], startup_embed)
    await ctx.bot.preferences.close()
    await ctx.bot.close()
