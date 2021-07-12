import datetime
from typing import Literal, Optional
from urllib.parse import urlencode

import aiohttp
import discord
from discord.ext.commands.errors import BadArgument
from redbot.core import Config, checks, commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Weather", __file__)



@cog_i18n(_)
class Weather(commands.Cog):
    """Get weather data from https://openweathermap.org"""

    __author__ = ["Doragon"]
    __version__ = "1.00"

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

    async def get_weather(
        self,
        ctx: commands.Context,
        *,
        location: Optional[str] = None,
    ) -> None:
        author = ctx.message.author
        bot_units = await self.config.units()
        units = "metric"
        params = {"appid": "88660f6af079866a3ef50f491082c386", "units": units}
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
        windspeed = str(data["wind"]["speed"]) + " " + self.unit[units]["speed"]
        city = data["name"]
        embed = discord.Embed(colour=discord.Colour.blue())
        try:
            country = data["sys"]["country"]
        except KeyError:
            country = ""
        lat, lon = data["coord"]["lat"], data["coord"]["lon"]
        condition = ", ".join(info["main"] for info in data["weather"])
        if len(city) and len(country):
            embed.add_field(name=_("🌍 **Location**"), value="{0}, {1}".format(city, country))
        else:
            embed.add_field(
                name=_("🌍 **Location**"), value=_("*Unavailable*")
            )
        embed.add_field(name=_("☁️ **Condition**"), value=condition)
        embed.add_field(
            name=_("🌡️ **Current Temperature**"),
            value="{0:.2f}{1}".format(currenttemp, self.unit[units]["temp"]),
        )
        embed.add_field(
            name=_("⬇️ **Lowest Temperature**"),
            value="{0:.2f}{1}".format(mintemp, self.unit[units]["temp"]),
                  )
        embed.add_field(
            name=_("⬆️ **Highest Temperature**"),
            value="{0:.2f}{1}".format(maxtemp, self.unit[units]["temp"]),
                  )
        embed.add_field(name=_("💨 **Wind Speed**"), value="{0}".format(windspeed))
        await ctx.send(embed=embed)
