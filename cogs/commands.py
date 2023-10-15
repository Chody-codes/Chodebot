import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
PermError = os.getenv("PermError")

class CustCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
##############################################

    @commands.command()
    async def ping(self, ctx):
        if ctx.author.guild_permissions.administrator:
            await ctx.send(f"Pong {round(self.bot.latency * 1000)} ms")
        else:
            await ctx.send(PermError)
    @commands.command()
    async def clear(self, ctx, limit:int):
        if ctx.author.guild_permissions.administrator:
            await ctx.channel.purge(limit=limit)
            await ctx.send(f'{limit} messages have been cleared.')
        else: await ctx.send(PermError)

##############################################

    @commands.command()
    async def stuffz(self, ctx):
        response = '\nYou can:\n!greet\n!pewpew\n!pizzabites'
        await ctx.send(response)

##############################################

    @commands.command()
    async def greet(self, ctx):
        response = await ctx.reply("Hola")
        await response.add_reaction("👋")
    @commands.command()
    async def pewpew(self, ctx):
        response = 'Pew Pew, Pew Pew Pew Pew Pew'
        await ctx.send(response)
    @commands.command()
    async def pizzabites(self, ctx):
        response = await ctx.send('PizzaBALLs!!')
        await response.add_reaction("🍕")
        await response.add_reaction("🏀")

##############################################
async def setup(bot):
    await bot.add_cog(CustCommands(bot))