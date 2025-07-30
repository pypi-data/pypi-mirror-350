"""
Document-related schema models for the Pythia client.
"""

from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field

from pythia_client.schema import StatusEnum


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


class FilterRequest(BaseModel):
    """Model for document filtering requests."""

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


class FilterDocStoreResponse(BaseModel):
    """Model for document filter response."""

    id: str | None = Field(default=None, description="")
    content: str | None = Field(default=None, description="")
    dataframe: str | Any | None = Field(default=None, description="")
    blob: str | Any | None = Field(default=None, description="")
    meta: Dict[str, Any] = Field(default_factory=dict, description="")
    score: float | None = Field(default=None, description="")
    embedding: List[float] | None = Field(default=None, description="")


class DocumentQueryResponse(BaseModel):
    """Model for document query response."""

    id: str = Field(..., description="")
    content: str = Field(..., description="")
    dataframe: str | Any | None = Field(default=None, description="")
    blob: str | Any | None = Field(default=None, description="")
    meta: Dict[str, Any] = Field(..., description="")
    score: float | None = Field(default=None, description="")
    embedding: List[float] | None = Field(default=None, description="")


class DeleteDocResponse(BaseModel):
    """Model for document deletion response."""

    n_deleted_documents: int = Field(..., description="")
    n_deleted_s3: int = Field(..., description="")
    deleted_s3_keys: List[str] = Field(..., description="")


class GetFileS3Reponse(BaseModel):
    """Model for S3 file retrieval response."""

    url: str = Field(..., description="")


class DocInfos(BaseModel):
    """Model for document information."""

    filename: str = Field(..., description="")
    group_id: str = Field(..., description="")
    embedding_model: str = Field(..., description="")
    is_deleted: bool = Field(..., description="")
    s3_key: str = Field(..., description="")
    file_meta: dict = Field(..., description="")
    total_tokens: int = Field(..., description="")
    task_id: int = Field(..., description="")


class ReplaceMetadataRequest(BaseModel):
    """Model for metadata replacement request."""

    metadata: Dict[str, Any] = Field(
        default={},
        description="Metadata dictionary to update current metadata.",
        examples=[{"keywords": ["ALE 400", "OXO Connect"]}],
    )
