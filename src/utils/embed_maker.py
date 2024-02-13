from typing import Optional

import discord

def regular(text: Optional[str] = None) -> discord.Embed:
    embed = discord.Embed(color=0x00AAAA)
    if text is not None:
        embed.add_field(name="", value=text)
    return embed


def warning(text: Optional[str] = None) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.red())
    if text is not None:
        embed.add_field(name="", value=text)
    return embed


def caution(text: Optional[str] = None) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.yellow())
    if text is not None:
        embed.add_field(name="", value=text)
    return embed


def success(text: Optional[str] = None) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.green())
    if text is not None:
        embed.add_field(name="", value=text)
    return embed
