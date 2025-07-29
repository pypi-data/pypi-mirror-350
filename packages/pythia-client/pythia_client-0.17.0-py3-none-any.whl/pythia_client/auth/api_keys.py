"""API key management functionality."""

import requests
from typing import List
from urllib.parse import urljoin

from pythia_client.schema import ApiKeys, Permissions
from pythia_client.utils.base import BaseService
from pythia_client.utils.http import create_basic_headers


class ApiKeyService(BaseService):
    """Service for API key management."""

    def __init__(self, url: str, api_key: str):
        """Initialize the API key service.

        Args:
            url: The base URL for the API.
            api_key: The API key for authentication.
        """
        super().__init__(url, api_key)
        self.api_keys_endpoint = urljoin(str(self.url), "/api-keys")

    def create_api_key(
        self,
        name: str,
        creator_id: str,
        group_id: str,
        permission: Permissions,
    ) -> ApiKeys:
        """Create an API key for a group_id.

        Args:
            name: The name of the API key.
            creator_id: The creator_id of the API key (streamlit user often).
            group_id: The group_id of the API key (cognito group name).
            permission: The permission of the API key  (full or read).

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict.
            Raises an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        api_response = client.create_api_key("my key", "e9824-d710c-f9018-82jh", "btq-group", "full")
        api_response.model_dump()
        ```
        """
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            data = {
                "name": name,
                "creator_id": creator_id,
                "group_id": group_id,
                "permission": permission,
            }
            with session.post(
                self.api_keys_endpoint + "/create", headers=headers, json=data
            ) as response:
                if response.status_code == 200:
                    api_response = ApiKeys(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response

    def revoke_api_key(
        self,
        api_key_to_revoke: str,
        creator_id: str,
    ) -> ApiKeys:
        """Revoke and API key.

        Args:
            api_key_to_revoke: The API key to revoke
            creator_id: The creator_id of the API key (streamlit user often).

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict.
            Raises an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        api_response = client.revoke_api_key(api_key_to_revoke="abe4arg84are9g4bear65gb16DS61", creator_id="e9824-d710c-f9018-82jh")
        api_response.model_dump()
        ```
        """
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            data = {"creator_id": creator_id}
            with session.delete(
                self.api_keys_endpoint + f"/revoke/{api_key_to_revoke}",
                params=data,
                headers=headers,
            ) as response:
                if response.status_code == 200:
                    api_response = ApiKeys(**response.json())
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response

    def list_api_keys_by_group_id(
        self,
        group_id: str,
    ) -> List[ApiKeys]:
        """List API Keys for a specific group_id.

        Args:
            group_id: Group ID to list the API keys from

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict.
            Raises an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        api_response = client.list_api_keys_by_group_id(group_id="btq-group")
        api_response.model_dump()
        ```
        """
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            with session.get(
                self.api_keys_endpoint + f"/list/by-group-id/{group_id}",
                headers=headers,
            ) as response:
                if response.status_code == 200:
                    api_response = [ApiKeys(**resp) for resp in response.json()]
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response

    def list_api_keys_by_creator_id(
        self,
        creator_id: str,
    ) -> List[ApiKeys]:
        """List API Keys for a specific creator_id.

        Args:
            creator_id: Creator ID to list the API keys from

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict.
            Raises an exception with API status code and error message if the status code is not 200.

        Usage:
        ```python
        api_response = client.list_api_keys_by_creator_id(creator_id="e9824-d710c-f9018-82jh")
        api_response.model_dump()
        ```
        """
        with requests.Session() as session:
            headers = create_basic_headers(self.api_key)
            with session.get(
                self.api_keys_endpoint + f"/list/by-creator-id/{creator_id}",
                headers=headers,
            ) as response:
                if response.status_code == 200:
                    api_response = [ApiKeys(**resp) for resp in response.json()]
                else:
                    raise Exception(
                        f"Pythia API Error {response.status_code}: {self._process_error_response(response)}"
                    )
        return api_response
