from .dependency import DependencyV1
from .resource import ResourceV1
from typing import Literal, List, Optional
from genotype import Model
from .openai import OpenAIProviderSettingsV1
from .anthropic import AnthropicProviderSettingsV1
from .perplexity import PerplexityProviderSettings


class PayloadSettingsProviders(Model):
    """Payload settings providers."""

    openai: Optional[OpenAIProviderSettingsV1] = None
    """OpenAI provider settings."""
    anthropic: Optional[AnthropicProviderSettingsV1] = None
    """Anthropic provider settings."""
    perplexity: Optional[PerplexityProviderSettings] = None
    """Perplexity provider settings."""


class PayloadSettings(Model):
    """Payload settings."""

    providers: Optional[PayloadSettingsProviders] = None
    """Payload providers settings. Changing the provider settings does not
    trigger major version bump directly, but rather indirectly by affecting
    the payload dependencies. The payload dependencies should always include
    whatever providers are used in the payload settings."""


class PayloadV1(Model):
    """Collection payload."""

    v: Literal[1]
    """Schema version."""
    dependencies: List[DependencyV1]
    """Payload dependencies. They define various dependencies that affect
    the behavior and requirements of the collection, i.e. adding Azure
    provider that will require Azure credentials. Adding a dependency
    triggers the major version bump, while removing a dependency does not."""
    resources: List[ResourceV1]
    """Payload resources."""
    settings: Optional[PayloadSettings] = None
    """Payload settings. They define various settings that dictate the collection
    behavior, i.e. which provider to use for a specific model or model author."""
