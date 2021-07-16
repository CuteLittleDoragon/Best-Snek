from discord.ext.commands import Cog
from discord.ext.commands import commands

class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot
        
        @Cog.listener()
        async def on_ready(self):
            if not self.bot.ready:
                self.bot.cogs_ready.ready_up("welcome")
                
        @Cog.listener()
        asynce def on_member_join(self, member):
            for channel in member.server.channels:
                if channel.name == 'general':
                     await self.bot.send(f"Welcome to **{member.guild.name}** {member.mention}!")
                        
                        
def setup(bot):
    bot.add_cog(Welcome(bot))
