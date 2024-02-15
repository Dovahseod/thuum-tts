import typing

import discord
from discord import app_commands
from discord.ext import commands

import utils.embed_maker as em

COGS_INCLUDED = ['Information', 'Voice', 'Music', 'Text']
autocomplete_choices = set()

async def _help(ctx: commands.Context, command: typing.Optional[str]):
    if not command:
        embed = em.regular()
        embed.set_footer(text="Use /help [command] for details about a command")
        for cog_name in COGS_INCLUDED:
            cog = commands.Bot.get_cog(ctx.bot, cog_name)
            if cog:
                command_name_list = sorted([cog_command.name for cog_command in cog.get_commands()])
                embed.add_field(name=cog_name, value="\n".join(command_name_list))
    else:
        command = command.lower()
        requested_command = None
        for cog_name in COGS_INCLUDED:
            cog = commands.Bot.get_cog(ctx.bot, cog_name)
            if cog:
                for cog_command in cog.walk_commands():
                    if cog_command.name == command or command in cog_command.aliases:
                        requested_command = cog_command
                        break
            if requested_command:
                break

        if not requested_command:
            embed = em.warning("Command not found.")
        else:
            requested_command = typing.cast(commands.HybridCommand, requested_command)
            embed = discord.Embed(color=discord.Colour.dark_purple())
            embed.set_footer(text="<> = required argument, [] = optional argument")
            embed.add_field(name="", value=f"**Command name:** {requested_command.name}")
            if requested_command.aliases:
                embed.add_field(name="", value=f"**Command aliases:** "+'/'.join(requested_command.aliases), inline=False)
            embed.add_field(name="", value=f"**Description:** {requested_command.short_doc}", inline=False)
            usage = f"**Usage:** '{requested_command.name}"
            for parameter_name, parameter in requested_command.clean_params.items():
                if parameter.required:
                    usage += f" <{parameter_name}>"
                else:
                    usage += f" [{parameter_name}]"
            embed.add_field(name="", value=usage, inline=False)
        
    await ctx.reply(embed=embed)


async def _help_autocomplete(
        interaction: discord.Interaction,
        current: str
) -> list[app_commands.Choice[str]]:
    if not autocomplete_choices:
        bot = typing.cast(commands.Bot, interaction.client)
        for cog_name in COGS_INCLUDED:
            cog = bot.get_cog(cog_name)
            if cog:
                for cog_command in cog.get_commands():
                    autocomplete_choices.add(cog_command.name)

    return [
        app_commands.Choice(name=choice, value=choice)
        for choice in autocomplete_choices if current.lower() in choice
    ]
