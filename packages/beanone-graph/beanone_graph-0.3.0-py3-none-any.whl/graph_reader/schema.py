"""Schema definitions for graph data structures.

This module defines the schema for graph entities, relations, and their properties
using Pydantic models for validation and type safety.
"""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class EntityProperties(BaseModel):
    """Schema for entity properties.

    This model defines the structure and validation rules for entity properties.
    All properties are nullable to allow for flexible entity types.
    """

    name: str | None = Field(None, description="Entity name")
    type: str | None = Field(None, description="Entity type")
    email: str | None = Field(None, description="Entity email")
    age: int | None = Field(None, description="Entity age")
    tags: list[str] | None = Field(None, description="Entity tags")
    status: str | None = Field(None, description="Entity status")
    community_id: Any | None = Field(
        None,
        description="Entity community identifier. Can be any type that uniquely identifies a community.",
    )
    description: str | None = Field(None, description="Entity description")

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int | None) -> int | None:
        """Validate age is reasonable."""
        if v is not None and (v < 0 or v > 150):  # Reasonable human age range
            raise ValueError("Age must be between 0 and 150")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str | None) -> str | None:
        """Validate email format if provided."""
        if v is not None and "@" not in v:
            raise ValueError("Invalid email format")
        return v


class Entity(BaseModel):
    """Schema for graph entities.

    This model defines the structure and validation rules for graph entities.
    """

    entity_id: Any = Field(..., description="Unique identifier for the entity")
    properties: EntityProperties = Field(..., description="Entity properties")
    last_update_time: datetime | None = Field(None, description="Last update timestamp")

    @field_validator("last_update_time", mode="before")
    @classmethod
    def parse_datetime(cls, v: str | None) -> datetime | None:
        """Parse datetime string, handling ISO format with Z suffix."""
        if v is None:
            return None
        if isinstance(v, str):
            # Remove Z suffix if present
            if v.endswith("Z"):
                v = v[:-1]
            return datetime.fromisoformat(v)
        return v


class Relation(BaseModel):
    """Schema for graph relations.

    This model defines the structure and validation rules for graph relations.
    """

    relation_id: Any = Field(..., description="Unique identifier for the relation")
    source_id: Any = Field(..., description="Source entity ID")
    target_id: Any = Field(..., description="Target entity ID")
    type: str = Field("default", description="Relation type")
    properties: dict[str, Any] = Field(
        default_factory=dict, description="Relation properties"
    )
    last_update_time: datetime | None = Field(None, description="Last update timestamp")

    @field_validator("last_update_time", mode="before")
    @classmethod
    def parse_datetime(cls, v: str | None) -> datetime | None:
        """Parse datetime string, handling ISO format with Z suffix."""
        if v is None:
            return None
        if isinstance(v, str):
            # Remove Z suffix if present
            if v.endswith("Z"):
                v = v[:-1]
            return datetime.fromisoformat(v)
        return v


class AdjacencyRecord(BaseModel):
    """Schema for adjacency list records.

    This model defines the structure and validation rules for adjacency list entries.
    """

    entity_id: Any = Field(..., description="Entity ID")
    relations: list[Any] = Field(
        default_factory=list, description="List of relation IDs"
    )
