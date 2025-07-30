from typing import Literal, Union, Optional, Dict
from genotype import Model


OpenAIModelV1 = Union[Literal["gpt-4o"], Literal["gpt-4o-2024-11-20"], Literal["gpt-4o-2024-08-06"], Literal["gpt-4o-2024-05-13"], Literal["chatgpt-4o-latest"], Literal["gpt-4o-mini"], Literal["gpt-4o-mini-2024-07-18"], Literal["o1"], Literal["o1-2024-12-17"], Literal["o1-mini"], Literal["o1-mini-2024-09-12"], Literal["o1-preview"], Literal["o1-preview-2024-09-12"], Literal["o3-mini"], Literal["o3-mini-2025-01-31"], Literal["gpt-4-turbo"], Literal["gpt-4-turbo-2024-04-09"], Literal["gpt-4-turbo-preview"], Literal["gpt-4-0125-preview"], Literal["gpt-4-1106-preview"], Literal["gpt-4"], Literal["gpt-4-0613"], Literal["gpt-4-0314"], Literal["gpt-3.5-turbo"], Literal["gpt-3.5-turbo-0125"], Literal["gpt-3.5-turbo-1106"], str]
"""OpenAI model identifier."""


class OpenAISettingsV1(Model):
    """OpenAI model settings."""

    type: Literal["openai"]
    """Settings type."""
    model: Optional[OpenAIModelV1] = None
    """Model identifier."""


OpenAIProvider = Union[Literal["openai"], Literal["azure"]]
"""OpenAI provider enum."""


class OpenAIProviderSettingsV1(Model):
    """OpenAI provider settings."""

    default: Optional[OpenAIProvider] = None
    models: Optional[Dict[str, OpenAIProvider]] = None
