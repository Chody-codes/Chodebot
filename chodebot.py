import asyncio
import datetime
import logging
import os
from configparser import ConfigParser

import discord
from discord.ext import commands
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('log.txt')
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)
now = datetime.datetime.now()
formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
load_dotenv()
DISTOKEN = os.getenv("TOKEN")
bot_owner_id = int(os.getenv("OWNERID"))
PermError = os.getenv("PermError")
tokens = ConfigParser()
tokens.read("tokens.ini")
TOKEN = tokens["tokens"]["bottoken"]
intents = discord.Intents.all()
# client = discord.Client(intents=intents) # discord.VoiceClient??
bot = commands.Bot(command_prefix='!', intents=intents)

startup_extensions = ["cogs.commands", "cogs.count", "cogs.events"]
# bot.remove_command('help')


async def on_ready():
    pass


@bot.event
async def on_ready():
    logger.info(f"------\n{formatted_time}: Logged in as: {bot.user.name}\n------")


@bot.command()
async def load(ctx, cog_name):
    """Loads a cog"""
    if ctx.author.id != bot_owner_id:
        await ctx.send(PermError)
        return
    try:
        await bot.load_extension(f'cogs.{cog_name}')
        logger.info(f"Loaded {cog_name}")
        await ctx.send(f"Loaded {cog_name}")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        logger.error(f"{formatted_time}: Failed to Load {cog_name}: {exc}")
        await ctx.send(f"Failed to Load {cog_name}")


@bot.command()
async def unload(ctx, cog_name):
    """Unloads a cog"""
    if ctx.author.id != bot_owner_id:
        await ctx.send(PermError)
        return
    try:
        await bot.unload_extension(f"cogs.{cog_name}")
        logger.info(f"Unloaded {cog_name}")
        await ctx.send(f"Unloaded {cog_name}")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        logger.error(f"{formatted_time}: Failed to unload {cog_name}: {exc}")
        await ctx.send(f"Failed to unload {cog_name}")


@bot.command()
async def reload(ctx, cog_name):
    """Reloads a cog"""
    if ctx.author.id != bot_owner_id:
        await ctx.send(PermError)
        return
    try:
        await bot.unload_extension(f"cogs.{cog_name}")
        logger.info(f"Unloaded {cog_name}")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        logger.error(f"{formatted_time}: Failed to unload {cog_name}: {exc}")
    try:
        await bot.load_extension(f"cogs.{cog_name}")
        logger.info(f"Loaded {cog_name}")
        await ctx.send(f"Reloaded extension {cog_name}")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        logger.error(f"{formatted_time}: Failed to load {cog_name}: {exc}")
        await ctx.send(f"Failed to load {cog_name}")


async def load_extensions():
    for extension in startup_extensions:
        try:
            await bot.load_extension(extension)
            logger.info(f"Loaded {extension}")
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            logger.error(f"{formatted_time}: Failed to load {extension}: {exc}")


async def main():
    print('\n')
    try:
        async with bot:
            await load_extensions()
            await bot.start(DISTOKEN)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
