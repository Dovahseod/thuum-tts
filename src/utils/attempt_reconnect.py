import discord
from discord.ext import commands


async def attempt_reconnect(ctx: commands.Context):
    if isinstance(ctx.voice_client, discord.VoiceClient):
        if not ctx.voice_client.is_connected():
            if ctx.interaction:
                await ctx.defer()
            await ctx.voice_client.connect(
                timeout=20, reconnect=True, self_deaf=True
                )
