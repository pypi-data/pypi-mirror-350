"""Pipeline operations functionality."""

import io
import requests
from urllib.parse import urljoin
from pythia_client.utils.base import BaseService


class PipelineService(BaseService):
    """Service for pipeline operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the pipeline service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.draw_endpoint = urljoin(str(self.url), "/draw")

    def draw_pipeline(self, pipeline_name) -> io.BytesIO:
        """Draw a PNG image of a specific Pythia pipeline.

        Args:
            pipeline_name: The name of the pipeline to draw.

        Returns:
            A BytesIO object containing the PNG image of the pipeline. Raise an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        image = client.draw_pipeline(pipeline_name="query")
        ```
        """
        with requests.Session() as session:
            headers = {"X-API-Key": self.api_key}
            with session.get(
                self.draw_endpoint + f"/{pipeline_name}",
                headers=headers,
            ) as response:
                if response.status_code == 200:
                    image = io.BytesIO(response.content)
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return image
