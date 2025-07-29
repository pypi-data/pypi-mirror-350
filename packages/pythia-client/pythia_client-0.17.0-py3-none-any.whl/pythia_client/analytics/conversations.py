"""Thread functionality."""

import requests
from typing import List, Optional
from urllib.parse import urljoin

from pythia_client.schema import ThreadResponse, ThreadListResponse
from pythia_client.utils.base import BaseService
from pythia_client.utils.http import create_basic_headers


class ThreadService(BaseService):
    """Service for thread operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the thread service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.feedback_endpoint = urljoin(str(self.url), "/feedback")

    def get_thread_queries(
        self, thread_id: str, group_id: Optional[str] = None
    ) -> ThreadResponse:
        """Get all queries for a specific thread ordered by creation date (oldest to newest).

        Args:
            thread_id: The ID of the thread to get queries for.
            group_id: Optional, only used if you use admin key, to get queries from a specific group.

        Returns:
            The response from the API as a Pydantic model containing thread info and queries.
            You can use response.model_dump() to get a Dict.
            Raises an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        thread = client.get_thread_queries(thread_id="123e4567-e89b-12d3-a456-426614174000")
        thread_info = thread.thread_info
        queries = thread.queries
        ```
        """
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            request_url = self.feedback_endpoint + f"/thread/{thread_id}"
            if group_id:
                request_url += f"?group_id={group_id}"
            with session.get(request_url, headers=headers) as response:
                if response.status_code == 200:
                    api_response = ThreadResponse(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response

    def list_threads(
        self,
        group_id: str,
        user_id: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[ThreadListResponse]:
        """List all threads for a group with pagination.

        Args:
            group_id: The group ID to list threads for.
            user_id: Optional user ID to filter threads by. If not provided, defaults to group_id.
            limit: Maximum number of threads to return (1-100, default 50).
            offset: Number of threads to skip for pagination (default 0).

        Returns:
            List of ThreadListResponse Pydantic models. You can use [thread.model_dump() for thread in response]
            to get a list of dicts. Raises an exception with API status code and error message if the status
            code is not 200.

        Usage:
        ```python
        # List all threads for a group
        threads = client.list_threads(group_id="my-group")

        # List threads with pagination
        threads = client.list_threads(
            group_id="my-group",
            user_id="specific-user",
            limit=20,
            offset=40  # Get threads 41-60
        )
        ```
        """
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            params = {
                "limit": limit,
                "offset": offset,
            }
            if user_id:
                params["user_id"] = user_id

            with session.get(
                self.feedback_endpoint + f"/threads/{group_id}",
                headers=headers,
                params=params,
            ) as response:
                if response.status_code == 200:
                    api_response = [
                        ThreadListResponse(**thread) for thread in response.json()
                    ]
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response
