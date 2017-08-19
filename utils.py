import json

class Utils:

    def __init__(self, bot=None):

        # Define standard configs
        # Used if config.json is missing an item
        self.STANDARD = {
            "token": "No Token",
            "command_prefix": "<<",
            "cogs": {
                "quote": {
                    "timestamp": False
                },
                "cse": {
                    "google_api_key": "No API Key",
                    "google_cse_id": "No CSE ID"
                },
                "code": {
                    "timeout": 5
                }
            }
        }
        
        def setitems(dic: dict, standard: dict):
            '''Recursivly generate a dictionary from dic with fallback to standard'''

            res = {}
            for k, v in standard.items():
                if isinstance(v, dict):
                    if dic.get(k):
                        res[k] = setitems(dic[k], standard[k])
                    else:
                        res[k] = standard[k]
                else:
                    try:
                        res[k] = dic[k]
                    except KeyError:
                        res[k] = v

            return res

        self.bot = bot
        with open('config.json') as f:
            self.loaded = json.load(f)

        self.config = setitems(self.loaded, self.STANDARD)


    def get_roles(self, guild_id: int, user_id: int):
        '''Return the roles of user with id user_id in guild with id guild_id'''

        # Get guild and member by id
        guild = self.bot.get_guild(guild_id) 
        member = guild.get_member(user_id)

        # Yield every role the from member.roles in order from highest to lowest
        for role in guild.role_hierarchy:
            if role in member.roles:
                yield role
