"""Chat functionality."""

import requests
from typing import Dict, Any, List, Union
from urllib.parse import urljoin

from pythia_client.schema import QueryRequest, QueryResponse, ChatMessage, SearchParams
from pythia_client.utils.base import BaseService
from pythia_client.utils.http import create_headers, prepare_json_payload


class ChatService(BaseService):
    """Service for chat operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the chat service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.chat_endpoint = urljoin(str(self.url), "chat/query")

    def chat(
        self,
        query: str,
        chat_history: List[ChatMessage] | None = None,
        filters: Dict[str, Any] | None = None,
        top_k=30,
        group_id: Union[str, None] = None,
        custom_system_prompt: Union[str, None] = None,
        threshold: float = 0.1,
        return_embedding: bool = False,
        group_by: Union[str, None] = None,
        group_size: Union[int, None] = None,
        return_content: bool = True,
        user_id: Union[str, None] = None,
        thread_id: Union[str, None] = None,
        len_chat_history: int = 3,
        raw_mode: bool = False,
    ) -> QueryResponse:
        """Query the Chat API endpoint with a user question to get a LLM-generated answer based
            on context from the document store. The difference with the query method is that the chat method can do "quick-answer" based on user history and doesn't always perform RAG search.

            Args:
                query: The user question to be answered.
                chat_history: The chat history to provide context to the model. Should be a list of ChatMessage objects.
                filters: Qdrant native filter dict (https://qdrant.tech/documentation/concepts/filtering/) OR Haystack 2.0 filter dict (https://docs.haystack.deepset.ai/v2.0/docs/metadata-filtering#filters).
                top_k: The number of document to fetch to answer the query.
                group_id: The name of the group_id the client making the request, for logging. Defaults to "api".
                custom_system_prompt: A custom system prompt to use for the LLM.
                threshold: The threshold to use for the LLM.
                return_embedding: If True, the response will include the embeddings of the documents that were used to generate the answer.
                return_content: If True, the response will include the content of the documents that were used to generate the answer.
                user_id: Optional parameter to tag the query in database with a user id on top of group_id. Useful for threads feature.
                thread_id: Optional thread ID to use for the query. If not provided, a new thread will be created.
                len_chat_history: The number of messages to keep in the chat history for the query (retrieved automatically based on thread ID. Default is 3.
                raw_mode: If True, the RAG mechanism is deactivated producing raw LLM response.

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
            query_response = client.chat("Hey how are you", filters=filters)
            query_response.model_dump()
            ```
            Can also be used with chat history:
            ```python
            chat_history = [
                {
                    "content": "Hello Chatbot. My name is Corentin !",
                    "role": "user",
                    "name": None,
                    "meta": {},
                }
            ]
            response = client.query(
                query="Given our previous exchange of messages, what is my name ?",
                chat_history=chat_history,
            )
        ```
        """
        if filters is None:
            filters = {}
        params = SearchParams(
            top_k=top_k,
            group_id=group_id,
            filters=filters,
            system_prompt=custom_system_prompt,
            return_embedding=return_embedding,
            return_content=return_content,
            threshold=threshold,
            group_by=group_by,
            group_size=group_size,
            len_chat_history=len_chat_history,
        ).model_dump()
        request = QueryRequest(
            query=query,
            chat_history=chat_history,
            params=params,
            user_id=user_id,
            thread_id=thread_id,
            raw=raw_mode,
        )
        with requests.Session() as session:
            payload = prepare_json_payload(request)
            headers = create_headers(self.api_key)
            with session.post(
                self.chat_endpoint, headers=headers, json=payload
            ) as response:
                if response.status_code == 200:
                    api_response = QueryResponse(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response
