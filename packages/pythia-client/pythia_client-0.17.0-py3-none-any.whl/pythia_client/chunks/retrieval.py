"""Chunks retrieval functionality."""

import requests
from typing import List
from urllib.parse import urljoin

from pythia_client.schema import (
    FilterDocStoreResponse,
    DeleteDocResponse,
)
from pythia_client.utils.base import BaseService
from pythia_client.utils.http import (
    create_basic_headers,
)


class ChunksRetrievalService(BaseService):
    """Service for chunk retrieval operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the chunk retrieval service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.documents_by_s3_key_endpoint = urljoin(str(self.url), "documents/s3-key")

    def get_docs_by_s3_key(self, s3_key: str) -> List[FilterDocStoreResponse]:
        """Get chunks (chunk of files in the Vector DB) from the API document store based on its S3 key.

        Args:
            s3_key: the S3 key of the file

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict. Raise an exception with API status code and error message if the status code is not 200.
        Usage:
        ```python
        chunks_list = client.get_docs_by_s3_key(s3_key="abc_sample.pdf")
        for chunk in chunks_list:
            chunk.model_dump()
        ```
        """
        with requests.Session() as session:
            url = self.documents_by_s3_key_endpoint + "/" + s3_key
            headers = create_basic_headers(self.api_key)
            with session.get(url, headers=headers) as response:
                if response.status_code == 200:
                    api_response = [
                        FilterDocStoreResponse(**resp) for resp in response.json()
                    ]
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response

    def delete_docs_by_s3_key(self, s3_key: str) -> DeleteDocResponse:
        """Delete chunks (chunk of files in the Vector DB) from the API document store based on its S3 key.

        Args:
            s3_key: the S3 key of the file

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict. Raise an exception with API status code and error message if the status code is not 200.
        Usage:
        ```python
        delete_response = client.delete_docs_by_s3_key(s3_key="abc_sample.pdf")
        delete_response.model_dump()
        ```
        """
        with requests.Session() as session:
            url = self.documents_by_s3_key_endpoint + "/" + s3_key
            headers = create_basic_headers(self.api_key)
            with session.delete(url, headers=headers) as response:
                if response.status_code == 200:
                    api_response = DeleteDocResponse(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response
