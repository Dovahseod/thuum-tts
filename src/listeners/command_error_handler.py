import asyncio
import time
import sys
import traceback

import discord
from discord import app_commands
from discord.ext import commands

from utils.basic_error_handler import basic_error_handler
import utils.embed_maker as em
from utils.embed_sender import send_embed_id
from utils.timestamp import timestamp


async def _on_command_error(ctx: commands.Context, error):
    """
    Checks for whether the command or the cog already have a local handler.
    If not, pass the context and error to `_command_error_handler`.
    """

    # Commands with local handlers
    if hasattr(ctx.command, 'on_error'):
        return

    # Cogs with an overwritten cog_command_error
    if hasattr(ctx.cog, f'_{ctx.cog.__class__.__name__}__error'):
        return

    await _command_error_handler(ctx, error)


async def _command_error_handler(ctx: commands.Context, error):
    ignored = (commands.CommandNotFound,
               )
    denied_access = (commands.MissingPermissions,
                     commands.MissingRole,
                     )
    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    # Any error in ignored will not be reported.
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.DisabledCommand):
        embed = em.warning(f'Command `{ctx.command}` has been disabled.')
        await ctx.send(embed=embed, ephemeral=True)

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            embed = em.warning(f'Command `{ctx.command}` can not be used in Private Messages.')
            await ctx.send(embed=embed)
        except discord.HTTPException:
            pass

    elif isinstance(error, commands.MemberNotFound | commands.UserNotFound):
        embed = em.warning(f"Member or User not found!")
        await ctx.send(embed=embed, ephemeral=True)

    elif isinstance(error, commands.ChannelNotFound):
        embed = em.warning(f"Channel not found!")
        await ctx.send(embed=embed, ephemeral=True)

    elif isinstance(error, commands.NotOwner):
        await ctx.send("This command is for the bot owners only.")
    
    elif isinstance(error, denied_access):
        await ctx.send("Access denied.")

    elif isinstance(error, commands.MissingRequiredArgument):
        embed = em.warning(f"Missing required argument `{error.param.name}`.")
        await ctx.send(embed=embed, ephemeral=True)

    elif isinstance(error, (AssertionError, commands.BadArgument, commands.BadUnionArgument, app_commands.errors.TransformerError)):
        embed = em.warning(f"At least one argument value is illegal.")
        await ctx.send(embed=embed, ephemeral=True)

    elif isinstance(error, asyncio.TimeoutError):
        if str(ctx.command) in {"join", "read", "move"}:
            embed = em.warning(f"Timed out joining voice channel. Please check the bot permissions.")
            await ctx.send(embed=embed, ephemeral=True)
            await basic_error_handler(error, "join voice channel (reported to user)", ctx.bot)
        else:
            embed = em.warning(f"An operation timed out. Bot developers have been notified.")
            await ctx.send(embed=embed, ephemeral=True)
            await basic_error_handler(error, f"command {ctx.command} from guild {ctx.guild and ctx.guild.id or None} (timeout also reported to user)", ctx.bot)
        
    else:
        if error is not None:
            # All other Errors not returned come here. And we can just print the default traceback.
            signed_time = time.gmtime()
            embed = em.warning(f"An unexpected error has occurred. Bot developers have been notified.")
            await ctx.send(embed=embed, ephemeral=True)
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", signed_time)}] [ERROR   ] Ignoring exception in command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

            if ctx.guild:
                traceback_embed = discord.Embed(
                    color=discord.Color.red(),
                    title=f"Ignored exception in command `{ctx.command}` from guild `{ctx.guild.id}`")
            else:
                traceback_embed = discord.Embed(
                    color=discord.Color.red(),
                    title=f"Ignored exception in command `{ctx.command}` from DM")
            traceback_lines = traceback.format_exception(type(error), error, error.__traceback__)
            traceback_embed.add_field(name=traceback_lines[0], value="")
            for traceback_line in traceback_lines[1:-2]:
                traceback_embed.add_field(name="",value=traceback_line, inline=False)
            traceback_embed.add_field(name="",value=f"**{traceback_lines[-1]}**", inline=False)
            traceback_embed.set_footer(text=timestamp(signed_time))
            await send_embed_id(ctx.bot, ctx.bot.bot_configs['debug_channel_id'], traceback_embed)
