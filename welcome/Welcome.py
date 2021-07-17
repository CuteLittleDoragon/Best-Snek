from redbot.core import commands
import discord

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        @commands.Cog.listener()
        async def on_ready(self):
            if not self.bot.ready:
                self.bot.cogs_ready.ready_up("welcome")
                
        @commands.Cog.listener()
        async def on_member_join(self, member, ctx: commands.Context,):
            await ctx.send(f"Welcome to **{member.guild.name}**!")
            
        @commands.command()    
        async def test(self, ctx, echo: str, echo2: str):
            await ctx.send(echo + " " + echo2)
            
                        
