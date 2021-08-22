import discord
from typing import Union


from redbot.core import  Config, commands, checks


class Welcome(commands.Cog):
    default_whisper = "Hey there {member.name}, welcome to {server.name}!"
    default_join = "{member.mention} https://cdn.discordapp.com/attachments/865760307087409155/879030917472067624/Miia_Greeting.mp4"
    guild_defaults = {"channel": None, "enabled": False,
    "join": {
            "enabled": True,
            "channel": None,
            "delete": False,
            "last": None,
            "counter": 0,
            "whisper": {"state": "off", "message": default_whisper},
            "messages": [default_join],
            "bot": None,
        }
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
        channel = await self.__get_channel(guild)
        
        user =  Union[discord.Member, discord.User]
        #await self.__dm_user(member, user)
        message = "{member.mention} https://cdn.discordapp.com/attachments/865760307087409155/879030917472067624/Miia_Greeting.mp4"
        #channel = guild.system_channel
        
        await self.__output_msg(guild, member, channel, message)
        
        #If you want to dm the person (was used for tests)
        #await self.__dm_user(member)
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
    
    async def __get_channel(self, guild: discord.Guild) -> discord.TextChannel:
        """Gets the best text channel to use for event notices.
        Order of priority:
        1. User-defined channel
        2. Guild's system channel (if bot can speak in it)
        3. First channel that the bot can speak in
        """

        channel = None
        
        channel_id: int = await self.config.guild(guild).channel()

        if channel_id is not None:
            channel = guild.get_channel(channel_id)

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

            channel = await self.__get_channel(guild)
            join_channel = await self.__get_channel(guild)

            j = c["join"]

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
                        f"**Enabled:** {j['enabled']}\n"
                        f"**Channel:** {join_channel.mention}\n"
                        f"**Delete previous:** {j['delete']}\n"
                        f"**Messages:** {len(j['messages'])}; do `{ctx.prefix}welcomeset join msg list` for a list\n"
                        f"**Bot message:** {j['bot']}"
                    ),
                )
                await ctx.send(embed=emb)
            else:
                msg = box(
                    f"  Enabled: {c['enabled']}\n"
                    f"  Channel: {channel}\n"
                    f"  Join:\n"
                    f"    Enabled: {j['enabled']}\n"
                    f"    Channel: {join_channel}\n"
                    f"    Delete previous: {j['delete']}\n"
                    "Current Welcome Settings",
                )

                await ctx.send(msg)
                
                
                

    @welcomeset.command(name="channel")
    async def welcomeset_channel(self, ctx: commands.Context, channel: discord.TextChannel) -> None:
        """Sets the channel to be used for event notices."""

        if not Welcome.__can_speak_in(channel):
            await ctx.send(
                f"I do not have permission to send messages in {channel.mention}. "
                "Check your permission settings and try again."
            )
            return

        guild = ctx.guild
        await self.config.guild(guild).channel.set(channel.id)

        await ctx.send(f"I will now send notices to {channel.mention}.")
        
        
        
    @staticmethod
    def __can_speak_in(channel: discord.TextChannel) -> bool:
        """Indicates whether the bot has permission to speak in channel."""

        return channel.permissions_for(channel.guild.me).send_messages

