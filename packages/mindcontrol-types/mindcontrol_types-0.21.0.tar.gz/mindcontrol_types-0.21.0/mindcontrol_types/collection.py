from typing import Literal, Optional, Union
from genotype import Model
from .payload import PayloadV1


class CollectionBase(Model):
    """Collection base type."""

    v: Literal[1]
    """Schema version."""
    time: int
    """Unix timestamp in milliseconds when the collection version was updated."""
    major: int
    """Major collection version number."""
    minor: int
    """Minor collection version number."""
    draft: bool
    """Signifies if the collection version is a draft."""


class CollectionV1(CollectionBase, Model):
    """Collection version."""

    payload: str
    """Collection payload JSON."""
    settings: Optional[str] = None
    """Collection settings JSON."""


class CollectionSettingsObj(Model):
    pass


CollectionSettings = Union[CollectionSettingsObj, None]
"""Collection settings object. Unused for now."""


class CollectionParsedV1(CollectionBase, Model):
    """Parsed collection version. Unlike regular collection, the payload property is a parsed JSON object."""

    payload: PayloadV1
    """Collection payload."""
    settings: CollectionSettings
    """Collection settings."""
