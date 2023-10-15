from discord.ext import commands


class WordGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.channelbeenset = False
        self.firstpass = True
        self.sentence = []
        self.last_user = []

    @commands.Cog.listener()
    async def on_message(self, message):
        # DEBUGGING
        print(f"beginning of \'loop\': {self.sentence}")
        # Check if first pass
        if self.firstpass and not self.channel:
            print('No channel set')
            self.firstpass = False
            return
        # Check if the message is a command
        if message.content.startswith('!'):
            print('message starts with a !')
            # Execute the command passed by author
            await self.bot.process_commands(message)
            # DEBUGGING
            print('tried to process_commands')
            # return
        # Check if we're in the right channel
        if message.channel != self.channel:
            if not self.channelbeenset:
                print('no channel has been set yet')
                return
            print('channel isn\'t the right channel')
        print('right channel')
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
        if self.last_user == message.author:
            print('second entry in a row')
            await message.channel.send('You cannot submit two words consecutively.')
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
        self.sentence.append(message.content)
        print(self.sentence)
        # Set the last user to input a word
        self.last_user = message.author
        print(self.last_user)

        if message.content.endswith('.') or message.content.endswith('!') or message.content.endswith('?'):
            # just a sane of mind check that the word is registering right, debugging
            print(f"sentence will be completed with {message}")
            # We end the sentence
            await message.channel.send(f'The sentence is:\n{" ".join(self.sentence)}')
            # Clear sentence
            self.sentence = []
            # Clear last user, so they can put in first word next round
            self.last_user = []
            # confirmation that the sentence and last_user is reset
            print(f'{self.sentence}, {self.last_user}')
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
            await ctx.author.send('You do not have permission to start the sentence game.')
            print(f"lack of privs prevents {message.author} from setting the channel")
            return
        # Set the current channel as the channel for the word game
        self.channel = message.channel
        # Send a message to the channel to let everyone know that the word game has started
        await message.channel.send('The word game has started!')
        print(f"{message.author} has set the channel")


async def setup(bot):
    await bot.add_cog(WordGame(bot))
