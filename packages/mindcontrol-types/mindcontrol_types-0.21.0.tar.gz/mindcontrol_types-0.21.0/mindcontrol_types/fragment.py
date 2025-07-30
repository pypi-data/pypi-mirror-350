from .var import VarV1
from .signature import SignatureInputFieldsV1
from genotype import Model


class FragmentV1(Model):
    """Prompt fragment. Represents an individual prompt snippets with variables
    that can be used independently or compiled together."""

    var: VarV1
    """Fragment variable"""
    signature: SignatureInputFieldsV1
    """Fragment signature."""
    content: str
    """Fragment content."""
