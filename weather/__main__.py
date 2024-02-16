"""Script is the entry point for a weather information application.

It fetches the user's coordinates and then retrieves weather data from a weather API.
"""

from sys import exit

from weather.coordinates import fetch_user_coordinates
from weather.exceptions import ApiServiceError, GetCoordinatesError
from weather.formatter import format_weather
from weather.weather_api_service import get_weather


def main() -> None:
    """Entry point of the application.

    It performs the following steps:
        1. Fetches the user's coordinates using the `fetch_user_coordinates` function.
        2. If coordinates are successfully fetched:
            * Retrieves weather data for the given coordinates.
        3. If any errors occur:
            * Exits the program with an exit code of 1.

    Raises
    ------
        GetCoordinatesError: If errors occur while fetching user coordinates.
        ApiServiceError: If errors occur while retrieving weather data.

    """
    try:
        coordinates = fetch_user_coordinates()
    except GetCoordinatesError:
        exit(1)

    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        exit(1)

    print(format_weather(weather))


if __name__ == "__main__":
    main()
