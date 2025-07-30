"""Chunks filter functionality."""

import requests
from typing import Dict, Any, List
from urllib.parse import urljoin

from pythia_client.schema import (
    FilterRequest,
    FilterDocStoreResponse,
    DeleteDocResponse,
)
from pythia_client.utils.base import BaseService
from pythia_client.utils.http import (
    create_headers,
    prepare_json_payload,
)


class FilterChunkService(BaseService):
    """Service for chunk filtering operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the chunk filtering service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.documents_by_filter_endpoint = urljoin(str(self.url), "documents/filters")

    def get_docs_by_filters(
        self,
        filters: Dict[str, Any] | None = None,
        return_content: bool = False,
    ) -> List[FilterDocStoreResponse]:
        """List all chunks in the document store that match the filter provided.

        Args:
            filters: Qdrant native filter dict (https://qdrant.tech/documentation/concepts/filtering/) OR Haystack 2.0 filter dict (https://docs.haystack.deepset.ai/v2.0/docs/metadata-filtering#filters).
            return_content: If True, the content of the chunks will be returned.

        Returns:
            The response from the API. Raise an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        # Haystack Filter Style
        filters = {
            "operator": "AND",
            "conditions": [
                {
                    "field": "meta.source",
                    "operator": "==",
                    "value": "Salesforce"
                }
            ]
        }
        # Qdrant Filter Style
        filters =  {
            "must":[
                {
                    "key":"meta.source",
                    "match":{
                        "value": "Salesforce"
                    }
                }
            ]
        }
        list_response = client.get_docs_by_filters(filters=filters)
        list_response.model_dump()
        ```
        """
        if filters is None:
            filters = {}
        request = FilterRequest(filters=filters)
        with requests.Session() as session:
            payload = prepare_json_payload(request)
            headers = create_headers(self.api_key)
            if return_content:
                endpoint = f"{self.documents_by_filter_endpoint}?return_content=true"
            else:
                endpoint = self.documents_by_filter_endpoint

            with session.post(endpoint, headers=headers, json=payload) as response:
                if response.status_code == 200:
                    responses = response.json()
                    api_response = [
                        FilterDocStoreResponse(**resp) for resp in responses
                    ]
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response

    def delete_docs_by_filters(
        self,
        filters: Dict[str, Any] | None = None,
    ) -> DeleteDocResponse:
        """Remove chunks from the API document store.

        Args:
            filters: Qdrant native filter dict (https://qdrant.tech/documentation/concepts/filtering/) OR Haystack 2.0 filter dict (https://docs.haystack.deepset.ai/v2.0/docs/metadata-filtering#filters).

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict. Raise an exception with API status code and error message if the status code is not 200.
        Usage:
        ```python
        # Haystack Filter Style
        filters = {
            "operator": "AND",
            "conditions": [
                {
                    "field": "meta.source",
                    "operator": "==",
                    "value": "Salesforce"
                }
            ]
        }
        # Qdrant Filter Style
        filters =  {
            "must":[
                {
                    "key":"meta.source",
                    "match":{
                        "value": "Salesforce"
                    }
                }
            ]
        }
        remove_response = client.delete_docs_by_filters(filters=filters)
        remove_response.model_dump()
        ```
        """
        if filters is None:
            filters = {}
        request = FilterRequest(filters=filters)
        with requests.Session() as session:
            payload = prepare_json_payload(request)
            headers = create_headers(self.api_key)
            with session.delete(
                self.documents_by_filter_endpoint, headers=headers, json=payload
            ) as response:
                if response.status_code == 200:
                    api_response = DeleteDocResponse(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response
