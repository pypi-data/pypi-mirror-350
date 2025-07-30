"""Files retrieval functionality."""

import requests
from typing import List
from urllib.parse import urljoin

from pythia_client.schema import (
    GetFileS3Reponse,
    DocInfos,
)
from pythia_client.utils.base import BaseService
from pythia_client.utils.http import (
    create_basic_headers,
)


class FilesRetrievalService(BaseService):
    """Service for file retrieval operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the file retrieval service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.files_endpoint = urljoin(str(self.url), "files")
        self.file_infos_endpoint = urljoin(str(self.url), "files/infos")

    def get_file_infos_by_group_id(
        self, group_id: str, limit: int = 20
    ) -> List[DocInfos]:
        """Get all the file infos from the API for a specific group_id (owner).

        Args:
            group_id: The name of the group_id the client making the request (who indexed the file).
            limit: The number of top most recent indexed documents to return.

        Returns:
            The response from the API. Raise an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        document_list = client.get_file_infos_by_group_id(group_id="api", limit=20)
        for doc in document_list:
            doc.model_dump()
        ```
        """
        with requests.Session() as session:
            params = {"limit": limit}
            headers = create_basic_headers(self.api_key)
            with session.get(
                self.file_infos_endpoint + "/" + group_id,
                params=params,
                headers=headers,
            ) as response:
                if response.status_code == 200:
                    api_response = [DocInfos(**resp) for resp in response.json()]
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response

    def get_file_infos_by_s3_key(self, group_id: str, s3_key: str) -> DocInfos:
        """Get the file infos from the API for a single file and a specific owner.

        Args:
            group_id: The name of the group_id the client making the request (who indexed the file).
            s3_key: The S3 Key of the file.

        Returns:
            The response from the API. Raise an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        document = client.get_file_infos_by_s3_key(group_id="api", s3_key="abc_sample.pdf")
        document.model_dump()
        ```
        """
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            with session.get(
                self.file_infos_endpoint + "/" + group_id + "/" + s3_key,
                headers=headers,
            ) as response:
                if response.status_code == 200:
                    api_response = DocInfos(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response

    def get_file_url(self, s3_key: str, page: int | None = 1) -> GetFileS3Reponse:
        """Get a pre-signed URL to a file located on S3.

        Args:
            s3_key: The filename of the file to get.
            page: The page to directly point the URL.

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict. Raise an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        get_doc_response = client.get_file_url("s3fd_sample.pdf", page=2)
        s3_url = get_doc_response.url
        ```
        """
        with requests.Session() as session:
            params = {"page": page}
            url = self.files_endpoint + "/" + s3_key
            headers = create_basic_headers(self.api_key)
            with session.get(
                url,
                params=params,
                headers=headers,
            ) as response:
                if response.status_code == 200:
                    api_response = GetFileS3Reponse(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response
