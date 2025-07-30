"""
Query and search-related schema models for the Pythia client.
"""

from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field

from .base import ChatMessage, Meta
from .chunks import DocumentQueryResponse


class SearchParams(BaseModel):
    """Model for search parameters."""

    group_id: str | None = Field(default=None, description="")
    top_k: int = Field(default=30, description="Top_K")
    threshold: float = Field(default=0.1, description="threshold")
    system_prompt: str | None = Field(
        default=None,
        description="System Prompt",
        examples=["Answer the query based on the provided documents."],
    )
    filters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Filters",
        examples=[
            {
                "must": [
                    {"key": "meta.pythia_document_category", "match": {"value": "UMC"}}
                ]
            }
        ],
    )
    return_embedding: bool = Field(
        default=False, description="Return embedding of chunks"
    )
    return_content: bool = Field(default=True, description="Return content of chunks")
    group_by: str | None = Field(default=None, description="")
    group_size: int | None = Field(default=None, description="")
    len_chat_history: int = Field(default=3, description="")


class QueryRequest(BaseModel):
    """Model for query request."""

    query: str = Field(..., description="", examples=["How to update my OXE ?"])
    chat_history: List[ChatMessage] | None = Field(
        default=None,
        description="",
        examples=[
            [
                {"content": "Hey how are you ?", "role": "user", "name": ""},
                {
                    "content": "I'm great, how can I help you ?",
                    "role": "assistant",
                    "name": "",
                },
            ]
        ],
    )
    params: SearchParams = Field(default_factory=SearchParams)
    thread_id: str | None = Field(
        default=None, description="Thread ID to associate the query with"
    )
    user_id: str | None = Field(
        default=None,
        description="Optional ID to associate to the thread and query. If None it will be your group ID.",
    )
    raw: bool | None = Field(
        default=False,
        description="If True, the chat will be processed by the raw chat pipeline.",
    )


class Answer(BaseModel):
    """Model for an answer."""

    data: str = Field(..., description="")
    query: str = Field(..., description="")
    documents: List[DocumentQueryResponse] = Field(default_factory=list, description="")
    meta: Meta = Field(..., description="")


class AnswerBuilderModel(BaseModel):
    """Model for answer builder."""

    answers: List[Answer] = Field(..., description="")


class QueryResponse(BaseModel):
    """Model for query response."""

    AnswerBuilder: AnswerBuilderModel = Field(..., description="")
    thread_id: str | None = Field(
        default=None, description="Thread ID to associate the query with"
    )


class RetrieveParams(BaseModel):
    """Model for retrieve parameters."""

    group_id: str | None = Field(default=None, description="")
    top_k: int = Field(default=30, description="Top_K")
    threshold: float = Field(default=0.1, description="threshold")
    filters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Filters",
        examples=[
            {
                "must": [
                    {"key": "meta.pythia_document_category", "match": {"value": "UMC"}}
                ]
            }
        ],
    )
    return_embedding: bool = Field(
        default=False, description="Return embedding of chunks"
    )
    return_content: bool = Field(default=True, description="Return content of chunks")
    group_by: str | None = Field(default=None, description="")
    group_size: int | None = Field(default=None, description="")


class RetrieveRequest(BaseModel):
    """Model for retrieve request."""

    query: str = Field(..., description="", examples=["How to update my OXE ?"])
    params: RetrieveParams = Field(default_factory=RetrieveParams)


class RetrieveResponse(BaseModel):
    """Model for retrieve response."""

    documents: List[DocumentQueryResponse] = Field(default_factory=list, description="")
