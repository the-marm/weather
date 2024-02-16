"""Module provides functions to fetch a user's coordinates based on their IP address.

Features:
    fetch_user_coordinates: Fetches the user's coordinates.

Exceptions:
    ApiServiceError: Raised if an error occurs while fetching the data.

"""

import json
import urllib.request
from json import JSONDecodeError
from typing import NamedTuple
from urllib.error import URLError

from weather.exceptions import GetCoordinatesError


class Coordinates(NamedTuple):
    """A namedtuple representing the latitude and longitude of a user."""

    latitude: float
    longitude: float


def fetch_user_coordinates() -> Coordinates:
    """Fetch the user's coordinates from IP API services.

    Raises
    ------
        ApiServiceError: If an error occurs while fetching the coordinates.

    Returns
    -------
        A Coordinates namedtuple containing the user's latitude and longitude.

    """
    user_ip = _fetch_user_ip()
    coordinates_data = _fetch_user_coordinates_data(user_ip)
    return Coordinates(coordinates_data["latitude"], coordinates_data["longitude"])


def _fetch_user_ip() -> str:
    """Fetch the user's IP address from the IPify API.

    Raises
    ------
        ApiServiceError: If an error occurs while fetching the IP address.

    Returns
    -------
        The user's IP address as a string.

    """
    url = "https://api64.ipify.org?format=json"
    try:
        response = urllib.request.urlopen(url)
        ip_data = response.read().decode()
        return _extract_ip_address(ip_data)
    except URLError as e:
        raise GetCoordinatesError from e


def _extract_ip_address(ip_data: str) -> str:
    """Extract the user's IP address from the JSON response of the IPify API.

    Raises
    ------
        ApiServiceError: If the JSON response is invalid or does not contain
        an IP address.

    Returns
    -------
        The user's IP address as a string.

    """
    try:
        ip_dict = json.loads(ip_data)
    except JSONDecodeError as e:
        raise GetCoordinatesError from e

    return ip_dict["ip"]


def _fetch_user_coordinates_data(user_ip: str) -> dict:
    """Fetch the user's coordinates data from the IP-API.com API.

    Raises
    ------
        ApiServiceError: If an error occurs while fetching the coordinates data.

    Returns
    -------
        A dictionary containing the user's coordinates data.

    """
    url = "https://ipapi.co/" + user_ip + "/json/"
    try:
        response = urllib.request.urlopen(url)
        coordinates_data = response.read().decode()
        return json.loads(coordinates_data)
    except URLError as e:
        raise GetCoordinatesError from e
