"""Retrieve functionality."""

import requests
from typing import Dict, Any, Union
from urllib.parse import urljoin

from pythia_client.schema import RetrieveRequest, RetrieveResponse, RetrieveParams
from pythia_client.utils.base import BaseService
from pythia_client.utils.http import create_headers, prepare_json_payload


class RetrieveService(BaseService):
    """Service for retrieve operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the retrieve service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.retrieve_endpoint = urljoin(str(self.url), "retrieve/query")

    def retrieve(
        self,
        query: str,
        filters: Dict[str, Any] | None = None,
        top_k=30,
        group_id: Union[str, None] = None,
        threshold: float = 0.1,
        return_embedding: bool = False,
        group_by: Union[str, None] = None,
        group_size: Union[int, None] = None,
        return_content: bool = True,
    ) -> RetrieveResponse:
        """Query the API with a user question to get a list of relevant chunk of documents from the document store.

            Args:
                query: The user question to be answered.
                filters: Qdrant native filter dict (https://qdrant.tech/documentation/concepts/filtering/) OR Haystack 2.0 filter dict (https://docs.haystack.deepset.ai/v2.0/docs/metadata-filtering#filters).
                top_k: The number of document to fetch to answer the query.
                group_id: The name of the group_id the client making the request, for logging. Defaults to "api".
                threshold: The threshold to use for the LLM.
                return_embedding: If True, the response will include the embeddings of the documents that were used to generate the answer.
                return_content: If True, the response will include the content of the documents that were used to generate the answer.

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
            retrieve_response = client.retrieve("Reboot my OXE", filters=filters)
            retrieve_response.model_dump()
        ```
        """
        if filters is None:
            filters = {}
        params = RetrieveParams(
            top_k=top_k,
            group_id=group_id,
            filters=filters,
            return_embedding=return_embedding,
            return_content=return_content,
            threshold=threshold,
            group_by=group_by,
            group_size=group_size,
        ).model_dump()
        request = RetrieveRequest(
            query=query,
            params=params,
        )
        with requests.Session() as session:
            payload = prepare_json_payload(request)
            headers = create_headers(self.api_key)
            with session.post(
                self.retrieve_endpoint, headers=headers, json=payload
            ) as response:
                if response.status_code == 200:
                    api_response = RetrieveResponse(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response
