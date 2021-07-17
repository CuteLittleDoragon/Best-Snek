import discord

class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot
        
        @Cog.listener()
        async def on_ready(self):
            if not self.bot.ready:
                self.bot.cogs_ready.ready_up("welcome")
                
        @Cog.listener()
        async def on_member_join(self, member):
            await member.send(f"Welcome to **{member.guild.name}**!")
            
                        
