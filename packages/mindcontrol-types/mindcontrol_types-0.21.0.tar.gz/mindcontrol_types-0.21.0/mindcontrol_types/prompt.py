from typing import List, Optional, Literal, Union
from .llm import LlmSettingsV1
from genotype import Model


PromptMessageV1Role = Union[Literal["user"], Literal["assistant"]]


class PromptMessageV1(Model):
    """Prompt message."""

    role: PromptMessageV1Role
    """Message role."""
    content: str
    """Message content."""


class PromptV1(Model):
    """Prompt object."""

    messages: List[PromptMessageV1]
    """Prompt messages."""
    system: Optional[str] = None
    """System model instructions."""
    settings: Optional[LlmSettingsV1] = None
    """LLM settings."""
