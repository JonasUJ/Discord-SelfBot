import json

class Utils:

    def __init__(self, bot=None):
        self.bot = bot
        with open('config.json') as f:
            self.config = json.load(f)


    def get_roles(self, guild_id:int, user_id:int):

        # Get guild and member by id
        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(user_id)

        # Yield every role the from member.roles in order from highest to lowest
        for role in guild.role_hierarchy:
            if role in member.roles:
                yield role