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
    """MongoDB document model for prompts"""

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
    """MongoDB document model for prompts versions"""

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
    name: str = None
    prompt_type: Optional[str] = None
    description: Optional[str] = None
    template: str


class PromptWithVersion(BaseModel):
    name: str
    prompt_type: str
    description: Optional[str] = None
    template: str
    prompt_id: str
    id: Optional[str] = None
    version: str


class CreatePromptVersion(BaseModel):
    template: str


class ReadPrompt(PromptBase):
    id: str


class ReadPromptByName(PromptBase):
    name: str


class UpdatePrompt(BaseModel):
    name: Optional[str] = None
    prompt_type: Optional[str] = None
    description: Optional[str] = None


class UpdatePromptVersion(BaseModel):
    template: Optional[str] = None
