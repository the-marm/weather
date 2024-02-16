"""Module defines the exceptions used in the application.

Exceptions:
    ApiServiceError: Raised when an error occurs while calling an API.
"""


class ApiServiceError(Exception):
    """Custom exception type for errors related to API calls."""


class GetCoordinatesError(Exception):
    """Raised when the user's coordinates cannot be retrieved."""
