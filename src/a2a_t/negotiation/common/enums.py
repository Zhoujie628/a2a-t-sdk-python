from __future__ import annotations

from enum import Enum


class NegotiationType(str, Enum):
    """Enumerate the negotiation flows supported by the SDK."""

    INFORMATION = "information"
    CLARIFICATION = "clarification"
    FEASIBILITY = "feasibility"
    FULFILLMENT = "fulfillment"


class NegotiationRole(str, Enum):
    """Describe which side owns the current negotiation state."""

    CLIENT = "client"
    SERVER = "server"


class NegotiationStatus(str, Enum):
    """Describe the lifecycle state of a negotiation round."""

    IN_PROGRESS = "in-progress"
    AGREED = "agreed"
    REJECTED = "rejected"
