"""Module is responsible for displaying weather information.

It contains the following functions:
    format_weather(weather: Weather) -> str`: Formats weather data from a
    Weather object into a human-readable string.
"""

from weather.weather_api_service import Weather


def format_weather(weather: Weather) -> str:
    """Format weather data from a Weather object into a human-readable string.

    Args:
    ----
        weather (weather_api_service.Weather): An instance of the Weather class
            containing weather data.

    Returns:
    -------
        str: A formatted string containing the weather information.

    """
    return (
        "\n"
        f"{weather.city} - {weather.weather_type.value}:\n"
        f" - Temperature: {weather.temperature}°C\n"
        f" - Sunrise: {weather.sunrise.strftime('%H:%M')}\n"
        f" - Sunset: {weather.sunset.strftime('%H:%M')}"
        "\n"
    )
