import discord

from utils.custom_exceptions import ChannelNotMessagable


async def send_embed_id(bot: discord.Client, channel_id: int, embed: discord.Embed) -> discord.Message:
    channel = await bot.fetch_channel(channel_id)
    if isinstance(channel, discord.abc.Messageable):
        return await channel.send(embed=embed)
    else:
        raise ChannelNotMessagable
