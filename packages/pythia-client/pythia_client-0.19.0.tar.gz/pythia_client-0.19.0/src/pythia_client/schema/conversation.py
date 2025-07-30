"""
Thread-related schema models for the Pythia client.
"""

from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from .feedback import QueryFeedbackResponse


class ThreadListResponse(BaseModel):
    """Model for thread list response."""

    thread_id: str = Field(..., description="Unique identifier for the thread")
    title: str = Field(..., description="Title of the thread")
    group_id: str = Field(..., description="Group ID associated with the thread")
    user_id: str | None = Field(..., description="User ID associated with the thread")
    created_at: datetime = Field(..., description="Thread creation timestamp")
    updated_at: datetime | None = Field(..., description="Thread last update timestamp")


class ThreadResponse(BaseModel):
    """Model for thread response."""

    thread_info: ThreadListResponse = Field(..., description="Thread details")
    queries: List[QueryFeedbackResponse] = Field(
        ..., description="List of queries in the thread"
    )
