from discord.ext import commands

print('test test can you see me')

class WordGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_dict = {}
        self.last_user_dict = {}
        self.sentence_dict = {}
        self.channelbeenset = False
        self.firstpass = True

    def channel_check(self, ctx):
        return ctx.channel == self.channel_dict[ctx.guild.id]

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message.author.name, message.content)
        # DEBUGGING
        print(f"beginning of \'loop\':")  # {self.sentence_dict[message.channel.id]}")

        # Check if we're in the right channel
        if not self.channel_check(message):
            print('channel isn\'t the right channel')
            return

        # Check if bot msg
        if message.author == self.bot.user:
            print('bots text will be ignored')
            return

        # Check for blank word
        if not message.content:
            # The player's word is empty
            response = await message.channel.send('Please enter a word.')
            response.delete_after(20)
            return

        # Check if the last user to input a word is the same user who is sending the current message
        if self.last_user_dict[message.channel.id] == message.author:
            print('second entry in a row')
            await message.channel.send('You cannot submit two words consecutively.')
            return

        # Check if the length is too long
        if len(message.content) > 20:
            # The player's word is too long
            response = await message.channel.send('Please enter a word that is no longer than 20 characters.')
            response.delete_after(20)
            message.delete_after(20)
            return

        # Valid entry
        print('valid entry')

        # Add the message to the sentence
        self.sentence_dict[message.channel.id].append(message.content)
        print(self.sentence_dict[message.channel.id])

        # Set the last user to input a word
        self.last_user_dict[message.channel.id] = message.author
        print(self.last_user_dict[message.channel.id])

        if message.content.endswith('.') or message.content.endswith('!') or message.content.endswith('?'):
            # We end the sentence
            await message.channel.send(f'The sentence is:\n{" ".join(self.sentence_dict[message.channel.id])}')

            # Clear sentence
            self.sentence_dict[message.channel.id] = []

            # Clear last user, so they can put in first word next round
            self.last_user_dict[message.channel.id] = None

            print(f'{self.sentence_dict[message.channel.id]}, {self.last_user_dict[message.channel.id]}')
            return

        # If I see this message in the console it's because we're still playing
        print('not the end of sentence')

    @commands.command()
    async def wchannel(self, ctx, message):
        """Sets the channel for the Word Game"""
        # Check for mod or admin priv

        # role = ctx.guild.get_role(1050511898384277535)
        # if role in ctx.author.roles or ctx.author.guild_permissions.administrator:
        if not ctx.author.guild_permissions.administrator:
            # The user does not have the administrator permission
            await ctx.author.send('You do not have permission to start the word game.')
            print(f"lack of privs prevents {message.author} from setting the channel")
            return

        # Add the current channel to the channel dictionary
        self.channel_dict[ctx.guild.id] = message.channel

        # Create a new dictionary to store the last_user and sentence for this channel
        self.last_user_dict[message.channel.id] = None
        self.sentence_dict[message.channel.id] = []

        # Send a message to the channel to let everyone know that the word game has started
        await message.channel.send('The word game has started in this channel!')
        print(f"{message.author} has set the channel")

    @commands.command()
    async def stop_game(self, ctx, message):
        """Stops the word game in the current channel"""
        # Check for mod or admin priv
        if not ctx.author.guild_permissions.administrator:
            # The user does not have the administrator permission
            await ctx.author.send('You do not have permission to stop the word game.')
            print(f"lack of privs prevents {message.author} from removing the channel")
            return
        try:
            # Delete the channel from dictionary
            del self.channel_dict[ctx.guild.id]
            # Lets users know the game is stopped in the channel
            await ctx.send('The word game has been stopped in this channel.')
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await ctx.send(f"Failed to stop{self.channel_dict[ctx.guild.id]}({exc}), are you sure this channel has been started?")


async def setup(bot):
    await bot.add_cog(WordGame(bot))
