from .Welcome import welcome

def setup(bot):
    bot.add_cog(welcome(bot))
