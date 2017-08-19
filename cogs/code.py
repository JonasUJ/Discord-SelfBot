import re
import traceback
import contextlib
import os
import discord
from threading import Timer
from subprocess import Popen, PIPE
from tempfile import TemporaryFile 
from io import StringIO
from discord.ext import commands
from utils import Utils


class Code:

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)

        # RegularExpression for detecting python code markdown
        self.code_expr = re.compile(r'```py\n([^```]+)')

    
    @commands.command()
    async def code(self, ctx, *, python):

        try:
            # Get code to run
            to_exec = self.code_expr.search(python).group(1).encode('utf-8')
        except AttributeError:
            # If the code markdown was improperly formatted
            return

        # Create TempFile and write code to it
        TempFile = TemporaryFile(delete=False)
        TempFile.write(to_exec)
        TempFile.close()

        # Open TempFile with Python
        process = Popen(['python', TempFile.name], shell=True, stdout=PIPE, stderr=PIPE)

        await ctx.message.edit(content='Processing...\n{}'.format(python))

        # Get output
        out = process.stdout.read().decode('utf-8')
        err = process.stderr.read().decode('utf-8')

        # Remove TempFile
        os.remove(TempFile.name)

        # Format output
        formatted_output = '```py\n{}{}```'.format(out, err)
        if formatted_output == '```py\n```': formatted_output = '```No output```'
        new_msg = '{}\nOutput:{}'.format(python, formatted_output)

        try:
            # Edit message
            await ctx.message.edit(content=new_msg)
        except discord.errors.HTTPException:
            await ctx.message.edit(content='Failed\n{}'.format(python))
        

   
    @commands.command()
    async def calc(self, ctx, *, expr):
        pass


def setup(bot):
    bot.add_cog(Code(bot))
