"""
Schema models for the Pythia client.

This module re-exports all models from the schema submodules for backward compatibility.
"""

# Re-export all models from the schema submodules
from .base import (
    ChatRole,
    ChatMessage,
    Usage,
    Meta,
    StatusEnum,
)

from .chunks import (
    FilterRequest,
    FilterDocStoreResponse,
    DocumentQueryResponse,
    DeleteDocResponse,
    GetFileS3Reponse,
    DocInfos,
)

from .query import (
    SearchParams,
    QueryRequest,
    Answer,
    AnswerBuilderModel,
    QueryResponse,
    RetrieveParams,
    RetrieveRequest,
    RetrieveResponse,
)

from .indexing import (
    IndexingResponse,
    IndexingTask,
)

from .auth import (
    Permissions,
    ApiKeys,
)


from .feedback import (
    QueryFeedbackResponse,
    QueryMetricsResponse,
)

from .structured_data import (
    DataExtractTask,
    DataExtractResponse,
)

from .conversation import (
    ThreadListResponse,
    ThreadResponse,
)

# Complete list of all exported models
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
