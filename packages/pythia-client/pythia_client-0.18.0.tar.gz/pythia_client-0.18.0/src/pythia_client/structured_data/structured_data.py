"""Structured data extraction functionality."""

import io
import os
import json
import requests
from typing import Dict, Any, Tuple, Literal
from urllib.parse import urljoin

from pythia_client.schema import DataExtractResponse, DataExtractTask
from pythia_client.utils.base import BaseService
from pythia_client.utils.http import create_basic_headers


class StructuredDataService(BaseService):
    """Service for pipeline operations."""

    def __init__(self, url: str, api_key: str):
        """Initialize the structured data extraction service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.data_extraction_endpoint = urljoin(
            str(self.url), "/data-extraction/extract-structured-data"
        )

    def extract_structured_data(
        self,
        file: str | Tuple[str, io.IOBase] | None = None,
        string_content: str | None = None,
        additional_instructions: str | None = None,
        json_schema: Dict[str, Any] | None = None,
        preset: Literal["esr-mail", "pk-list"] | None = None,
        extraction_mode: Literal["fast", "precise"] | None = "fast",
    ) -> DataExtractResponse:
        """This method extracts structured data according to a JSON schema. The input data can either be a text (string) or a file (such as PDF, Word, Email), but not both.

        The JSON schema to extract and additional instructions can be provided by the user, or you can use one of the presets developed by BTQ (`esr-mail`, `pk-list`). The extraction can run in two different modes: fast (single step LLM extraction) or precise (looping LLM).

        This extraction is asynchronous and the endpoint returns a 202 status with a job_uuid that can be used to check the status of the background task running. The extraction result will be a JSON validated to the provided JSON schema.

        Args:
            file: The path to the file OR tuple of filename and file object to extract the data from. Exclusive with `string_content` parameter. The file is processed with Tika.
            string_content: The string content to extract the data from. Exclusive with `file` parameter.
            additional_instructions: Additional instructions for the extraction. It will be inserted in the LLM prompt to help him extract information as expected.
            json_schema: The JSON schema to validate the extracted data, needed if no preset set. Exclusive with preset parameter
            preset: The preset to use for the extraction, it overwrites `json_schema` and add specific `additional_instructions` with our default values. Can be `esr-mail` or `pk-list`. Exclusive with `json_schema` parameter.
            extraction_mode: The extraction mode to use. Default to `fast` (single step LLM tool-use). Can also be `precise` (looping LLM requests with schema validator).

        Returns:
            The response from the API. Raise an exception with API status code and error message if the status code is not 202.

        Usage:
        ```python
        extract_structured_data_response = client.extract_structured_data("path/to/file.pdf", preset="pk-list")
        {"message": "Content Submitted. Data extract task created.", "job_uuid": "abc123-def456-ghj789"}

        extract_structured_data_response = client.extract_structured_data(("file.pdf", file), preset="pk-list")
        {"message": "Content Submitted. Data extract task created.", "job_uuid": "abc123-def456-ghj789"}


        string_content = "Hey, I have an issue with my MyPortal access."
        additional_instructions = "If myportal issue please name the ticket_category as MP_ACCESS"
        json_schema = json.loads('''{"$schema":"http://json-schema.org/draft-04/schema#","type":"object","properties":{"ticket_category":{"type":"string"}},"required":["ticket_category"]}''')

        response = client.extract_structured_data(string_content=string_content, additional_instructions=additional_instructions, json_schema=json_schema, extraction_mode="precise")
        ```
        """
        prepared_file = []
        if file:
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
                    "File must be a file path or a tuple of (filename, fileIObyte)"
                )

            prepared_file.append(("file", (file_name, file_content)))

        if prepared_file == [] and not string_content:
            raise ValueError(
                "You must provide a file or string content to extract the data from."
            )
        if not json_schema and not preset:
            raise ValueError("You must provide a json_schema or a preset.")
        if json_schema and preset:
            raise ValueError("You can't provide both a json_schema and a preset.")
        if extraction_mode not in ["fast", "precise"]:
            raise ValueError("extraction_mode must be 'fast' or 'precise'.")

        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            data = {}
            if string_content:
                data["string_content"] = string_content
            data["additional_instructions"] = (
                additional_instructions if additional_instructions else None
            )
            data["json_schema"] = json.dumps(json_schema) if json_schema else None
            data["preset"] = preset if preset else None
            data["extraction_mode"] = extraction_mode if extraction_mode else None

            with session.post(
                self.data_extraction_endpoint,
                files=prepared_file if prepared_file else None,
                data=data,
                headers=headers,
            ) as response:
                if response.status_code == 202:
                    api_response = response.json()
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return DataExtractResponse.model_validate(api_response)

    def get_extract_structured_data_job(
        self,
        job_uuid: str,
    ) -> DataExtractTask:
        """Get the status and result of a data extract task based on its job UUID. When the `status` is `completed`, The resulting extracted JSON is under the `result_json` key of the return response.

        Args:
            job_uuid: The job UUID from the data extract task.

        Returns:
            The response from the API. Raise an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        data_extract_task_result = client.get_extract_structured_data_job("abc123-def456-ghj789")
        data_extract_task_result.model_dump()["result_json"]
        ```
        """
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            with session.get(
                self.data_extraction_endpoint + f"/{job_uuid}",
                headers=headers,
            ) as response:
                if response.status_code == 200:
                    api_response = DataExtractTask(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response
