from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from elluminate.schemas.template_variables import TemplateVariables


class TemplateVariablesCollection(BaseModel):
    """Collection of template variables."""

    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class TemplateVariablesCollectionWithEntries(TemplateVariablesCollection):
    """Template variables collection with entries."""

    variables: list[TemplateVariables]


class CreateCollectionRequest(BaseModel):
    """Request to create a new template variables collection."""

    name: str | None = None
    description: str = ""
    variables: list[dict[str, str]] | None = None
