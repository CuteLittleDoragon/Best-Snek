from redbot.core.bot import Red
from .submit import submit


def setup(bot: Red):
    bot.add_cog(submit(bot))
