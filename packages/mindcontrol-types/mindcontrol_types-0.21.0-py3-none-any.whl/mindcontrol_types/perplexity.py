from typing import Literal, Union, Optional, Dict
from genotype import Model


PerplexityModel = Union[Literal["sonar-pro"], Literal["sonar"], Literal["sonar-deep-research"], Literal["sonar-reasoning-pro"], Literal["sonar-reasoning"], Literal["r1-1776"], str]
"""Perplexity model identifier.
Source: https://docs.perplexity.ai/models/model-cards"""


class PerplexitySettings(Model):
    """Perplexity model settings."""

    type: Literal["perplexity"]
    """Settings type."""
    model: Optional[PerplexityModel] = None
    """Model identifier."""


PerplexityProvider = Literal["perplexity"]
"""Perplexity provider identifier."""


class PerplexityProviderSettings(Model):
    """Perplexity provider settings."""

    default: Optional[PerplexityProvider] = None
    models: Optional[Dict[str, PerplexityProvider]] = None
