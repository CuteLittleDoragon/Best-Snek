from .Welcome import Welcome

import json

def setup(bot):
    n = Weather(bot)
    bot.add_cog(n)
