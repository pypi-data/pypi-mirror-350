from datetime import datetime
from typing import Any, Dict, List

from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel, model_validator

from elluminate.schemas.base import BatchCreateStatus
from elluminate.schemas.generation_metadata import GenerationMetadata
from elluminate.schemas.prompt import Prompt
from elluminate.schemas.rating import Rating
from elluminate.utils import deprecated


class PromptResponse(BaseModel):
    """Prompt response model."""

    id: int
    prompt: Prompt
    messages: List[ChatCompletionMessageParam]
    generation_metadata: GenerationMetadata | None
    epoch: int
    ratings: list[Rating] = []
    created_at: datetime

    @property
    @deprecated(
        since="0.3.9",
        removal_version="0.4.0",
        alternative="messages property to access chat messages",
    )
    def response(self) -> str:
        """Return the response from the last message."""
        if not self.messages:
            raise ValueError("No messages found in prompt response")

        return self.messages[-1]["content"]

    @model_validator(mode="before")
    @classmethod
    def fix_message_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        # The backend returns a ChatCompletionMessage  (tool_calls is optional) and
        # we expect a ChatCompletionAssistantMessageParam (tool_calls can not be None)
        if "messages" in data and isinstance(data["messages"], list):
            for i, msg in enumerate(data["messages"]):
                if isinstance(msg, dict):
                    if msg.get("role") == "assistant":
                        if "tool_calls" in msg and msg["tool_calls"] is None:
                            del msg["tool_calls"]

        return data


class CreatePromptResponseRequest(BaseModel):
    """Request to create a new prompt response."""

    prompt_template_id: int
    template_variables_id: int
    llm_config_id: int | None = None
    messages: List[ChatCompletionMessageParam] = []
    metadata: GenerationMetadata | None = None


class BatchCreatePromptResponseRequest(BaseModel):
    prompt_response_ins: list[CreatePromptResponseRequest]


class BatchCreatePromptResponseStatus(BatchCreateStatus[PromptResponse]):
    # The result is a tuple with epoch and response
    pass
