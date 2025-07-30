"""
Indexing-related schema models for the Pythia client.
"""

from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field

from .base import StatusEnum


class IndexingResponse(BaseModel):
    """Model for indexing response."""

    message: str = Field(..., description="")
    s3_keys: List[str] = Field(..., description="")
    group_id: str = Field(..., description="")


class IndexingTask(BaseModel):
    """Model for indexing task."""

    group_id: str = Field(..., description="")
    job_queue_uuid: str | None = Field(default=None, description="")
    description: str | None = Field(default=None, description="")
    type: str = Field(..., description="")
    id: int = Field(..., description="")
    name: str | None = Field(default=None, description="")
    status: StatusEnum = Field(..., description="")
    s3_key: str = Field(..., description="")
    task_parameters: Dict | None = Field(default=None, description="")
    result_json: Dict | None = Field(default=None, description="")
    detailed_token_consumption: List[Dict] | None = Field(..., description="")
    time_taken: float | None = Field(default=None, description="")
