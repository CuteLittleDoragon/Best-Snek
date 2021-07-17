from .Welcome import Welcome

import json

def setup(bot):
    n = Welcome(bot)
    bot.add_cog(n)
