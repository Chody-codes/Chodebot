import discord
from discord.ext import commands

class ReactionRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reactionroles")
    async def create_reaction_roles_message(self, ctx):
        # Get the message channel.
        channel = ctx.channel

        # Send the embed message.
        message = await channel.send(embed=self.create_embed())

        # Add the reaction emojis.
        await message.add_reaction("🍎")
        await message.add_reaction("🍌")
        await message.add_reaction("🍊")

    def create_embed(self):
        embed = discord.Embed(title="Embedded Reaction Message")
        embed.add_field(name="Apple", value="🍎", inline=True)
        embed.add_field(name="Banana", value="🍌", inline=True)
        embed.add_field(name="Orange", value="🍊", inline=True)
        return embed

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Check if the reaction was added to the specific message.
        if reaction.message.id != self.message_id:
            return

        # Check if the reaction is one of the emojis that we have configured for our reaction role system.
        if reaction.emoji not in self.reaction_roles:
            return

        # Get the corresponding role.
        role = discord.utils.get(user.guild.roles, name=self.reaction_roles[reaction.emoji])

        # Add the role to the user.
        await user.add_roles(role)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        # Check if the reaction was removed from the specific message.
        if reaction.message.id != self.message_id:
            return

        # Check if the reaction is one of the emojis that we have configured for our reaction role system.
        if reaction.emoji not in self.reaction_roles:
            return

        # Get the corresponding role.
        role = discord.utils.get(user.guild.roles, name=self.reaction_roles[reaction.emoji])

        # Remove the role from the user.
        await user.remove_roles(role)

# Add the cog to the bot.
async def setup(bot):
    await bot.add_cog(ReactionRoleCog(bot))
