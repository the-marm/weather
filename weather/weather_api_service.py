"""Module provides functionality for retrieving weather data from OpenWeatherMap API.

It contains the following classes:
- Weather: A class that holds weather information for a specific location.
- Coordinates: A class that holds geographic coordinates.

It contains the following functions:
- get_weather: A function that fetches weather data for the given coordinates.
"""

import json
import urllib
import urllib.request
from datetime import datetime, timezone
from enum import Enum
from json.decoder import JSONDecodeError
from typing import Literal, NamedTuple
from urllib.error import URLError

from weather import config
from weather.coordinates import Coordinates
from weather.exceptions import ApiServiceError

Celcius = float


class WeatherType(Enum):
    """Represents different weather conditions."""

    THUNDERSHTORM = "Thundershtorm"
    DRIZZLE = "Drizzle"
    RAIN = "Rain"
    SNOW = "Snow"
    CLEAR = "Clear"
    FOG = "Fog"
    CLOUDS = "Clouds"


class Weather(NamedTuple):
    """Holds weather information for a specific location.

    Attributes
    ----------
        weather_type (WeatherType): The current weather condition.
        city (str): The city name.
        temperature (float): The current temperature in Celsius.
        sunrise (datetime): The sunrise time in UTC.
        sunset (datetime): The sunset time in UTC.

    """

    weather_type: WeatherType
    city: str
    temperature: Celcius
    sunrise: datetime
    sunset: datetime


def get_weather(coordinates: Coordinates) -> Weather:
    """Retrieve weather data for the given coordinates.

    Args:
    ----
        coordinates (Coordinates): The geographic coordinates.

    Returns:
    -------
        Weather: A Weather object containing the weather information.

    Raises:
    ------
        ApiServiceError: If an error occurs while fetching or parsing the data.

    """
    owm_response = _get_owm_response(coordinates.latitude, coordinates.longitude)
    return _parse_owm_response(owm_response)


def _get_owm_response(latitude: float, longitude: float) -> str:
    """Fetch raw weather data from OpenWeatherMap API.

    Args:
    ----
        latitude (float): The latitude coordinate.
        longitude (float): The longitude coordinate.

    Returns:
    -------
        str: The raw JSON response from the OpenWeatherMap API.

    Raises:
    ------
        ApiServiceError: If an error occurs during the network request.

    """
    url = config.OWM_URL.format(latitude=latitude, longitude=longitude)

    try:
        response = urllib.request.urlopen(url)
        return response.read().decode()
    except URLError as e:
        raise ApiServiceError from e


def _parse_owm_response(response: str) -> Weather:
    """Parse the raw JSON response into a Weather object.

    Args:
    ----
        response (str): The raw JSON response from the OpenWeatherMap API.

    Returns:
    -------
        Weather: A Weather object containing the weather information.

    Raises:
    ------
        ApiServiceError: If an error occurs while parsing the JSON data.

    """
    try:
        owm_dict = json.loads(response)
    except JSONDecodeError as e:
        raise ApiServiceError from e

    return Weather(
        weather_type=_parse_weather_type(owm_dict),
        city=_parse_city(owm_dict),
        temperature=_parse_temperature(owm_dict),
        sunrise=_parse_sun_time(owm_dict, "sunrise"),
        sunset=_parse_sun_time(owm_dict, "sunset"),
    )


def _parse_weather_type(owm_dict: dict) -> WeatherType:
    """Parse the weather type from the OpenWeatherMap API response.

    Args:
    ----
        owm_dict (dict): The parsed JSON response dictionary.

    Returns:
    -------
        WeatherType: The corresponding weather type.

    Raises:
    ------
        ApiServiceError: If the weather type cannot be determined.

    """
    try:
        weather_type_id = str(owm_dict["weather"][0]["id"])
    except (IndexError, KeyError) as e:
        raise ApiServiceError from e

    weather_types = {
        "1": WeatherType.THUNDERSHTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS,
    }

    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type

    raise ApiServiceError


def _parse_city(owm_dict: dict) -> str:
    """Parse the city name from the OpenWeatherMap API response.

    Args:
    ----
        owm_dict (dict): The parsed JSON response dictionary.

    Returns:
    -------
        str: The city name.

    Raises:
    ------
        ApiServiceError: If the city name cannot be found.

    """
    try:
        return owm_dict["name"]
    except KeyError as e:
        raise ApiServiceError from e


def _parse_temperature(owm_dict: dict) -> Celcius:
    """Parse the temperature from the OpenWeatherMap API response.

    Args:
    ----
        owm_dict (dict): The parsed JSON response dictionary.

    Returns:
    -------
        float: The temperature in Celsius.

    Raises:
    ------
        ApiServiceError: If the temperature cannot be found.

    """
    try:
        return owm_dict["main"]["temp"]
    except KeyError as e:
        raise ApiServiceError from e


def _parse_sun_time(owm_dict: dict, time: Literal["sunrise", "sunset"]) -> datetime:
    """Parse the sunrise or sunset time from the OpenWeatherMap API response.

    Args:
    ----
        owm_dict (dict): The parsed JSON response dictionary.
        time (str): The time of day to parse ("sunrise" or "sunset").

    Returns:
    -------
        datetime: The time in UTC.

    Raises:
    ------
        ApiServiceError: If the time cannot be found.

    """
    try:
        timestamp = owm_dict["sys"][time]
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    except KeyError as e:
        raise ApiServiceError from e
