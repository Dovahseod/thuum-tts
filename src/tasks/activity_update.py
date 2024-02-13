import random

import discord
from discord.ext import commands

from utils.json_async_io import JsonAIO


activity_file = JsonAIO("activity.json", default_value=[['p', 'missing activity.json']])


async def _activity_update(bot: commands.Bot):
    activity_list = await activity_file.read_cache()
    assert isinstance(activity_list, list)

    activity = random.choice(activity_list)
    activity_type, activity_name = activity[0], activity[1]
    await bot.change_presence(activity=discord.Activity(
        type=activity_type_decode(activity_type),
        name=activity_name))


def activity_type_decode(activity_type) -> discord.ActivityType:
    match activity_type:
        case 'p':
            return discord.ActivityType.playing
        case 's':
            return discord.ActivityType.streaming
        case 'l':
            return discord.ActivityType.listening
        case 'w':
            return discord.ActivityType.watching
        case 'c':
            return discord.ActivityType.competing
        case _:
            return discord.ActivityType.playing
