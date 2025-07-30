from typing import Literal, Union
from genotype import Model


class Log(Model):
    """Log type."""

    level: Union[Literal["info"], Literal["error"]]
    """Log level."""
    content: str
    """Log content."""
    time: int
    """Unix timestamp in milliseconds."""
