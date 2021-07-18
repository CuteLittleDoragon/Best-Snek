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
    async def on_member_join(self, member: discord.Member) -> None:
        await self.__dm_user(member)
    
    
    
    
    async def __dm_user(self, member: discord.Member) -> None:
        """Sends a DM to the user with a filled-in message_format."""

        message_format = await self.config.guild(member.guild).join.whisper.message()

        try:
            await member.send(message_format.format(member=member, server=member.guild))
            
    @commands.command()    
    async def test(self, ctx, echo: str, echo2: str):
        await ctx.send(echo + " " + echo2)
            
                        
