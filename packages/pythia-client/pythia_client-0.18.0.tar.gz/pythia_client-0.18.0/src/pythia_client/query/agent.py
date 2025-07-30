"""Agent functionality."""

import requests
from typing import Generator
from urllib.parse import urljoin

from pythia_client.utils.base import BaseService
from pythia_client.utils.http import create_headers
from pythia_client.utils.streaming import stream_response


class AgentService(BaseService):
    """Service for Agent operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the Agent service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.agent_endpoint = urljoin(str(self.url), "/agent/stream")

    def agent_stream(
        self,
        query: str,
    ) -> Generator:
        """Query the API with a user question to get a LLM-generated answer based
        on context from the document store. This method works with the "agent" endpoint and stream the output.
        WARNING: This method is in Alpha, not ready for production and will be subject to breaking changes.

        Args:
            query: The user question to be answered.

        Returns:
            A generator containing the streamed response from the API. The generator yields chunks of data as they are received.
        """
        # Create a session that will be kept alive for the duration of the generator
        session = requests.Session()
        payload = {"text": query}
        headers = create_headers(self.api_key)
        response = session.post(
            self.agent_endpoint, headers=headers, json=payload, stream=True
        )

        if response.status_code != 200:
            response.close()
            session.close()
            raise Exception(
                f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
            )

        # Create a generator that will clean up resources when done
        def generate():
            try:
                yield from stream_response(response)
            finally:
                response.close()
                session.close()

        return generate()
