"""Chunks facets functionality."""

import requests
from typing import Dict, Any, List
from urllib.parse import urljoin

from pythia_client.schema import (
    FilterRequest,
)
from pythia_client.utils.base import BaseService
from pythia_client.utils.http import (
    create_basic_headers,
    prepare_json_payload,
)


class FacetsService(BaseService):
    """Service for chunk facets operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the chunk facets service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.facets_endpoint = urljoin(str(self.url), "/documents/facets")

    def get_facets_count(
        self,
        filters: Dict[str, Any] | None = None,
    ) -> int:
        """This method allows you to retrieve the number of unique file for a specific [Qdrant filter](https://qdrant.tech/documentation/concepts/filtering/).
        You can only use Qdrant filters for this endpoint, and we recommend to only filter on field that have an index in Qdrant.

        Args:
            filters: Optional Qdrant filters to restrict the chunk facets counting.

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict. Raise an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        filters =  {
            "must":[
                {
                    "key":"meta.pythia_document_category",
                    "match":{
                        "value": "KCS"
                    }
                }
            ]
        }
        client.get_facets_count(filters=filters)
        > 123
        ```
        """
        if filters is None:
            filters = {}
        request = FilterRequest(filters=filters)
        payload = prepare_json_payload(request)
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            with session.post(
                self.facets_endpoint + "/count",
                headers=headers,
                json=payload,
            ) as response:
                if response.status_code == 200:
                    count = int(response.text)
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return count

    def get_facets_values(
        self,
        metadata_field: str,
        filters: Dict[str, Any] | None = None,
    ) -> List[str]:
        """This method allows you to retrieve the unique values for a specific metadata field with an optional [Qdrant filter](https://qdrant.tech/documentation/concepts/filtering/).
        You can only use Qdrant filters for this method, and we recommend to only filter on field that have an index in Qdrant.
        For the metadata_field value, an error will be raised if the field corresponding to the metadata_field does not have an index in Qdrant.
        Example of metadata_field: `meta.keywords`

        Args:
            metadata_field: The metadata field to get the unique values form. Will raise an error if the field does not have an index in Qdrant.
            filters: Optional Qdrant filters to restrict the chunk facets counting.

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict. Raise an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        filters =  {
            "must":[
                {
                    "key":"meta.pythia_document_category",
                    "match":{
                        "value": "KCS"
                    }
                }
            ]
        }
        client.get_facets_values("meta.keywords", filters=filters)
        > ["ALE 400", "OXO Connect"]
        ```
        """
        if filters is None:
            filters = {}
        request = FilterRequest(filters=filters)
        payload = prepare_json_payload(request)
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            with session.post(
                self.facets_endpoint + "/values",
                headers=headers,
                params={"metadata_field": metadata_field},
                json=payload,
            ) as response:
                if response.status_code == 200:
                    response_data = response.json()
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return response_data
