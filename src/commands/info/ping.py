import time

from discord.ext import commands

import utils.embed_maker as em

async def _ping(ctx: commands.Context):
    bot: commands.Bot = ctx.bot

    embed = em.regular()
    embed.add_field(name="Latency", value="Please wait")
    embed.add_field(inline=False, name="WebSocket Protocol Latency", value=f"{int(bot.latency*1000)} ms")

    start_ping = time.time()
    message = await ctx.send(embed=embed)
    ping = time.time() - start_ping
    embed.set_field_at(0, name="Command Execution Latency", value=f"{int(ping*1000)} ms")
    await message.edit(embed=embed)
