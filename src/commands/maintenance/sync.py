from discord.ext import commands

import utils.embed_maker as em

async def _sync(ctx: commands.Context, clear):
    embed = em.caution("Syncing application commands...")
    response = await ctx.reply(embed=embed)
    if clear:
        ctx.bot.tree.clear_commands(guild=None)
    synced_global_commands = await ctx.bot.tree.sync(guild=None)
    embed = em.success(f"Synced {len(synced_global_commands)} global application commands.")
    await response.edit(embed=embed)
