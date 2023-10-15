import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

WelcTitle = os.getenv("WelcTitle")

class CustEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1162273553341755504)
        emb = discord.Embed(title=WelcTitle, description = f"Welcome in {member.mention}!")
        welcmsg = await channel.send(embed=emb)
        await welcmsg.add_reaction("👋")
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(1162502898618466315)
        departmsg = await channel.send(f"{member} has left Thee Nest")
        await departmsg.add_reaction("🤝")
    
async def setup(bot):
    await bot.add_cog(CustEvents(bot))