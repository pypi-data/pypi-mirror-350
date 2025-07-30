"""Document metadata functionality."""

import json
import requests
from typing import Dict, Any
from urllib.parse import urljoin

from pythia_client.utils.base import BaseService
from pythia_client.utils.http import create_basic_headers


class MetadataService(BaseService):
    """Service for document metadata operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the metadata service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.documents_by_s3_key_endpoint = urljoin(str(self.url), "documents/s3-key")

    def get_document_metadata(self, s3_key: str) -> Dict[str, Any]:
        """Get a single document metadata based on its S3 key.

        Args:
            s3_key: the S3 key of the file

        Returns:
            The response from the API as a dictionary. Raise an exception with API status code and error message if the status code is not 200.
        Usage:
        ```python
        metadata_dict = client.get_document_metadata(s3_key="abc_sample.pdf")
        ```
        """
        with requests.Session() as session:
            url = self.documents_by_s3_key_endpoint + "/" + s3_key + "/metadata"
            headers = create_basic_headers(self.api_key)
            with session.get(url, headers=headers) as response:
                if response.status_code == 200:
                    api_response = response.json()
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response

    def update_document_metadata(
        self, s3_key: str, metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a single document metadata based on its S3 key. Metadata that can't be changed such as S3 key are ignored. Metadata values that are set to null (None) are deleted.

        Args:
            s3_key: the S3 key of the file
            metadata: new metadata to replace/update/delete.

        Returns:
            The response from the API as a dictionary. Raise an exception with API status code and error message if the status code is not 200.
        Usage:
        ```python
        new_metadata = client.update_document_metadata(s3_key="abc_sample.pdf", metadata={"keywords": ["ALE 400","OXO Connect"], "language": None})
        ```
        """
        with requests.Session() as session:
            url = self.documents_by_s3_key_endpoint + "/" + s3_key + "/metadata"
            headers = create_basic_headers(self.api_key)
            headers["Content-Type"] = "application/json"
            new_metadata = {"metadata": metadata}
            with session.post(
                url, headers=headers, data=json.dumps(new_metadata)
            ) as response:
                if response.status_code == 200:
                    api_response = response.json()
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response
