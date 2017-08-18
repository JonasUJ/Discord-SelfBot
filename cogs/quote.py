import discord
from discord.ext import commands
from utils import Utils


class Quote:

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(bot)

    @commands.command()
    async def quote(self, ctx, msg_id:int, *, content=''):
        '''Send an embedded version of the message with id msg_id'''

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

        # Get roles of the message author
        author_roles = self.utils.get_roles(ctx.guild.id, ctx.message.author.id)

        # Get colour of authors highest role
        colour = discord.Colour.default()
        for role in author_roles:
            colour = role.colour
            break

        # Generate embed
        emb = discord.Embed(colour=colour)
        emb.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url)
        if msg.content:
            emb.add_field(name='Said:', value=msg.content)

        atts = []
        has_image = False
        for att in msg.attachments:
            if att.filename.split('.')[1].lower() in ['jpg', 'jpeg', 'png', 'gif'] and not has_image:
                emb.set_image(url=att.url)
                has_image = True
            else:
                atts.append(att.url)
        
        if atts:
            emb.add_field(name='Attachments:', value='\n'.join(atts))

        if self.utils.config['cogs']['quote']['timestamp']:
            emb.timestamp = msg.created_at

        # Delete command and send result
        await ctx.message.delete()
        await ctx.channel.send(content=content, embed=emb)


def setup(bot):
    bot.add_cog(Quote(bot))
