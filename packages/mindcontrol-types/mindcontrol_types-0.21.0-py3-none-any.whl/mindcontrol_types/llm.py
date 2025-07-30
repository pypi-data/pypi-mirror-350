from .anthropic import AnthropicSettingsV1, AnthropicProvider
from .openai import OpenAISettingsV1, OpenAIProvider
from .perplexity import PerplexitySettings, PerplexityProvider
from typing import Union, Optional
from typing_extensions import Annotated
from pydantic import Field
from genotype import Model


LlmProvider = Union[AnthropicProvider, OpenAIProvider, PerplexityProvider]


class SettingsNope(Model):
    """Fallback for when no settings are provided. It is needed to fallback for
    older payloads with empty settings object."""

    type: Optional[None] = None
    model: Optional[None] = None


LlmSettingsV1 = Annotated[Union[SettingsNope, AnthropicSettingsV1, OpenAISettingsV1, PerplexitySettings], Field(json_schema_extra={'discriminator': 'type'})]
