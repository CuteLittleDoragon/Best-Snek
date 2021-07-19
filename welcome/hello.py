import discord
from redbot.core import  Config, commands, checks


class Welcome(commands.Cog):
    guild_defaults = {"channel": None}
    
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
            
    
    async def __get_channel(self, guild: discord.Guild, event: str) -> discord.TextChannel:
        """Gets the best text channel to use for event notices.
        Order of priority:
        1. User-defined channel
        2. Guild's system channel (if bot can speak in it)
        3. First channel that the bot can speak in
        """

        channel = None

        if event == "default":
            channel_id: int = await self.config.guild(guild).channel()
        else:
            channel_id = await self.config.guild(guild).get_attr(event).channel()

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

            channel = await self.__get_channel(guild, "default")
            join_channel = await self.__get_channel(guild, "join")
            leave_channel = await self.__get_channel(guild, "leave")
            ban_channel = await self.__get_channel(guild, "ban")
            unban_channel = await self.__get_channel(guild, "unban")

            j = c["join"]
            jw = j["whisper"]
            v = c["leave"]
            b = c["ban"]
            u = c["unban"]

            whisper_message = jw["message"] if len(jw["message"]) <= 50 else jw["message"][:50] + "..."

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
                        f"**Whisper state:** {jw['state']}\n"
                        f"**Whisper message:** {whisper_message}\n"
                        f"**Messages:** {len(j['messages'])}; do `{ctx.prefix}welcomeset join msg list` for a list\n"
                        f"**Bot message:** {j['bot']}"
                    ),
                )
                emb.add_field(
                    name="Leave",
                    inline=False,
                    value=(
                        f"**Enabled:** {v['enabled']}\n"
                        f"**Channel:** {leave_channel.mention}\n"
                        f"**Delete previous:** {v['delete']}\n"
                        f"**Messages:** {len(v['messages'])}; do `{ctx.prefix}welcomeset leave msg list` for a list\n"
                    ),
                )
                emb.add_field(
                    name="Ban",
                    inline=False,
                    value=(
                        f"**Enabled:** {b['enabled']}\n"
                        f"**Channel:** {ban_channel.mention}\n"
                        f"**Delete previous:** {b['delete']}\n"
                        f"**Messages:** {len(b['messages'])}; do `{ctx.prefix}welcomeset ban msg list` for a list\n"
                    ),
                )
                emb.add_field(
                    name="Unban",
                    inline=False,
                    value=(
                        f"**Enabled:** {u['enabled']}\n"
                        f"**Channel:** {unban_channel.mention}\n"
                        f"**Delete previous:** {u['delete']}\n"
                        f"**Messages:** {len(u['messages'])}; do `{ctx.prefix}welcomeset unban msg list` for a list\n"
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
                    f"    Whisper:\n"
                    f"      State: {jw['state']}\n"
                    f"      Message: {whisper_message}\n"
                    f"    Messages: {len(j['messages'])}; do '{ctx.prefix}welcomeset join msg list' for a list\n"
                    f"    Bot message: {j['bot']}\n"
                    f"  Leave:\n"
                    f"    Enabled: {v['enabled']}\n"
                    f"    Channel: {leave_channel}\n"
                    f"    Delete previous: {v['delete']}\n"
                    f"    Messages: {len(v['messages'])}; do '{ctx.prefix}welcomeset leave msg list' for a list\n"
                    f"  Ban:\n"
                    f"    Enabled: {b['enabled']}\n"
                    f"    Channel: {ban_channel}\n"
                    f"    Delete previous: {b['delete']}\n"
                    f"    Messages: {len(b['messages'])}; do '{ctx.prefix}welcomeset ban msg list' for a list\n"
                    f"  Unban:\n"
                    f"    Enabled: {u['enabled']}\n"
                    f"    Channel: {unban_channel}\n"
                    f"    Delete previous: {u['delete']}\n"
                    f"    Messages: {len(u['messages'])}; do '{ctx.prefix}welcomeset unban msg list' for a list\n",
                    "Current Welcome Settings",
                )

                await ctx.send(msg)
