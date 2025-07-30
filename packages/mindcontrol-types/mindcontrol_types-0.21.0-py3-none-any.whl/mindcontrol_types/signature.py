from .var import VarV1
from genotype_json_types import GtjAny
from genotype import Model
from typing import List, Literal, Union, Any


SignatureInputV1Type = Union[Literal["string"], Literal["number"]]


class SignatureInputV1(Model):
    """Input schema. It defines individual input variable and type."""

    type: SignatureInputV1Type
    """Input type."""
    var: VarV1
    """Input variable."""


class SignatureInputFieldsV1(Model):
    input: List[SignatureInputV1]
    """Input definition."""


class SignatureOutputBaseV1(Model):
    """Output base type."""

    var: VarV1
    """Output variable."""


class SignatureOutputStringV1(SignatureOutputBaseV1, Model):
    """Output string type."""

    type: Literal["string"]
    """Output type."""


class SignatureOutputJsonV1(SignatureOutputBaseV1, Model):
    """Output JSON type."""

    type: Literal["json"]
    """Output type."""
    descriptor: Any
    """JSON schema descriptor."""


SignatureOutputV1 = Union[SignatureOutputStringV1, SignatureOutputJsonV1]
"""Output type. It defines output variable and type."""


class SignatureV1(SignatureInputFieldsV1, Model):
    """Prompt signature. It defines the input and output types of the prompt."""

    output: SignatureOutputV1
    """Output definition."""
    n: int
    """The number of choices to generate."""
