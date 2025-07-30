from genotype import Model


class VarV1(Model):
    """Variable type. It defines meta information about the variable."""

    id: str
    """Unique variable identifier. Used to identify the changes in the payload."""
    name: str
    """Variable name unique to the context. Used to access the variable from the client."""
    description: str
    """Variable description. Used as the documentation."""
