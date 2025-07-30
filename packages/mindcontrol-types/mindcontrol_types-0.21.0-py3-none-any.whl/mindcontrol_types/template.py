from .var import VarV1
from .signature import SignatureInputFieldsV1
from genotype import Model


class TemplateV1(Model):
    """Template. Represents an individual prompt with variables that can be used
    independently."""

    var: VarV1
    """Template variable"""
    signature: SignatureInputFieldsV1
    """Template signature."""
    content: str
    """Template."""
