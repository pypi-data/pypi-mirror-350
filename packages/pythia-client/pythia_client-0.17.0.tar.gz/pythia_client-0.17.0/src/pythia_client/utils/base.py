"""Base classes for services."""


class BaseService:
    """Base class for all services."""

    def __init__(self, url: str, api_key: str):
        """Initialize the service with the API URL and key.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        self.url = url
        self.api_key = api_key

    def _process_error_response(self, response):
        """Process error responses from the API.

        Args:
            response: The response object from the API.

        Returns:
            The error detail as a string.
        """
        try:
            # Try to parse the response as JSON
            error_detail = response.json()["detail"]
            return error_detail
        except Exception as e:
            # If JSON parsing fails, capture the raw response content
            try:
                error_detail = response.text
                return error_detail
            except Exception:
                # Catch any other exceptions
                error_detail = str(e)
                return error_detail
