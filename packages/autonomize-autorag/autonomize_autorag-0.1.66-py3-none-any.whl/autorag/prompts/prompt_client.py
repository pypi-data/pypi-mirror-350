""" Prompt Client for managing prompts extending BaseClient """

from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from autorag.core.base_client import BaseClient
from autorag.exceptions.core.credentials import (
    ModelHubException,
    ModelHubParsingException,
    ModelhubUnauthorizedException,
)
from autorag.types.prompts import Prompt, PromptVersion, PromptWithVersion
from autorag.utilities.logger import get_logger

logger = get_logger(__name__)

NO_PROMPT_FOUND = "No Prompt Found"


# pylint: disable=too-many-public-methods
class PromptClient(BaseClient):
    """Client for managing prompts with both synchronous and asynchronous methods."""

    def create_prompt(
        self,
        name: str,
        template: str,
        prompt_type: str = "USER",
        description: Optional[str] = None,
    ) -> PromptWithVersion:
        """
        Creates a new prompt and stores it in the database (synchronous).

        Args:
            name (str): The name of the prompt.
            template (str): The prompt template.
            prompt_type (str, optional): The type of prompt (USER or SYSTEM). Defaults to "USER".
            description (Optional[str], optional): A description of the prompt. Defaults to None.

        Returns:
            PromptWithVersion: The newly created prompt object with its version.

        Raises:
            ModelHubBadRequestException: If the prompt data is invalid.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = "prompts"

        # Create payload directly without using models
        payload = {
            "name": name,
            "template": template,
            "prompt_type": prompt_type,
        }

        if description is not None:
            payload["description"] = description

        # Send request
        response = self.post(endpoint, json=payload)

        try:
            if isinstance(response, dict):
                return PromptWithVersion(**response)
            if isinstance(response, str):
                logger.warning("Received string response in create_prompt")
                return PromptWithVersion.model_validate_json(response)

            logger.error(
                "Unexpected response type in create_prompt: %s", type(response)
            )
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in create_prompt: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse create_prompt response: {str(e)}"
            ) from e

    async def acreate_prompt(
        self,
        name: str,
        template: str,
        prompt_type: str = "USER",
        description: Optional[str] = None,
    ) -> PromptWithVersion:
        """
        Creates a new prompt and stores it in the database (asynchronous).

        Args:
            name (str): The name of the prompt.
            template (str): The prompt template.
            prompt_type (str, optional): The type of prompt (USER or SYSTEM). Defaults to "USER".
            description (Optional[str], optional): A description of the prompt. Defaults to None.

        Returns:
            PromptWithVersion: The newly created prompt object with its version.

        Raises:
            ModelHubBadRequestException: If the prompt data is invalid.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = "prompts"

        # Create payload directly without using models
        payload = {
            "name": name,
            "template": template,
            "prompt_type": prompt_type,
        }

        if description is not None:
            payload["description"] = description

        # Send async request
        response = await self.apost(endpoint, json=payload)

        try:
            if isinstance(response, dict):
                return PromptWithVersion(**response)
            if isinstance(response, str):
                logger.warning("Received string response in acreate_prompt")
                return PromptWithVersion.model_validate_json(response)

            logger.error(
                "Unexpected response type in acreate_prompt: %s", type(response)
            )
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in acreate_prompt: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse acreate_prompt response: {str(e)}"
            ) from e

    def add_version(self, prompt_name: str, template: str) -> PromptVersion:
        """
        Adds a new version to an existing prompt in the database (synchronous).

        Args:
            prompt_name (str): The name of the existing prompt.
            template (str): The template content for the new version.

        Returns:
            PromptVersion: The newly created prompt version.

        Raises:
            ModelHubResourceNotFoundException: If the prompt does not exist.
            ModelHubBadRequestException: If the version data is invalid.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/{prompt_name}"

        # Create payload directly
        payload = {"template": template}

        # Send request
        response = self.post(endpoint, json=payload)

        try:
            if isinstance(response, dict):
                return PromptVersion(**response)

            logger.error("Unexpected response type in add_version: %s", type(response))
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in add_version: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse add_version response: {str(e)}"
            ) from e

    async def aadd_version(self, prompt_name: str, template: str) -> PromptVersion:
        """
        Adds a new version to an existing prompt in the database (asynchronous).

        Args:
            prompt_name (str): The name of the existing prompt.
            template (str): The template content for the new version.

        Returns:
            PromptVersion: The newly created prompt version.

        Raises:
            ModelHubResourceNotFoundException: If the prompt does not exist.
            ModelHubBadRequestException: If the version data is invalid.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/{prompt_name}"

        # Create payload directly
        payload = {"template": template}

        # Send async request
        response = await self.apost(endpoint, json=payload)

        try:
            if isinstance(response, dict):
                return PromptVersion(**response)

            logger.error("Unexpected response type in aadd_version: %s", type(response))
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in aadd_version: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse aadd_version response: {str(e)}"
            ) from e

    def get_all(self, prompt_type: Optional[str] = None) -> List[Prompt]:
        """
        Retrieves all prompts from the database (synchronous).

        Args:
            prompt_type (Optional[str]): Filter prompts by type.

        Returns:
            List[Prompt]: A list of all stored prompt objects.

        Raises:
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = "prompts"
        if prompt_type:
            endpoint = f"prompts?prompt_type={prompt_type}"

        response = self.get(endpoint)

        # Handle different response formats
        if isinstance(response, list):
            # If response is already a list
            try:
                return [
                    (
                        Prompt(**item)
                        if isinstance(item, dict)
                        else Prompt.model_validate(item)
                    )
                    for item in response
                ]
            except Exception as e:
                logger.error("Error parsing response in get_all: %s", e)
                logger.debug("Response content: %s", response)
                raise ModelHubParsingException(
                    f"Failed to parse get_all response: {str(e)}"
                ) from e
        if isinstance(response, dict) and "items" in response:
            # If response is paginated with an 'items' field
            items = response.get("items", [])
            try:
                return [Prompt(**item) for item in items]
            except Exception as e:
                logger.error("Error parsing paginated response in get_all: %s", e)
                raise ModelHubParsingException(
                    f"Failed to parse paginated response: {str(e)}"
                ) from e

        # If response is in unexpected format
        logger.error("Unexpected response format in get_all: %s", type(response))
        logger.debug("Response content: %s", response)
        raise ModelHubParsingException(f"Unexpected response format: {type(response)}")

    async def aget_all(self, prompt_type: Optional[str] = None) -> List[Prompt]:
        """
        Retrieves all prompts from the database (asynchronous).

        Args:
            prompt_type (Optional[str]): Filter prompts by type.

        Returns:
            List[Prompt]: A list of all stored prompt objects.

        Raises:
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = "prompts"
        if prompt_type:
            endpoint = f"prompts?prompt_type={prompt_type}"

        response = await self.aget(endpoint)

        # Handle different response formats
        if isinstance(response, list):
            # If response is already a list
            try:
                return [
                    (
                        Prompt(**item)
                        if isinstance(item, dict)
                        else Prompt.model_validate(item)
                    )
                    for item in response
                ]
            except Exception as e:
                logger.error("Error parsing response in aget_all: %s", e)
                logger.debug("Response content: %s", response)
                raise ModelHubParsingException(
                    f"Failed to parse aget_all response: {str(e)}"
                ) from e
        if isinstance(response, dict) and "items" in response:
            # If response is paginated with an 'items' field
            items = response.get("items", [])
            try:
                return [Prompt(**item) for item in items]
            except Exception as e:
                logger.error("Error parsing paginated response in aget_all: %s", e)
                raise ModelHubParsingException(
                    f"Failed to parse paginated response: {str(e)}"
                ) from e

        # If response is in unexpected format
        logger.error("Unexpected response format in aget_all: %s", type(response))
        logger.debug("Response content: %s", response)
        raise ModelHubParsingException(f"Unexpected response format: {type(response)}")

    def get_versions(self, prompt_name: Optional[str] = None) -> List[PromptVersion]:
        """
        Retrieves all versions of a given prompt (synchronous).

        Args:
            prompt_name (Optional[str]): The name of the prompt. If None, retrieves all versions.

        Returns:
            List[PromptVersion]: A list of all versions of the specified prompt.

        Raises:
            ModelHubResourceNotFoundException: If the prompt does not exist.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = "prompts/versions"
        if prompt_name:
            endpoint = f"{endpoint}?prompt_name={prompt_name}"

        response = self.get(endpoint)

        # Handle different response formats
        if isinstance(response, list):
            try:
                return [
                    (
                        PromptVersion(**item)
                        if isinstance(item, dict)
                        else PromptVersion.model_validate(item)
                    )
                    for item in response
                ]
            except Exception as e:
                logger.error("Error parsing response in get_versions: %s", e)
                logger.debug("Response content: %s", response)
                raise ModelHubParsingException(
                    f"Failed to parse get_versions response: {str(e)}"
                ) from e
        if isinstance(response, dict) and "items" in response:
            # If response is paginated
            items = response.get("items", [])
            try:
                return [PromptVersion(**item) for item in items]
            except Exception as e:
                logger.error("Error parsing paginated response in get_versions: %s", e)
                raise ModelHubParsingException(
                    f"Failed to parse paginated response: {str(e)}"
                ) from e

        logger.error("Unexpected response format in get_versions: %s", type(response))
        logger.debug("Response content: %s", response)
        raise ModelHubParsingException(f"Unexpected response format: {type(response)}")

    async def aget_versions(
        self, prompt_name: Optional[str] = None
    ) -> List[PromptVersion]:
        """
        Retrieves all versions of a given prompt (asynchronous).

        Args:
            prompt_name (Optional[str]): The name of the prompt. If None, retrieves all versions.

        Returns:
            List[PromptVersion]: A list of all versions of the specified prompt.

        Raises:
            ModelHubResourceNotFoundException: If the prompt does not exist.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = "prompts/versions"
        if prompt_name:
            endpoint = f"{endpoint}?prompt_name={prompt_name}"

        response = await self.aget(endpoint)

        # Handle different response formats
        if isinstance(response, list):
            try:
                return [
                    (
                        PromptVersion(**item)
                        if isinstance(item, dict)
                        else PromptVersion.model_validate(item)
                    )
                    for item in response
                ]
            except Exception as e:
                logger.error("Error parsing response in aget_versions: %s", e)
                logger.debug("Response content: %s", response)
                raise ModelHubParsingException(
                    f"Failed to parse aget_versions response: {str(e)}"
                ) from e
        if isinstance(response, dict) and "items" in response:
            # If response is paginated
            items = response.get("items", [])
            try:
                return [PromptVersion(**item) for item in items]
            except Exception as e:
                logger.error("Error parsing paginated response in aget_versions: %s", e)
                raise ModelHubParsingException(
                    f"Failed to parse paginated response: {str(e)}"
                ) from e

        logger.error("Unexpected response format in aget_versions: %s", type(response))
        logger.debug("Response content: %s", response)
        raise ModelHubParsingException(f"Unexpected response format: {type(response)}")

    def get_version(
        self, prompt_name: str, version: Optional[str] = None
    ) -> PromptVersion:
        """
        Retrieves a specific version of a given prompt,
        or the latest version if none is specified (synchronous).

        Args:
            prompt_name (str): The name of the prompt.
            version (Optional[str]): The specific version to fetch.
            If None, retrieves the latest version.

        Returns:
            PromptVersion: The requested prompt version.

        Raises:
            ModelHubResourceNotFoundException: If the prompt or version is not found.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/{prompt_name}/version"
        if version:
            endpoint = f"{endpoint}?version={version}"

        response = self.get(endpoint)

        try:
            if isinstance(response, dict):
                return PromptVersion(**response)
            if isinstance(response, str):
                # If response is a string, try to parse it as JSON
                logger.warning(
                    "Received string response in get_version: %s...", response[:100]
                )
                return PromptVersion.model_validate_json(response)

            logger.error("Unexpected response type in get_version: %s", type(response))
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in get_version: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse get_version response: {str(e)}"
            ) from e

    async def aget_version(
        self, prompt_name: str, version: Optional[str] = None
    ) -> PromptVersion:
        """
        Retrieves a specific version of a given prompt,
        or the latest version if none is specified (asynchronous).

        Args:
            prompt_name (str): The name of the prompt.
            version (Optional[str]): The specific version to fetch.
            If None, retrieves the latest version.

        Returns:
            PromptVersion: The requested prompt version.

        Raises:
            ModelHubResourceNotFoundException: If the prompt or version is not found.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/{prompt_name}/version"
        if version:
            endpoint = f"{endpoint}?version={version}"

        response = await self.aget(endpoint)

        try:
            if isinstance(response, dict):
                return PromptVersion(**response)
            if isinstance(response, str):
                # If response is a string, try to parse it as JSON
                logger.warning(
                    "Received string response in aget_version: %s...", response[:100]
                )
                return PromptVersion.model_validate_json(response)

            logger.error("Unexpected response type in aget_version: %s", type(response))
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in aget_version: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse aget_version response: {str(e)}"
            ) from e

    def get_by_id(self, prompt_id: UUID) -> Prompt:
        """
        Retrieves a specific prompt by its ID (synchronous).

        Args:
            prompt_id (UUID): The unique identifier of the prompt.

        Returns:
            Prompt: The found prompt object.

        Raises:
            ModelHubResourceNotFoundException: If the prompt is not found.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/id/{prompt_id}"
        response = self.get(endpoint)

        try:
            if isinstance(response, dict):
                return Prompt(**response)

            logger.error("Unexpected response type in get_by_id: %s", type(response))
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in get_by_id: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse get_by_id response: {str(e)}"
            ) from e

    async def aget_by_id(self, prompt_id: UUID) -> Prompt:
        """
        Retrieves a specific prompt by its ID (asynchronous).

        Args:
            prompt_id (UUID): The unique identifier of the prompt.

        Returns:
            Prompt: The found prompt object.

        Raises:
            ModelHubResourceNotFoundException: If the prompt is not found.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/id/{prompt_id}"
        response = await self.aget(endpoint)

        try:
            if isinstance(response, dict):
                return Prompt(**response)

            logger.error("Unexpected response type in aget_by_id: %s", type(response))
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in aget_by_id: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse aget_by_id response: {str(e)}"
            ) from e

    def get_by_name(self, name: str) -> Prompt:
        """
        Retrieves a specific prompt by its name (synchronous).

        Args:
            name (str): The unique name of the prompt.

        Returns:
            Prompt: The found prompt object.

        Raises:
            ModelHubResourceNotFoundException: If the prompt is not found.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/name/{name}"
        response = self.get(endpoint)

        try:
            if isinstance(response, dict):
                return Prompt(**response)

            logger.error("Unexpected response type in get_by_name: %s", type(response))
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in get_by_name: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse get_by_name response: {str(e)}"
            ) from e

    async def aget_by_name(self, name: str) -> Prompt:
        """
        Retrieves a specific prompt by its name (asynchronous).

        Args:
            name (str): The unique name of the prompt.

        Returns:
            Prompt: The found prompt object.

        Raises:
            ModelHubResourceNotFoundException: If the prompt is not found.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/name/{name}"
        response = await self.aget(endpoint)

        try:
            if isinstance(response, dict):
                return Prompt(**response)

            logger.error("Unexpected response type in aget_by_name: %s", type(response))
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in aget_by_name: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse aget_by_name response: {str(e)}"
            ) from e

    def update(
        self,
        prompt_id: Union[str, UUID],
        name: Optional[str] = None,
        prompt_type: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Prompt:
        """
        Updates an existing prompt in the database (synchronous).

        Args:
            prompt_id (Union[str, UUID]): The unique identifier of the prompt to update.
            name (Optional[str], optional): The new name for the prompt. Defaults to None.
            prompt_type (Optional[str], optional): The new type for the prompt. Defaults to None.
            description (Optional[str], optional): The new description for the prompt.
            Defaults to None.

        Returns:
            Prompt: The updated prompt object.

        Raises:
            ModelHubResourceNotFoundException: If the prompt is not found.
            ModelHubBadRequestException: If the update data is invalid.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/{prompt_id}"

        # Create payload directly
        payload = {}
        if name is not None:
            payload["name"] = name
        if prompt_type is not None:
            payload["prompt_type"] = prompt_type
        if description is not None:
            payload["description"] = description

        response = self.patch(endpoint, json=payload)

        try:
            if isinstance(response, dict):
                return Prompt(**response)

            logger.error("Unexpected response type in update: %s", type(response))
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in update: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse update response: {str(e)}"
            ) from e

    async def aupdate(
        self,
        prompt_id: Union[str, UUID],
        name: Optional[str] = None,
        prompt_type: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Prompt:
        """
        Updates an existing prompt in the database (asynchronous).

        Args:
            prompt_id (Union[str, UUID]): The unique identifier of the prompt to update.
            name (Optional[str], optional): The new name for the prompt. Defaults to None.
            prompt_type (Optional[str], optional): The new type for the prompt. Defaults to None.
            description (Optional[str], optional): The new description for the prompt.
            Defaults to None.

        Returns:
            Prompt: The updated prompt object.

        Raises:
            ModelHubResourceNotFoundException: If the prompt is not found.
            ModelHubBadRequestException: If the update data is invalid.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/{prompt_id}"

        # Create payload directly
        payload = {}
        if name is not None:
            payload["name"] = name
        if prompt_type is not None:
            payload["prompt_type"] = prompt_type
        if description is not None:
            payload["description"] = description

        response = await self.apatch(endpoint, json=payload)

        try:
            if isinstance(response, dict):
                return Prompt(**response)

            logger.error("Unexpected response type in aupdate: %s", type(response))
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in aupdate: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse aupdate response: {str(e)}"
            ) from e

    def update_version(
        self,
        prompt_name: str,
        template: str,
        version: Optional[str] = None,
    ) -> PromptVersion:
        """
        Updates an existing prompt version in the database (synchronous).

        Args:
            prompt_name (str): The name of the prompt.
            template (str): The new template content.
            version (Optional[str]): The specific version to update (if not provided,
            the latest version is updated).

        Returns:
            PromptVersion: The updated prompt version object.

        Raises:
            ModelHubResourceNotFoundException: If the prompt or version is not found.
            ModelHubBadRequestException: If the update data is invalid.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/{prompt_name}/version"
        if version:
            endpoint = f"{endpoint}?version={version}"

        # Create payload directly
        payload = {"template": template}

        response = self.patch(endpoint, json=payload)

        try:
            if isinstance(response, dict):
                return PromptVersion(**response)

            logger.error(
                "Unexpected response type in update_version: %s", type(response)
            )
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in update_version: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse update_version response: {str(e)}"
            ) from e

    async def aupdate_version(
        self,
        prompt_name: str,
        template: str,
        version: Optional[str] = None,
    ) -> PromptVersion:
        """
        Updates an existing prompt version in the database (asynchronous).

        Args:
            prompt_name (str): The name of the prompt.
            template (str): The new template content.
            version (Optional[str]): The specific version to update (if not provided,
            the latest version is updated).

        Returns:
            PromptVersion: The updated prompt version object.

        Raises:
            ModelHubResourceNotFoundException: If the prompt or version is not found.
            ModelHubBadRequestException: If the update data is invalid.
            ModelHubParsingException: If response parsing fails.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/{prompt_name}/version"
        if version:
            endpoint = f"{endpoint}?version={version}"

        # Create payload directly
        payload = {"template": template}

        response = await self.apatch(endpoint, json=payload)

        try:
            if isinstance(response, dict):
                return PromptVersion(**response)

            logger.error(
                "Unexpected response type in aupdate_version: %s", type(response)
            )
            raise ModelHubParsingException(
                f"Unexpected response format: {type(response)}"
            )
        except Exception as e:
            logger.error("Error parsing response in aupdate_version: %s", e)
            logger.debug("Response content: %s", response)
            if isinstance(e, (ModelHubException, ModelhubUnauthorizedException)):
                raise
            raise ModelHubParsingException(
                f"Failed to parse aupdate_version response: {str(e)}"
            ) from e

    def delete_prompt(self, prompt_id: Union[str, UUID]) -> Dict[str, Any]:
        """
        Deletes a prompt from the database (synchronous).

        Args:
            prompt_id (Union[str, UUID]): The unique identifier of the prompt to delete.

        Returns:
            Dict[str, Any]: The response message.

        Raises:
            ModelHubResourceNotFoundException: If the prompt is not found.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/{prompt_id}"
        return self.delete(endpoint)

    async def adelete_prompt(self, prompt_id: Union[str, UUID]) -> Dict[str, Any]:
        """
        Deletes a prompt from the database (asynchronous).

        Args:
            prompt_id (Union[str, UUID]): The unique identifier of the prompt to delete.

        Returns:
            Dict[str, Any]: The response message.

        Raises:
            ModelHubResourceNotFoundException: If the prompt is not found.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/{prompt_id}"
        return await self.adelete(endpoint)

    def delete_version(
        self, prompt_id: Union[str, UUID], version: str
    ) -> Dict[str, Any]:
        """
        Deletes a specific version of a prompt from the database (synchronous).

        Args:
            prompt_id (Union[str, UUID]): The unique identifier of the prompt.
            version (str): The version number to delete.

        Returns:
            Dict[str, Any]: The response message.

        Raises:
            ModelHubResourceNotFoundException: If the prompt or version is not found.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/{prompt_id}/{version}"
        return self.delete(endpoint)

    async def adelete_version(
        self, prompt_id: Union[str, UUID], version: str
    ) -> Dict[str, Any]:
        """
        Deletes a specific version of a prompt from the database (asynchronous).

        Args:
            prompt_id (Union[str, UUID]): The unique identifier of the prompt.
            version (str): The version number to delete.

        Returns:
            Dict[str, Any]: The response message.

        Raises:
            ModelHubResourceNotFoundException: If the prompt or version is not found.
            ModelhubUnauthorizedException: If the credentials are invalid.
            ModelHubException: For other API errors.
        """
        endpoint = f"prompts/{prompt_id}/{version}"
        return await self.adelete(endpoint)
