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
        async def on_member_join(member: discord.Member):
            await member.send('Private message')
            
                        
