import datetime
from typing import Literal, Optional
from urllib.parse import urlencode

import aiohttp
import discord
from discord.ext.commands.converter import Converter
from discord.ext.commands.errors import BadArgument
from redbot.core import Config, checks, commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Weather", __file__)


class UnitConverter(Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> Optional[str]:
        new_units = None
        if argument.lower() in ["f", "imperial", "mph"]:
            new_units = "imperial"
        elif argument.lower() in ["c", "metric", "kph"]:
            new_units = "metric"
        elif argument.lower() in ["k", "kelvin"]:
            new_units = "kelvin"
        elif argument.lower() in ["clear", "none"]:
            new_units = None
        else:
            raise BadArgument(_("`{units}` is not a vaild option!").format(units=argument))
        return new_units


@cog_i18n(_)
class Weather(commands.Cog):
    """Get weather data from https://openweathermap.org"""

    __author__ = ["TrustyJAID"]
    __version__ = "1.2.1"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 138475464)
        default = {"units": None}
        self.config.register_global(**default)
        self.config.register_guild(**default)
        self.config.register_user(**default)
        self.unit = {
            "metric": {"code": ["m", "c"], "speed": "km/h", "temp": " °C"}
        }

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ):
        """
        Method for finding users data inside the cog and deleting it.
        """
        await self.config.user_from_id(user_id).clear()

    @commands.group(name="weather", aliases=["we"], invoke_without_command=True)
    @commands.bot_has_permissions(embed_links=True)
    async def weather(self, ctx: commands.Context, *, location: str) -> None:
        """
        Display weather in a given location
        `location` must take the form of `city, Country Code`
        example: `[p]weather New York,US`
        """
        await ctx.trigger_typing()
        await self.get_weather(ctx, location=location)

    @weather.command(name="zip")
    @commands.bot_has_permissions(embed_links=True)
    async def weather_by_zip(self, ctx: commands.Context, *, zipcode: str) -> None:
        """
        Display weather in a given location
        `zipcode` must be a valid ZIP code or `ZIP code, Country Code` (assumes US otherwise)
        example: `[p]weather zip 20500`
        """
        await ctx.trigger_typing()
        await self.get_weather(ctx, zipcode=zipcode)

    @weather.command(name="cityid")
    @commands.bot_has_permissions(embed_links=True)
    async def weather_by_cityid(self, ctx: commands.Context, *, cityid: int) -> None:
        """
        Display weather in a given location
        `cityid` must be a valid openweathermap city ID
        (get list here: <https://bulk.openweathermap.org/sample/city.list.json.gz>)
        example: `[p]weather cityid 2172797`
        """
        await ctx.trigger_typing()
        await self.get_weather(ctx, cityid=cityid)

    @weather.command(name="co", aliases=["coords", "coordinates"])
    @commands.bot_has_permissions(embed_links=True)
    async def weather_by_coordinates(self, ctx: commands.Context, lat: float, lon: float) -> None:
        """
        Display weather in a given location
        `lat` and `lon` specify a precise point on Earth using the
        geographic coordinates specified by latitude (north-south) and longitude (east-west).
        example: `[p]weather coordinates 35 139`
        """
        await ctx.trigger_typing()
        await self.get_weather(ctx, lat=lat, lon=lon)

    @commands.group(name="weatherset")
    async def weather_set(self, ctx: commands.Context) -> None:
        """Set user or guild default units"""
        pass

    async def get_weather(
        self,
        ctx: commands.Context,
        *,
        location: Optional[str] = None,
        zipcode: Optional[str] = None,
    ) -> None:
        guild = ctx.message.guild
        author = ctx.message.author
        bot_units = await self.config.units()
        guild_units = None
        if guild:
            guild_units = await self.config.guild(guild).units()
        user_units = await self.config.user(author).units()
        units = "imperial"
        if bot_units:
            units = bot_units
        if guild_units:
            units = guild_units
        if user_units:
            units = user_units
        params = {"appid": "88660f6af079866a3ef50f491082c386", "units": units}
        if zipcode:
            params["zip"] = str(zipcode)
        else:
            params["q"] = str(location)
        url = "https://api.openweathermap.org/data/2.5/weather?{0}".format(urlencode(params))
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
        try:
            if data["message"] == "city not found":
                await ctx.send("City not found.")
                return
        except Exception:
            pass
        currenttemp = data["main"]["temp"]
        mintemp = data["main"]["temp_min"]
        maxtemp = data["main"]["temp_max"]
        city = data["name"]
        embed = discord.Embed(colour=discord.Colour.blue())
        try:
            country = data["sys"]["country"]
        except KeyError:
            country = ""
        lat, lon = data["coord"]["lat"], data["coord"]["lon"]
        condition = ", ".join(info["main"] for info in data["weather"])
        embed.set_footer(text=_("Powered by https://openweathermap.org"))
        await ctx.send(embed=embed)
