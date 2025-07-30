from typing import Literal, Union, Optional, Dict
from genotype import Model


AnthropicModelV1 = Union[Literal["claude-3-5-sonnet"], Literal["claude-3-opus"], Literal["claude-3-sonnet"], Literal["claude-3-haiku"], str]
"""Anthropic model identifier."""


class AnthropicSettingsV1(Model):
    """Anthropic model settings."""

    type: Literal["anthropic"]
    """Settings type."""
    model: Optional[AnthropicModelV1] = None
    """Model identifier."""


AnthropicProvider = Union[Literal["aws"], Literal["anthropic"], Literal["gcp"]]
"""Anthropic providers."""


class AnthropicProviderSettingsV1(Model):
    """Anthropic provider settings."""

    default: Optional[AnthropicProvider] = None
    models: Optional[Dict[str, AnthropicProvider]] = None
