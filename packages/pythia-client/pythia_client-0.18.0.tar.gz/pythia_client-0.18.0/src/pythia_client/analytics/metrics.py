"""Metrics functionality."""

import requests
from typing import Optional
from datetime import datetime
from urllib.parse import urljoin

from pythia_client.schema import QueryMetricsResponse
from pythia_client.utils.base import BaseService
from pythia_client.utils.http import create_basic_headers


class MetricsService(BaseService):
    """Service for metrics operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the metrics service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.feedback_endpoint = urljoin(str(self.url), "/feedback")

    def get_query_metrics_by_group_id(
        self,
        group_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_feedback: Optional[int] = None,
        max_feedback: Optional[int] = None,
        has_comments: Optional[bool] = False,
        category: Optional[str] = None,
    ) -> QueryMetricsResponse:
        """Get aggregated metrics for queries with filtering options.

        Args:
            group_id: Group ID to get metrics for. Use "admin" to get metrics across all groups (requires admin API key)
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
        # Get basic metrics
        metrics = client.get_query_metrics_by_group_id(group_id="ec878-bc91398-j8092")

        # Get metrics with filters
        from datetime import datetime, timedelta
        start = datetime.now() - timedelta(days=7)  # Last 7 days
        end = datetime.now()
        metrics = client.get_query_metrics_by_group_id(
            group_id="UMC",
            start_date=start,
            end_date=end,
            min_feedback=3,  # Only queries with feedback >= 3
            has_comments=True,  # Only queries with comments
            category="KCS"  # Only KCS documents
        )
        metrics.model_dump()
        ```
        """
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            with session.get(
                self.feedback_endpoint + f"/query-metrics/{group_id}",
                headers=headers,
                params={
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None,
                    "min_feedback": min_feedback,
                    "max_feedback": max_feedback,
                    "has_comments": has_comments,
                    "category": category,
                },
            ) as response:
                if response.status_code == 200:
                    api_response = QueryMetricsResponse(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response
