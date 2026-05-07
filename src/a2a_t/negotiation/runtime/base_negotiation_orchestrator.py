from __future__ import annotations

from a2a_t.negotiation.common.enums import NegotiationRole
from a2a_t.negotiation.common.models import ContinueNegotiationInput, StartNegotiationInput


class BaseNegotiationOrchestrator:
    """Expose the shared negotiation handler behind a role-specific facade."""

    def __init__(self, *, handler, role: NegotiationRole) -> None:
        self._handler = handler
        self._role = role

    def start_negotiation(self, input: StartNegotiationInput) -> dict[str, object]:
        """Start a negotiation from the bound local role."""
        return self._handler.start(input=input, role=self._role)

    def receive_negotiation(self, message: str, context: dict[str, object]) -> dict[str, object]:
        """Process a negotiation message received from the remote peer."""
        return self._handler.receive(
            message=message,
            context=context,
        )

    def continue_negotiation(self, input: ContinueNegotiationInput) -> dict[str, object]:
        """Continue a negotiation from the bound local role."""
        return self._handler.continue_(input=input)
