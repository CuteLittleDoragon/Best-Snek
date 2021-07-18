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
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.guild.system_channel
        await self.__dm_user(member, channel)
        #await channel.send("hello")                  
    
    
    
    
    async def __dm_user(self, member: discord.Member, channel):
        await member.send("hello")
        await member.send(channel)
        
            
    @commands.command()    
    async def test(self, ctx, echo: str, echo2: str):
        await ctx.send(echo + " " + echo2)
            
                        
