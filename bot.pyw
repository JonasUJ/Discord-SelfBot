import json
import os
import asyncio
import discord
import utils as U
from discord.ext.commands import Bot


utils = U.Utils()
bot = Bot(command_prefix=utils.config['command_prefix'], self_bot=True)
utils.bot = bot


def is_self(other_id):

    # Compare other_id with our own id
    return other_id == bot.user.id


@bot.command()
async def exit(ctx):

    # Close the bot
    await ctx.message.delete()
    await bot.close()


@bot.event
async def on_message(msg):

    # Self-Bots should only react to your actions
    # Check if the message author is_self
    if is_self(msg.author.id):
        await bot.process_commands(msg)


@bot.event
async def on_ready():

    # Print something to let us know the bot has started
    print('Logged in as:', bot.user.name)
    print('User id:', bot.user.id)
    print('--------')


if __name__ == '__main__':

    # Load extensions
    for cog in os.listdir('cogs'):
        name, extension = os.path.splitext(cog)
        if extension == '.py':
            bot.load_extension('cogs.{}'.format(name))

    # Launch bot
    bot.run(utils.config['token'], bot=False)
