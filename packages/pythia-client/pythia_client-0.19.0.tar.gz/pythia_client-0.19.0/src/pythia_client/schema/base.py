"""
Base schema models for the Pythia client.
"""

from __future__ import annotations

import enum
from typing import Any, Dict

from pydantic import BaseModel, Field


class ChatRole(str, enum.Enum):
    """Enumeration representing the roles within a chat."""

    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"
    TOOL = "tool"


class ChatMessage(BaseModel):
    """Model representing a chat message."""

    content: str
    role: ChatRole
    name: str | None
    meta: Dict[str, Any]


class Usage(BaseModel):
    """Model representing token usage information."""

    prompt_tokens: int | None = Field(default=None, description="")
    completion_tokens: int | None = Field(default=None, description="")


class Meta(BaseModel):
    """Model representing metadata for responses."""

    id: str = Field(..., description="")
    stop_sequence: str | None = Field(default=None, description="")
    model: str = Field(..., description="")
    usage: Usage = Field(..., description="")
    index: int | None = Field(default=None, description="")
    finish_reason: str | None = Field(default=None, description="")


class StatusEnum(str, enum.Enum):
    """Enumeration representing the status of a task."""

    initialized = "initialized"
    completed = "completed"
    processing = "processing"
    failed = "failed"
