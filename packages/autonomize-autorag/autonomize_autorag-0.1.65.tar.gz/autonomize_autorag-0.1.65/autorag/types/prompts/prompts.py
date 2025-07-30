""" This module contains Pydantic models for prompt-related functionality.

These models define the data structures for storing, retrieving, and manipulating prompts.
Prompts are stored with their metadata and template content, and can have multiple versions.
"""

from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


def utc_now():
    """
    Get the current UTC time.

    Returns:
        datetime: The current datetime in UTC timezone.
    """
    return datetime.now(timezone.utc)


class PromptBase(BaseModel):
    """
    Base class for prompt models containing common fields.

    This class defines the common fields that all prompt-related models share,
    such as name, description, type, and timestamps.
    """

    name: str = Field()
    description: Optional[str] = Field(default=None)
    prompt_type: Literal["USER", "SYSTEM"] = Field(
        default="USER", description="Prompt type"
    )
    created_at: datetime = Field(
        default_factory=utc_now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=utc_now, description="Last update timestamp"
    )
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
        }
    )


class VersionBase(BaseModel):
    """
    Base class for prompt version models containing common fields.

    This class defines the common fields that all prompt version models share,
    such as template content, version identifier, prompt ID, and timestamps.
    """

    template: str
    version: str = Field(default="1")
    prompt_id: str
    created_at: datetime = Field(
        default_factory=utc_now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=utc_now, description="Last update timestamp"
    )
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
        }
    )


class Prompt(PromptBase):
    """
    MongoDB document model for prompts.

    This class extends PromptBase to include a unique identifier for
    the prompt and provides methods to convert the model to data format.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique identifier"
    )

    def to_data(self):
        """
        Serializes the Prompt object into a dictionary format.

        This method converts the Prompt model instance into a dictionary
        by extracting specific fields while ensuring the `id` field is
        included separately.

        Returns:
            dict: A dictionary containing the prompt's attributes:
                - `id` (str): The unique identifier of the prompt.
                - `name` (str): The name of the prompt.
                - `description` (str): A brief description of the prompt.
                - `prompt_type` (str): The type/category of the prompt.
                - `created_at` (datetime): Timestamp of when the prompt was created.
                - `updated_at` (datetime): Timestamp of the last update to the prompt.
        """
        serialized = self.model_dump()
        return {
            "id": serialized.pop("id"),
            "name": serialized.pop("name"),
            "description": serialized.pop("description"),
            "prompt_type": serialized.pop("prompt_type"),
            "created_at": serialized.pop("created_at"),
            "updated_at": serialized.pop("updated_at"),
        }


class PromptVersion(VersionBase):
    """
    MongoDB document model for prompt versions.

    This class extends VersionBase to include a unique identifier for
    the prompt version and provides methods to convert the model to data format.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique identifier"
    )

    def to_data(self):
        """
        Serializes the PromptVersion object into a dictionary format.

        This method converts the PromptVersion model instance into a dictionary
        by extracting specific fields while ensuring the `id` field is
        included separately.

        Returns:
            dict: A dictionary containing the prompt version's attributes:
                - `id` (str): The unique identifier of the prompt version.
                - `version` (str): The version of the prompt.
                - `template` (str): Template of the prompt.
                - `prompt_id` (str): ID of the prompt.
                - `created_at` (datetime): Timestamp of when the prompt version was created.
                - `updated_at` (datetime): Timestamp of the last update to the prompt version.
        """
        serialized = self.model_dump()
        return {
            "id": serialized.pop("id"),
            "version": serialized.pop("version"),
            "template": serialized.pop("template"),
            "prompt_id": serialized.pop("prompt_id"),
            "created_at": serialized.pop("created_at"),
            "updated_at": serialized.pop("updated_at"),
        }


class CreatePrompt(BaseModel):
    """
    Model for creating a new prompt.

    This model contains the required fields for creating a new prompt,
    including the template content for the initial version.
    """

    name: str
    prompt_type: str
    description: Optional[str] = None
    template: str


class PromptWithVersion(BaseModel):
    """
    Model representing a prompt with its version information.

    This combined model is used to return both prompt metadata and
    its version details in a single response.
    """

    name: str
    prompt_type: str
    description: Optional[str] = None
    template: str
    prompt_id: str
    id: Optional[str] = None
    version: str


class CreatePromptVersion(BaseModel):
    """
    Model for creating a new prompt version.

    This model contains the template content required for creating
    a new version of an existing prompt.
    """

    template: str


class ReadPrompt(PromptBase):
    """
    Model for reading a prompt with its ID.

    This model extends PromptBase to include the prompt's unique identifier
    and is used for API responses when retrieving a prompt.
    """

    id: str


class ReadPromptByName(PromptBase):
    """
    Model for reading a prompt by its name.

    This model is used for API responses when retrieving a prompt by name.
    """

    name: str


class UpdatePrompt(BaseModel):
    """
    Model for updating an existing prompt.

    This model contains optional fields that can be updated for an existing prompt.
    Only the fields that are provided will be updated.
    """

    name: Optional[str] = None
    prompt_type: Optional[str] = None
    description: Optional[str] = None


class UpdatePromptVersion(BaseModel):
    """
    Model for updating an existing prompt version.

    This model contains optional fields that can be updated for an existing
    prompt version. Only the fields that are provided will be updated.
    """

    template: Optional[str] = None
