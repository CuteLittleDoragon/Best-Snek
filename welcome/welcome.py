from redbot.core import commands

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
            
            
        async def totest(self, ctx: commands.Context):
        """
        Display weather in a given location
        `location` must take the form of `city, Country Code`
        example: `[p]weather New York,US`
        """
            await ctx.send("hello")
            
                        
