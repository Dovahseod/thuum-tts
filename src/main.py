import asyncio
import json
import logging
import os
import platform
import time
from collections import defaultdict

import aiosqlite
import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs import EXTENSIONS
from tasks.activity_update import _activity_update
from utils.espeak_ng import Speaker
import utils.embed_maker as em
from utils.embed_sender import send_embed_id
from utils.timestamp import timestamp


load_dotenv()
TOKEN = os.getenv("TOKEN")
assert TOKEN
BOT_CONFIG_FILENAME = os.getenv("BOT_CONFIG_FILENAME")
assert BOT_CONFIG_FILENAME is not None


dirname = os.path.dirname(__file__)
config_filepath = os.path.join(dirname, f'../config/{BOT_CONFIG_FILENAME}.json')
with open(config_filepath) as config_file:
    try:
        bot_configs: dict = json.load(config_file)
    except json.decoder.JSONDecodeError as error:
        print(f"Bot configuration error: Expecting value in {BOT_CONFIG_FILENAME}.json at Line {error.lineno} Column {error.colno}.")
        input("Press Enter to exit...")
        exit()
    if not bot_configs:
        print(f"Bot configuration error: Configuration file does not exist or is empty. In .env, BOT_CONFIG_FILENAME should not include the file extension or file path.")
        input("Press Enter to exit...")
        exit()


class Bot(commands.Bot):
    def __init__(self, bot_configs: dict) -> None:
        self.bot_configs: dict = bot_configs
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=bot_configs['command_prefix'],
            intents=intents,
            help_command=None, # Custom help command is implemented
            max_messages=None
        )
        self.owner_ids = bot_configs['owner_ids']
        self.tts = Speaker(
            program=bot_configs['espeak_ng_path'],
            voice=bot_configs['default_voice'])

    async def setup_hook(self) -> None:
        self.preferences = await aiosqlite.connect("data/users.db")
        for extension in EXTENSIONS:
            await self.load_extension(extension)
        print("Bot ready")
        startup_embed = em.success(f"Bot started/restarted at {timestamp()}.")
        await send_embed_id(self, self.bot_configs['debug_channel_id'], startup_embed)

    async def on_connect(self):
        await _activity_update(self)


async def main(**kwargs):
    log_filename = f'logs/{time.strftime("%Y.%m.%d.%H.%M.%S", time.gmtime())}_discord.log'
    handler = logging.FileHandler(filename=log_filename, encoding='utf-8', mode='w')
    discord.utils.setup_logging(handler=handler, level=logging.INFO, root=False)
    async with Bot(bot_configs) as bot:
        await bot.start(TOKEN)  


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
