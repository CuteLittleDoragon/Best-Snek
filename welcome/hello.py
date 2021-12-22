import discord
from typing import Union


from redbot.core import  Config, commands, checks
default_join = "\n https://cdn.discordapp.com/attachments/866485084660301833/879501914826485800/Excited_Miia.gif"
default_prefix = "Welcome to the server"
default_leave = "bye"

class Welcome(commands.Cog):
    default_whisper = "Hey there {member.name}, welcome to {server.name}!"
    
    guild_defaults = {"channel": None, "join_channel": None, "leave_channel": None, "enabled": False, "join_msg": default_join, "join_prefix": default_prefix
                     }                  
    
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 123456788)
        self.config.register_guild(**self.guild_defaults)
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")
                
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild: discord.Guild = member.guild
        channel = await self.__get_channel(guild, "join")
        
        user =  Union[discord.Member, discord.User]
        #await self.__dm_user(member, user)
        message = await self.config.guild(member.guild).join_prefix() + ", {member.mention}!" + " " + await self.config.guild(member.guild).join_msg()
        #channel = guild.system_channel
        
        await self.__output_msg(guild, member, channel, message)
        
        #If you want to dm the person (was used for tests)
        #await self.__dm_user(member)
        #await channel.send(message.format(member=user))                  
    
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        guild: discord.Guild = member.guild
        channel = await self.__get_channel(guild, "leave")
        message = "**{member}** just left the server! \n https://cdn.discordapp.com/attachments/865760307087409155/892171125130424391/Screenshot_1031.png"
        
        await self.__output_msg(guild, member, channel, message)
        
        #If you want to dm the person (was used for tests)
        
        #await channel.send(message.format(member=user))    
    
    
    async def __output_msg(self, guild: discord.guild, user: Union[discord.Member, discord.User], channel, message):
        await channel.send(message.format(member=user))     
    
    async def __dm_user(self, member: discord.Member, msg):
        await member.send("hello")
        await member.send(msg)
        
            
    @commands.command()    
    async def test(self, ctx, echo: str, echo2: str):
        await ctx.send(echo + " " + echo2)
            
    @commands.command()
    async def my_chance(self, ctx: commands.Context, channel: discord.TextChannel):
        await channel.send("https://cdn.discordapp.com/attachments/865760307087409155/879031015866261514/One_Less_Rival.mp4")
    
    async def __get_channel(self, guild: discord.Guild, event_type: str) -> discord.TextChannel:
        """Gets the best text channel to use for event notices.
        Order of priority:
        1. User-defined channel
        2. Guild's system channel (if bot can speak in it)
        3. First channel that the bot can speak in
        """

        channel = None
        
        channel_id: int = await self.config.guild(guild).channel()

        if channel_id is not None:
            if event_type == "join":
                channel = guild.get_channel(await self.config.guild(guild).join_channel())
            elif event_type == "leave":
                channel = guild.get_channel(await self.config.guild(guild).leave_channel())
            else:
                channel = guild.get_channel(await self.config.guild(guild).channel())

        if channel is None or not Welcome.__can_speak_in(channel):
            channel = guild.get_channel(await self.config.guild(guild).channel())

        if channel is None or not Welcome.__can_speak_in(channel):
            channel = guild.system_channel

        if channel is None or not Welcome.__can_speak_in(channel):
            for ch in guild.text_channels:
                if Welcome.__can_speak_in(ch):
                    channel = ch
                    break

        return channel


    
    @commands.group(aliases=["welcome"])
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    async def welcomeset(self, ctx: commands.Context) -> None:
        """Change Welcome settings."""

        await ctx.trigger_typing()

        if ctx.invoked_subcommand is None:
            guild: discord.Guild = ctx.guild
            c = await self.config.guild(guild).all()
            
            join_channel = await self.__get_channel(guild, "join")
            channel = await self.__get_channel(guild, "none")
            leave_channel = await self.__get_channel(guild, "leave")
   

            if await ctx.embed_requested():
                emb = discord.Embed(color=await ctx.embed_color(), title="Current Welcome Settings")
                emb.add_field(
                    name="General",
                    inline=False,
                    value=f"**Enabled:** {c['enabled']}\n**Channel:** {channel.mention}\n",
                    )
                emb.add_field(
                    name="Join",
                    inline=False,
                    value=(
                        f"**Channel:** {join_channel.mention}\n"
                    ),
                )
                emb.add_field(
                    name="Leave",
                    inline=False,
                    value=(
                        f"**Channel:** {leave_channel.mention}\n"
                ),
                )
                await ctx.send(embed=emb)
            else:
                msg = box(
                    f"  Enabled: {c['enabled']}\n"
                    f"  Channel: {channel}\n"
                    f"  Join:\n"
                    f"    Channel: {join_channel}\n"
                    f"  Leave:\n"
                    f"    Channel: {leave_channel}\n"
                    "Current Welcome Settings",
                )

                await ctx.send(msg)
                
                
                

    @welcomeset.command(name="join")
    async def welcomeset_join(self, ctx: commands.Context, channel: discord.TextChannel) -> None:
        """Sets the channel to be used for event notices."""

        if not Welcome.__can_speak_in(channel):
            await ctx.send(
                f"I do not have permission to send messages in {channel.mention}. "
                "Check your permission settings and try again."
            )
            return

        guild = ctx.guild
        await self.config.guild(guild).join_channel.set(channel.id)

        await ctx.send(f"I will now send join notices to {channel.mention}.")
    
    @welcomeset.command(name="join_reset")
    async def welcomeset_join_reset(self, ctx: commands.Context) -> None:
        """Sets the channel to be used for event notices."""

        guild = ctx.guild
        await self.config.guild(guild).join_msg.set(default_join)
        await self.config.guild(guild).join_prefix.set(default_prefix)

        await ctx.send(f"Join has been reset!")
    
    @welcomeset.command(name="join_msg")
    async def welcomeset_join_msg(self, ctx: commands.Context, msg: str) -> None:
        """Sets the channel to be used for event notices."""

        guild = ctx.guild
        await self.config.guild(guild).join_msg.set(msg)

        await ctx.send(f"Join Message Changed!")
        
    @welcomeset.command(name="join_prefix")
    async def welcomeset_join_prefix(self, ctx: commands.Context, prefix: str) -> None:
        """Sets the channel to be used for event notices."""

        guild = ctx.guild
        await self.config.guild(guild).join_prefix.set(prefix)

        await ctx.send(f"Join Prefix Changed!")
    
    @welcomeset.command(name="leave")
    async def welcomeset_leave(self, ctx: commands.Context, channel: discord.TextChannel) -> None:
        """Sets the channel to be used for event notices."""

        if not Welcome.__can_speak_in(channel):
            await ctx.send(
                f"I do not have permission to send messages in {channel.mention}. "
                "Check your permission settings and try again."
            )
            return

        guild = ctx.guild
        await self.config.guild(guild).leave_channel.set(channel.id)

        await ctx.send(f"I will now send leave notices to {channel.mention}.")
        
        
    @staticmethod
    def __can_speak_in(channel: discord.TextChannel) -> bool:
        """Indicates whether the bot has permission to speak in channel."""

        return channel.permissions_for(channel.guild.me).send_messages

