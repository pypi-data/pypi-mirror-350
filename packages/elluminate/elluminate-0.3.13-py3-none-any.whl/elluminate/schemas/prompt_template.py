from __future__ import annotations

import re
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Literal

from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel, model_validator

from elluminate.schemas.template_variables_collection import TemplateVariablesCollection
from elluminate.utils import deprecated


class TemplateString(BaseModel):
    """Convenience class for rendering a string with template variables."""

    template_str: str
    _PLACEHOLDER_PATTERN: ClassVar[re.Pattern] = re.compile(r"{{\s*(\w+)\s*}}")

    @property
    def is_template(self) -> bool:
        """Return True if the template string contains any placeholders."""
        return bool(self._PLACEHOLDER_PATTERN.search(self.template_str))

    @property
    def placeholders(self) -> set[str]:
        """Return a set of all the placeholders in the template string."""
        return set(self._PLACEHOLDER_PATTERN.findall(self.template_str))

    def render(self, **kwargs: str) -> str:
        """Render the template string with the given variables. Raises ValueError if any placeholders are missing."""
        if not set(self.placeholders).issubset(set(kwargs.keys())):
            missing = set(self.placeholders) - set(kwargs.keys())
            raise ValueError(f"Missing template variables: {str(missing)}")

        def replacer(regex_match: re.Match[str]) -> str:
            var_name = regex_match.group(1)
            return str(kwargs[var_name])

        return self._PLACEHOLDER_PATTERN.sub(replacer, self.template_str)

    def __str__(self) -> str:
        return self.template_str

    def __eq__(self, other: object) -> bool:
        """Compare TemplateString with another object.

        If other is a string, compare with template_str.
        If other is a TemplateString, compare template_str values.
        """
        if isinstance(other, str):
            return self.template_str == other
        if isinstance(other, TemplateString):
            return self.template_str == other.template_str
        return NotImplemented


class PromptTemplateFilter(BaseModel):
    name: str | None = None
    version: int | Literal["latest"] | None = None
    search: str | None = None
    default_template_variables_collection_id: int | None = None
    criterion_set_id: int | None = None

    @model_validator(mode="after")
    def validate_version_requires_name(self) -> "PromptTemplateFilter":
        if self.version is not None and not self.name:
            raise ValueError("Version can only be set when name is provided")
        return self


class PromptTemplate(BaseModel):
    """Prompt template model."""

    id: int
    name: str
    version: int
    messages: List[ChatCompletionMessageParam] = []
    default_template_variables_collection: TemplateVariablesCollection
    parent_prompt_template: "PromptTemplate | None" = None
    created_at: datetime
    updated_at: datetime

    @property
    @deprecated(
        since="0.3.9",
        removal_version="0.4.0",
        alternative="messages property to access chat messages",
    )
    def user_prompt_template(self) -> TemplateString:
        """Return the user prompt template string."""
        if len(self.messages) == 1:
            return TemplateString(template_str=self.messages[0]["content"])
        elif len(self.messages) > 1:
            return TemplateString(
                template_str="\n\n".join(f"[{msg['role']}]: {msg['content']}" for msg in self.messages)
            )
        else:
            raise ValueError("No messages found in prompt template / error in conversion")

    @model_validator(mode="before")
    @classmethod
    def fix_message_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        # OpenAI's ChatCompletionAssistantMessageParam requires a tool_calls field.
        # Since this field is not always included, we initialize it
        # as an empty list when absent to ensure compatibility.
        if "messages" in data and isinstance(data["messages"], list):
            for i, msg in enumerate(data["messages"]):
                if isinstance(msg, dict):
                    if msg.get("role") == "assistant":
                        if "tool_calls" not in msg or msg["tool_calls"] is None:
                            data["messages"][i]["tool_calls"] = []

        return data


class CreatePromptTemplateRequest(BaseModel):
    """Request to create a new prompt template."""

    name: str | None = None
    messages: List[ChatCompletionMessageParam] = []
    parent_prompt_template_id: int | None = None
    default_collection_id: int | None = None
