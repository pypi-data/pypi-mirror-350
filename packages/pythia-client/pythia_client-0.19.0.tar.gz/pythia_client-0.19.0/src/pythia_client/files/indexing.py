"""Document indexing functionality."""

import io
import os
import json
import requests
from typing import List, Tuple, Literal
from urllib.parse import urljoin

from pythia_client.schema import IndexingResponse, IndexingTask
from pythia_client.utils.base import BaseService
from pythia_client.utils.http import create_basic_headers


class IndexingService(BaseService):
    """Service for document indexing operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the indexing service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.files_endpoint = urljoin(str(self.url), "files")
        self.indexing_tasks_endpoint = urljoin(str(self.url), "files/indexing-tasks")

    def upload_files(
        self,
        files: List[str | Tuple[str, io.IOBase]],
        meta: List[dict] | None = None,
        indexing_mode: Literal["unstructured", "tika"] = "unstructured",
        priority_queue: bool = False,
    ) -> IndexingResponse:
        """Index one or multiples files (documents) to the document store through the Pythia-API upload-file endpoint.
        It is recommended to add the following minimum metadata fields:
            - pythia_document_category (string, category name tag)
            - document_date (datetime)
            - language (string)
            - keywords (list)
            Example of value for meta field for the indexing of two files:
            ```json
            {
              "meta": [
                {
                    "pythia_document_category":"TDL Document",
                    "document_date":"2024-01-19 14:56",
                    "keywords":["ALE 400", "ALE 500"],
                    "language":"English",
                },
                {
                    "pythia_document_category":"Marketing Document
                    "document_date":"2024-01-19 14:58",
                    "keywords":["OXE 8", "OXE 9"],
                    "language":"Français",
                }
              ]
            }
            ```
        Args:
            files: The paths to the files OR tuples of filename and file object to index.
            meta: The list of metadata for the files.
            indexing_mode: The indexing mode between Unstructured and Apache Tika.
            priority_queue: If the indexing should use the priority queue (more workers). Only working with admin API Key.

        Returns:
            The response from the API. Raise an exception with API status code and error message if the status code is not 202.

        Usage:
        ```python
        index_response = client.upload_files(["path/to/file.pdf"], meta=[{"source": "Salesforce"}])
        {"message": "Files Submitted. Indexing task created."}
        index_response = client.upload_files([("file.pdf", file)], meta=[{"source": "Salesforce"}])
        {"message": "Files Submitted. Indexing task created."}
        ```
        """
        prepared_files = []
        for file in files:
            if isinstance(file, str):
                file_name = os.path.basename(file)
                with open(file, "rb") as f:
                    file_content = f.read()
            elif (
                isinstance(file, tuple)
                and len(file) == 2
                and isinstance(file[1], io.IOBase)
            ):
                file_name, file_object = file
                file_content = file_object.read()
            else:
                raise ValueError(
                    "Each file must be a file path or a tuple of (filename, fileIObyte)"
                )

            prepared_files.append(("files", (file_name, file_content)))

        with requests.Session() as session:
            payload = {
                "meta": json.dumps(meta),
                "priority_queue": priority_queue,
                "indexing_mode": indexing_mode,
            }
            headers = create_basic_headers(self.api_key)
            with session.post(
                self.files_endpoint,
                files=prepared_files,
                data=payload,
                headers=headers,
            ) as response:
                if response.status_code == 202:
                    api_response = response.json()
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return IndexingResponse.model_validate(api_response)

    def get_indexing_tasks_by_group_id(
        self, group_id: str, top: int = 20
    ) -> List[IndexingTask]:
        """Get the indexing tasks from the API.

        Args:
            group_id: The name of the group_id the client making the request, for logging. If none, the default group_id is "api" (set by the API itself).
            top: The number of top most recent indexing tasks to return.

        Returns:
            The response from the API. Raise an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        indexing_tasks = client.get_indexing_tasks(group_id="api", top=20)
        indexing_tasks.model_dump()
        ```
        """
        with requests.Session() as session:
            params = {"top": top}
            headers = create_basic_headers(self.api_key)
            with session.get(
                self.indexing_tasks_endpoint + "/" + group_id,
                params=params,
                headers=headers,
            ) as response:
                if response.status_code == 200:
                    api_response = [IndexingTask(**resp) for resp in response.json()]
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response

    def get_indexing_task_by_s3_key(self, group_id: str, s3_key: str) -> IndexingTask:
        """Get a specific indexing task by its S3 key.

        Args:
            group_id: The name of the group_id the client making the request.
            s3_key: The S3 key of the file.

        Returns:
            The response from the API. Raise an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        indexing_task = client.get_indexing_task_by_s3_key(group_id="api", s3_key="abc_sample.pdf")
        indexing_task.model_dump()
        ```
        """
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            with session.get(
                self.indexing_tasks_endpoint + "/" + group_id + "/" + s3_key,
                headers=headers,
            ) as response:
                if response.status_code == 200:
                    api_response = IndexingTask(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response
