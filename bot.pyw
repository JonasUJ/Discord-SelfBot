import discord
import json
from discord.ext.commands import Bot
from discord import abc


bot = Bot(command_prefix='<<', self_bot=True)

with open('config.json') as f:
    config = json.load(f)


def is_self(other_id):

    # Compare other_id with our own id
    return other_id == bot.user.id


def get_roles(guild_id:int, user_id:int):

    # Get guild and member by id
    guild = bot.get_guild(guild_id)
    member = guild.get_member(user_id)

    # Yield every role the from member.roles in order from highest to lowest
    for role in guild.role_hierarchy:
        if role in member.roles:
            yield role


@bot.command()
async def embed(ctx):
    pass # Not implemented


@bot.command()
async def quote(ctx, msg_id:int, *, content=''):

    # Get message by id
    msg = ''
    async for prev in ctx.channel.history(limit=None):
        if msg_id == prev.id:
            msg = prev
            break

    # If no message matching id
    if not msg:
        await ctx.message.delete()
        await ctx.channel.send(content)
        return

    # Get author of message
    quoted = msg.author
    quoted_roles = get_roles(ctx.guild.id, quoted.id)

    # Get colour of authors highest role
    colour = discord.Colour.default()
    for role in quoted_roles:
        colour = role.colour
        break

    # Generate embed
    emb = discord.Embed(colour=colour, timestamp=msg.created_at)
    emb.add_field(name='Said:', value=msg.content)
    emb.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)

    # Delete command and send result
    await ctx.message.delete()
    await ctx.channel.send(**{'content': content, 'embed': emb})


@bot.event
async def on_message(msg):

    # Self-Bots should only react to your actions
    # Check if the message author is_self
    if is_self(msg.author.id):
        await bot.process_commands(msg)


@bot.event
async def on_ready():
    print('Logged in as:', bot.user.name)
    print('User id:', bot.user.id)
    print('--------')


bot.run(config['token'], bot=False)

