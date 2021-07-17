import discord
from redbot.core import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        @commands.Cog.listener()
        async def on_ready(self):
            if not self.bot.ready:
                self.bot.cogs_ready.ready_up("welcome")
                
        @commands.Cog.listener()
        async def on_member_join(member):
            await self.bot.get_channel(696799466220421191).send(f"Hello")
            
                        
