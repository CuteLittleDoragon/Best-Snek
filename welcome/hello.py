import discord
from redbot.core import  Config, commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")
                
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild: discord.Guild = member.guild
        channel_id: int = await self.config.guild(guild).channel()
        
        
        #channel = guild.system_channel
        
        #If you want to dm the person (was used for tests)
        #await self.__dm_user(member)
        await channel.send("hello")                  
    
    
    
    
    async def __dm_user(self, member: discord.Member):
        await member.send("hello")
        
            
    @commands.command()    
    async def test(self, ctx, echo: str, echo2: str):
        await ctx.send(echo + " " + echo2)
            
                        
