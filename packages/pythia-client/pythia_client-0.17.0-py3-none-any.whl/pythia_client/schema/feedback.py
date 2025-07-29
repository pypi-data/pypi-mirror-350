"""
Feedback-related schema models for the Pythia client.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, Field


class QueryFeedbackResponse(BaseModel):
    """Model for query feedback response."""

    id: int = Field(..., description="")
    query_uuid: str | None = Field(..., description="")
    thread_id: str | None = Field(..., description="")
    group_id: str = Field(..., description="")
    user_id: str | None = Field(..., description="")
    system_prompt: str = Field(..., description="")
    user_query: str = Field(..., description="")
    answer: str = Field(..., description="")
    embedding_model: str = Field(..., description="")
    chat_model: str = Field(..., description="")
    retrieved_s3_keys: List[str] = Field(..., description="")
    retrieved_chunks: List[Dict] = Field(..., description="")
    prompt_tokens: int = Field(..., description="")
    completion_tokens: int = Field(..., description="")
    total_tokens: int = Field(..., description="")
    time_taken: float = Field(..., description="")
    feedback: int = Field(..., description="")
    feedback_comment: str | None = Field(..., description="")
    detailed_token_consumption: List[Dict] | None = Field(..., description="")
    created_at: datetime = Field(..., description="")
    pythia_document_categories: List[str] | None = Field(..., description="")
    pipeline_type: str | None = Field(..., description="")


class QueryMetricsResponse(BaseModel):
    """Model for query metrics response."""

    total_queries: int | None = Field(default=..., description="")
    feedback_distribution: Dict[str, int] = Field(
        default=..., description=""
    )  # Maps feedback value to count
    avg_time: float | None = Field(default=..., description="")
    total_tokens: int | None = Field(default=..., description="")
    estimated_cost: float | None = Field(default=..., description="")
