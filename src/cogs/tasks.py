import datetime

from discord.ext import commands, tasks

from main import Bot
from tasks.activity_update import _activity_update
from utils.basic_error_handler import basic_error_handler

EVERY_MINUTE = [datetime.time(h, m) for h in range(24) for m in range(60)]


class Tasks(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.activity_update.start()

    def cog_unload(self):
        self.activity_update.cancel()

    @tasks.loop(time=EVERY_MINUTE)
    async def activity_update(self):
        await _activity_update(self.bot)

    @activity_update.before_loop
    async def activity_update_before_loop(self):
        await self.bot.wait_until_ready()

    @activity_update.error
    async def activity_update_handler(self, error):
        await basic_error_handler(error, "activity update", self.bot)


async def setup(bot: Bot):
    await bot.add_cog(Tasks(bot))
    print("Cog loaded: Tasks")
