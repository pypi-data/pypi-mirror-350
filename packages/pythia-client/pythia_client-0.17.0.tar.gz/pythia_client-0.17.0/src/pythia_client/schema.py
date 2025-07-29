"""
Schema models for the Pythia client.

This module re-exports all models from the schema package for backward compatibility.
"""

# Re-export all models from the schema package
from pythia_client.schema import (
    # Base models
    ChatRole,
    ChatMessage,
    Usage,
    Meta,
    StatusEnum,
    # Document models
    FilterRequest,
    FilterDocStoreResponse,
    DocumentQueryResponse,
    DeleteDocResponse,
    GetFileS3Reponse,
    DocInfos,
    # Query models
    SearchParams,
    QueryRequest,
    Answer,
    AnswerBuilderModel,
    QueryResponse,
    RetrieveParams,
    RetrieveRequest,
    RetrieveResponse,
    # Indexing models
    IndexingResponse,
    IndexingTask,
    # Auth models
    Permissions,
    ApiKeys,
    # Feedback models
    QueryFeedbackResponse,
    QueryMetricsResponse,
    # Structured Data models
    DataExtractTask,
    DataExtractResponse,
    # Thread models
    ThreadListResponse,
    ThreadResponse,
)

# Define __all__ to control what gets imported with "from pythia_client.schema import *"
__all__ = [
    # Base models
    "ChatRole",
    "ChatMessage",
    "Usage",
    "Meta",
    "StatusEnum",
    # Document models
    "FilterRequest",
    "FilterDocStoreResponse",
    "DocumentQueryResponse",
    "DeleteDocResponse",
    "GetFileS3Reponse",
    "DocInfos",
    # Query models
    "SearchParams",
    "QueryRequest",
    "Answer",
    "AnswerBuilderModel",
    "QueryResponse",
    "RetrieveParams",
    "RetrieveRequest",
    "RetrieveResponse",
    # Indexing models
    "IndexingResponse",
    "IndexingTask",
    # Auth models
    "Permissions",
    "ApiKeys",
    # Feedback models
    "QueryFeedbackResponse",
    "QueryMetricsResponse",
    # Structured Data models
    "DataExtractTask",
    "DataExtractResponse",
    # Thread models
    "ThreadListResponse",
    "ThreadResponse",
]
