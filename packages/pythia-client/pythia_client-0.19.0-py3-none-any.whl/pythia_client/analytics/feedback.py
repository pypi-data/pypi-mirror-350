"""Query feedback functionality."""

import requests
from typing import List, Optional, Union
from datetime import datetime
from urllib.parse import urljoin

from pythia_client.schema import QueryFeedbackResponse
from pythia_client.utils.base import BaseService
from pythia_client.utils.http import create_basic_headers


class QueryFeedbackService(BaseService):
    """Service for query feedback operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the query feedback service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.feedback_endpoint = urljoin(str(self.url), "/feedback")

    def list_query_history_by_group_id(
        self,
        group_id: str,
        limit: int = 50,
        offset: int = 0,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_feedback: Optional[int] = None,
        max_feedback: Optional[int] = None,
        has_comments: bool | None = None,
        category: Optional[str] = None,
    ) -> List[QueryFeedbackResponse]:
        """List the query history for a specific group_id with advanced filtering options.

        Args:
            group_id: Group ID (user ID) to list the query history from
            limit: The number of top most recent queries to return.
            offset: Number of queries to skip (for pagination purpose).
            start_date: Optional datetime to filter queries from this date (inclusive)
            end_date: Optional datetime to filter queries until this date (inclusive)
            min_feedback: Filter queries with feedback greater than or equal to this value
            max_feedback: Filter queries with feedback less than or equal to this value
            has_comments: Filter queries that have comments
            category: Filter queries by Pythia document category

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict.
            Raises an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        # List all queries
        query_history = client.list_query_history_by_group_id(group_id="ec878-bc91398-j8092")

        # List queries with advanced filters
        from datetime import datetime, timedelta
        start = datetime.now() - timedelta(days=7)  # Last 7 days
        end = datetime.now()
        query_history = client.list_query_history_by_group_id(
            group_id="UMC",
            start_date=start,
            end_date=end,
            min_feedback=3,  # Only queries with feedback >= 3
            has_comments=True,  # Only queries with comments
            category="KCS"  # Only KCS documents
        )
        query_history.model_dump()
        ```
        """
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            with session.get(
                self.feedback_endpoint + f"/query-history/{group_id}",
                headers=headers,
                params={
                    "limit": limit,
                    "offset": offset,
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None,
                    "min_feedback": min_feedback,
                    "max_feedback": max_feedback,
                    "has_comments": has_comments,
                    "category": category,
                },
            ) as response:
                if response.status_code == 200:
                    api_response = [
                        QueryFeedbackResponse(**resp) for resp in response.json()
                    ]
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response

    def add_feedback_to_query(
        self,
        query_uuid: int | str,
        feedback: int,
        feedback_comment: Union[str, None] = None,
    ) -> QueryFeedbackResponse:
        """Add feedback to a specific query

        Args:
            query_uuid: UUID of the query to add feedback to. Can also be query_id (legacy)
            feedback: Feedback to add to query. From O (negative feedback) to 5 (positive feedback). Default to -1 (no feedback)
            feedback_comment: Optional text feedback (user comment)

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict. Raise an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        feedback_response = client.add_feedback_to_query(query_id=1337, feedback=0)
        feedback_response.model_dump()
        ```
        """
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            with session.get(
                self.feedback_endpoint + f"/add/{query_uuid}",
                headers=headers,
                params={"feedback": feedback, "feedback_comment": feedback_comment},
            ) as response:
                if response.status_code == 200:
                    api_response = QueryFeedbackResponse(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response
