from .prompt import PromptV1
from .var import VarV1
from .signature import SignatureV1
from .llm import LlmSettingsV1
from .fragment import FragmentV1
from typing import Union, Literal, List, Optional, Any
from typing_extensions import Annotated
from pydantic import Field
from genotype import Model


class ResourceChainV1(Model):
    """Prompt chain resource. Represents a chain of prompts."""

    type: Literal["chain"]
    """Resource type."""
    var: VarV1
    """Chain variable"""
    signature: SignatureV1
    """Chain signature."""
    chain: List[PromptV1]
    """Prompts chain."""
    system: Optional[str] = None
    """Default system model instructions. Applied to each prompt in the chain unless specified."""
    settings: Optional[LlmSettingsV1] = None
    """Default settings. Applied to each prompt in the chain unless specified."""


class ResourceDataV1(Model):
    """Data resource. Represents free-form data."""

    type: Literal["data"]
    """Resource type."""
    var: VarV1
    """Data variable."""
    data: Any
    """Data."""


class ResourcePromptV1(Model):
    """Prompt resource. Represents a prompt template."""

    type: Literal["prompt"]
    """Resource type."""
    var: VarV1
    """Prompt variable."""
    signature: SignatureV1
    """Prompt signature."""
    prompt: PromptV1
    """Prompt."""


class ResourceSettingsV1(Model):
    """AI model settings resource."""

    type: Literal["settings"]
    """Resource type."""
    var: VarV1
    """Settings variable."""
    settings: LlmSettingsV1
    """Settings object."""


class ResourceFragmentsV1(Model):
    """Fragments resource."""

    type: Literal["fragments"]
    """Fragments type."""
    var: VarV1
    """Fragments variable."""
    fragments: List[FragmentV1]
    """Fragments array."""


ResourceV1 = Annotated[Union[ResourcePromptV1, ResourceChainV1, ResourceDataV1, ResourceSettingsV1, ResourceFragmentsV1], Field(json_schema_extra={'discriminator': 'type'})]
