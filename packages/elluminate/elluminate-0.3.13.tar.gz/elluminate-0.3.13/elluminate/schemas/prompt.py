from datetime import datetime
from typing import List

from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel

from elluminate.schemas.prompt_template import PromptTemplate
from elluminate.schemas.template_variables import TemplateVariables
from elluminate.utils import deprecated


class Prompt(BaseModel):
    """New prompt model."""

    id: int
    prompt_template: PromptTemplate
    template_variables: TemplateVariables
    messages: List[ChatCompletionMessageParam] = []
    created_at: datetime

    @property
    @deprecated(
        since="0.3.9",
        removal_version="0.4.0",
        alternative="messages property to access chat messages",
    )
    def prompt_str(self) -> str:
        """Return the prompt string."""
        if len(self.messages) == 1:
            return self.messages[0]["content"]
        elif len(self.messages) > 1:
            return "\n\n".join(f"[{msg['role']}]: {msg['content']}" for msg in self.messages)
        else:
            raise ValueError("No messages found in prompt template / error in conversion")
