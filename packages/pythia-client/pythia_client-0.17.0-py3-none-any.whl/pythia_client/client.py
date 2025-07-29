"""A client for interacting with the API.

This module provides a client class for interacting with the API, including
indexing documents, listing them, deleting them, get S3 URL to a document,
querying them and extracting structured json data from text.

Classes:
    APIClient: Client for interacting with the API.
"""

from urllib.parse import urljoin

from pythia_client.auth.api_keys import ApiKeyService
from pythia_client.files.indexing import IndexingService
from pythia_client.files.files_info import FilesRetrievalService
from pythia_client.chunks.retrieval import ChunksRetrievalService
from pythia_client.chunks.metadata import MetadataService
from pythia_client.chunks.facets import FacetsService
from pythia_client.chunks.filter import FilterChunkService
from pythia_client.query.rag import QueryService
from pythia_client.query.chat import ChatService
from pythia_client.query.retrieve import RetrieveService
from pythia_client.query.agent import AgentService
from pythia_client.structured_data.structured_data import StructuredDataService
from pythia_client.pipelines.pipelines import PipelineService
from pythia_client.analytics.feedback import QueryFeedbackService
from pythia_client.analytics.conversations import ThreadService
from pythia_client.analytics.metrics import MetricsService


class APIClient:
    """Client for interacting with the API.

    This class provides methods for interacting with the API, including
    indexing documents, listing them, deleting them, get S3 URL to a document,
    querying them and extracting structured json data from text.

    Attributes:
        url: The base URL for the API.
        api-key: The api key for the API.
    """

    def __init__(self, url: str, api_key: str):
        """Initializes the API client with the given URL and the API key.

        Args:
            url: The base URL for the API.
            api_key: The api key for the API.

        Usage:
        ```python
        from pythia_client.client import APIClient
        client = APIClient("http://localhost:8000", "api-key")
        ```
        """
        self.url = url
        self.api_key = api_key

        # Initialize services
        self._api_key_service = ApiKeyService(url, api_key)
        self._indexing_service = IndexingService(url, api_key)
        self._files_retrieval_service = FilesRetrievalService(url, api_key)
        self._document_retrieval_service = ChunksRetrievalService(url, api_key)
        self._metadata_service = MetadataService(url, api_key)
        self._facets_service = FacetsService(url, api_key)
        self._filters_service = FilterChunkService(url, api_key)
        self._query_service = QueryService(url, api_key)
        self._chat_service = ChatService(url, api_key)
        self._agent_service = AgentService(url, api_key)
        self._retrieve_service = RetrieveService(url, api_key)
        self._structured_data_service = StructuredDataService(url, api_key)
        self._query_feedback_service = QueryFeedbackService(url, api_key)
        self._thread_service = ThreadService(url, api_key)
        self._metrics_service = MetricsService(url, api_key)
        self._pipeline_service = PipelineService(url, api_key)

        # Initialize endpoints for backward compatibility
        self.files_endpoint = urljoin(str(self.url), "files")
        self.facets_endpoint = urljoin(str(self.url), "/documents/facets")
        self.indexing_tasks_endpoint = urljoin(str(self.url), "files/indexing-tasks")
        self.file_infos_endpoint = urljoin(str(self.url), "files/infos")
        self.documents_by_filter_endpoint = urljoin(str(self.url), "chunks/filters")
        self.documents_by_s3_key_endpoint = urljoin(str(self.url), "chunks/s3-key")
        self.chat_endpoint = urljoin(str(self.url), "chat/query")
        self.search_endpoint = urljoin(str(self.url), "search/query")
        self.agent_endpoint = urljoin(str(self.url), "/agent/stream")
        self.retrieve_endpoint = urljoin(str(self.url), "retrieve/query")
        self.data_extraction_endpoint = urljoin(
            str(self.url), "/data-extraction/extract-structured-data"
        )
        self.api_keys_endpoint = urljoin(str(self.url), "/api-keys")
        self.feedback_endpoint = urljoin(str(self.url), "/feedback")
        self.draw_endpoint = urljoin(str(self.url), "/draw")

    # API Key Management Methods
    def create_api_key(self, name, creator_id, group_id, permission):
        """Create an API key for a group_id."""
        return self._api_key_service.create_api_key(
            name, creator_id, group_id, permission
        )

    def revoke_api_key(self, api_key_to_revoke, creator_id):
        """Revoke an API key."""
        return self._api_key_service.revoke_api_key(api_key_to_revoke, creator_id)

    def list_api_keys_by_group_id(self, group_id):
        """List API Keys for a specific group_id."""
        return self._api_key_service.list_api_keys_by_group_id(group_id)

    def list_api_keys_by_creator_id(self, creator_id):
        """List API Keys for a specific creator_id."""
        return self._api_key_service.list_api_keys_by_creator_id(creator_id)

    # Document Indexing Methods
    def upload_files(
        self, files, meta=None, indexing_mode="unstructured", priority_queue=False
    ):
        """Index one or multiples files (documents) to the document store."""
        return self._indexing_service.upload_files(
            files, meta, indexing_mode, priority_queue
        )

    def get_indexing_tasks_by_group_id(self, group_id, top=20):
        """Get the indexing tasks from the API."""
        return self._indexing_service.get_indexing_tasks_by_group_id(group_id, top)

    def get_indexing_task_by_s3_key(self, group_id, s3_key):
        """Get a specific indexing task by its S3 key."""
        return self._indexing_service.get_indexing_task_by_s3_key(group_id, s3_key)

    # Document Retrieval Methods
    def get_file_infos_by_group_id(self, group_id, limit=20):
        """Get all the file infos from the API for a specific group_id (owner)."""
        return self._files_retrieval_service.get_file_infos_by_group_id(group_id, limit)

    def get_file_infos_by_s3_key(self, group_id, s3_key):
        """Get the file infos from the API for a single file and a specific owner."""
        return self._files_retrieval_service.get_file_infos_by_s3_key(group_id, s3_key)

    def get_file_url(self, s3_key, page=1):
        """Get a pre-signed URL to a file located on S3."""
        return self._files_retrieval_service.get_file_url(s3_key, page)

    def get_docs_by_filters(self, filters=None, return_content=False):
        """List all documents in the document store that match the filter provided."""
        return self._filters_service.get_docs_by_filters(filters, return_content)

    def delete_docs_by_filters(self, filters=None):
        """Remove documents from the API document store."""
        return self._filters_service.delete_docs_by_filters(filters)

    def get_docs_by_s3_key(self, s3_key):
        """Get documents (chunk of files in the Vector DB) from the API document store based on its S3 key."""
        return self._document_retrieval_service.get_docs_by_s3_key(s3_key)

    def delete_docs_by_s3_key(self, s3_key):
        """Delete documents (chunk of files in the Vector DB) from the API document store based on its S3 key."""
        return self._document_retrieval_service.delete_docs_by_s3_key(s3_key)

    def get_facets_count(self, filters=None):
        """Get the number of unique file/document for a specific Qdrant filter."""
        return self._facets_service.get_facets_count(filters)

    def get_facets_values(self, metadata_field, filters=None):
        """Get the unique values for a specific metadata field with an optional Qdrant filter."""
        return self._facets_service.get_facets_values(metadata_field, filters)

    # Document Metadata Methods
    def get_document_metadata(self, s3_key):
        """Get a single document metadata based on its S3 key."""
        return self._metadata_service.get_document_metadata(s3_key)

    def update_document_metadata(self, s3_key, metadata):
        """Update a single document metadata based on its S3 key."""
        return self._metadata_service.update_document_metadata(s3_key, metadata)

    # Search Methods
    def query(
        self,
        query,
        chat_history=None,
        filters=None,
        top_k=30,
        group_id=None,
        custom_system_prompt=None,
        threshold=0.1,
        return_embedding=False,
        group_by=None,
        group_size=None,
        return_content=True,
        user_id=None,
        thread_id=None,
        len_chat_history=3,
    ):
        """Query the API with a user question to get a LLM-generated answer based on context from the document store."""
        return self._query_service.query(
            query,
            chat_history,
            filters,
            top_k,
            group_id,
            custom_system_prompt,
            threshold,
            return_embedding,
            group_by,
            group_size,
            return_content,
            user_id,
            thread_id,
            len_chat_history,
        )

    def chat(
        self,
        query,
        chat_history=None,
        filters=None,
        top_k=30,
        group_id=None,
        custom_system_prompt=None,
        threshold=0.1,
        return_embedding=False,
        group_by=None,
        group_size=None,
        return_content=True,
        user_id=None,
        thread_id=None,
        len_chat_history=3,
        raw_mode=False,
    ):
        """Query the Chat API endpoint with a user question to get a LLM-generated answer."""
        return self._chat_service.chat(
            query,
            chat_history,
            filters,
            top_k,
            group_id,
            custom_system_prompt,
            threshold,
            return_embedding,
            group_by,
            group_size,
            return_content,
            user_id,
            thread_id,
            len_chat_history,
            raw_mode,
        )

    def agent_stream(self, query):
        """Query the API with a user question to get a LLM-generated answer based on context from the document store."""
        return self._agent_service.agent_stream(query)

    def retrieve(
        self,
        query,
        filters=None,
        top_k=30,
        group_id=None,
        threshold=0.1,
        return_embedding=False,
        group_by=None,
        group_size=None,
        return_content=True,
    ):
        """Query the API with a user question to get a list of relevant chunk of documents from the document store."""
        return self._retrieve_service.retrieve(
            query,
            filters,
            top_k,
            group_id,
            threshold,
            return_embedding,
            group_by,
            group_size,
            return_content,
        )

    # Data Extraction Methods
    def extract_structured_data(
        self,
        file=None,
        string_content=None,
        additional_instructions=None,
        json_schema=None,
        preset=None,
        extraction_mode="fast",
    ):
        """Extract structured data according to a JSON schema."""
        return self._structured_data_service.extract_structured_data(
            file,
            string_content,
            additional_instructions,
            json_schema,
            preset,
            extraction_mode,
        )

    def get_extract_structured_data_job(self, job_uuid):
        """Get the status and result of a data extract task based on its job UUID."""
        return self._structured_data_service.get_extract_structured_data_job(job_uuid)

    # Query Feedback Methods
    def list_query_history_by_group_id(
        self,
        group_id,
        limit=50,
        offset=0,
        start_date=None,
        end_date=None,
        min_feedback=None,
        max_feedback=None,
        has_comments=None,
        category=None,
    ):
        """List the query history for a specific group_id with advanced filtering options."""
        return self._query_feedback_service.list_query_history_by_group_id(
            group_id,
            limit,
            offset,
            start_date,
            end_date,
            min_feedback,
            max_feedback,
            has_comments,
            category,
        )

    def get_query_metrics_by_group_id(
        self,
        group_id,
        start_date=None,
        end_date=None,
        min_feedback=None,
        max_feedback=None,
        has_comments=False,
        category=None,
    ):
        """Get aggregated metrics for queries with filtering options."""
        return self._metrics_service.get_query_metrics_by_group_id(
            group_id,
            start_date,
            end_date,
            min_feedback,
            max_feedback,
            has_comments,
            category,
        )

    def add_feedback_to_query(self, query_uuid, feedback, feedback_comment=None):
        """Add feedback to a specific query."""
        return self._query_feedback_service.add_feedback_to_query(
            query_uuid, feedback, feedback_comment
        )

    # Thread Methods
    def get_thread_queries(self, thread_id, group_id=None):
        """Get all queries for a specific thread ordered by creation date."""
        return self._thread_service.get_thread_queries(thread_id, group_id)

    def list_threads(self, group_id, user_id=None, limit=50, offset=0):
        """List all threads for a group with pagination."""
        return self._thread_service.list_threads(group_id, user_id, limit, offset)

    def draw_pipeline(self, pipeline_name):
        """Draw the pipeline image."""
        return self._pipeline_service.draw_pipeline(pipeline_name)
