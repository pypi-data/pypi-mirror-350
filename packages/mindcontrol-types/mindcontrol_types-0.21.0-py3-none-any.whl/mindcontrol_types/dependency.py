from .anthropic import AnthropicProvider
from .openai import OpenAIProvider
from .perplexity import PerplexityProvider
from typing import Literal, Union
from genotype import Model


class DependencyProviderV1(Model):
    """Provider dependency. It defines a provider that is required for
    the collection to operate."""

    type: Literal["provider"]
    """Dependency type."""
    id: Union[OpenAIProvider, AnthropicProvider, PerplexityProvider]
    """Provider id."""


DependencyV1 = DependencyProviderV1
"""Payload dependency."""
