# thuum-tts
A Discord bot for text-to-speech.

## Dependencies
[discord.py](https://github.com/Rapptz/discord.py) (with voice support), [python-dotenv](https://github.com/theskumar/python-dotenv), [aiofiles](https://github.com/Tinche/aiofiles), [aiosqlite](https://github.com/omnilib/aiosqlite)

## Initial Configuration
[eSpeak NG](https://github.com/espeak-ng/espeak-ng) is required for the tts to work. [MBROLA](https://github.com/numediart/MBROLA) with a selection of [MBROLA voices](https://github.com/numediart/MBROLA-voices) is recommended as the resulted speech is more natural.

In `/config/` folder make a copy of `example.json`, rename it to your liking, and fill in values.

All IDs should be integers. `default_voice` should be the identifier a voice available to eSpeak NG, either [natively](https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md) or a [MBROLA voice as available in eSpeak](https://github.com/espeak-ng/espeak-ng/blob/master/docs/mbrola.md#voice-names) You can also get a list of accepted voices by running
```
espeak-ng --voices
```
in the command line (Linux command line, or on Windows, command prompt or PowerShell). If the bot is running on Windows, eSpeak NG should be added to PATH, or change the `espeak_ng_path` to the path of the eSpeak NG program. If you have not set up MBROLA, then change `enable_mbrola` to `false`.

In the root folder, create a `.env` for the bot token and configuration file name. It should look like this:
```
TOKEN=your_bot_token_here
BOT_CONFIG_FILENAME=filename_without_extension
```

On Discord developer portal's side, this bot requires the message content intent to accept message commands - slash commands will still work without it as long as you sync them somehow in advance.

## Launching
**Command prompt or PowerShell:**
```
python src/main.py
```
**Linux**, with the autorestart-on-crash bash script **(recommended)**:
```
bash start.sh
```
Linux, directly:
```
python3 src/main.py
```

## Post-launch configuration
Once the bot is launched, run `-sync` as a Owner as registered in the configuration file to enable the application commands.
