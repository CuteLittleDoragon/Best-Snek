from .hello import Welcome
  
from redbot.core.bot import Red


def setup(bot: Red):
    bot.add_cog(Welcome(bot))
