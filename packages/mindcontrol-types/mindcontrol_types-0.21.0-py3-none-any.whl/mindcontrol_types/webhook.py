from typing import Literal, Any, Union
from .collection import CollectionV1
from genotype import Model


class WebhookCollectionV1(Model):
    """Collecton webhook body."""

    type: Literal["collection"]
    """Webhook type."""
    id: str
    """Collection id."""
    collection: CollectionV1
    """Collection."""


class WebhookPingV1(Model):
    """Ping webhook body."""

    type: Literal["ping"]
    """Webhook type."""
    id: str
    """Webhook id to ping"""


class WebhookPongV1(Model):
    """Webhook pong response."""

    ping: Literal["pong"]
    """Ping response message."""


class WebhookV1(Model):
    """Webhook body."""

    v: Any
    """Schema version"""
    id: str
    """Webhook id."""
    time: int
    """Webhook timestamp."""
    payload: Union[WebhookPingV1, WebhookCollectionV1]
    """Webhook payload."""
