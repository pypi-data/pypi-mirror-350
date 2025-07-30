"""
Authentication-related schema models for the Pythia client.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Permissions = Literal["full", "read_only"]


class ApiKeys(BaseModel):
    """Model for API keys."""

    name: str | None = Field(default=None, description="")
    creator_id: str = Field(..., description="")
    group_id: str = Field(..., description="")
    api_key: str = Field(..., description="")
    permission: Permissions = Field(..., description="")
    revoked: bool = Field(..., description="")
    revoked_at: datetime | None = Field(..., description="")
