from dataclasses import (
    dataclass,
    field
)

from datetime import (
    datetime
)

from typing import (
    Optional,
    List,
    Dict
)


@dataclass
class SessionState:

    session_id: str

    email: Optional[str] = None

    pending_ticket: Optional[
        Dict
    ] = None

    awaiting_confirmation: bool = False

    last_ticket_id: Optional[
        str
    ] = None

    last_query: Optional[
        str
    ] = None

    current_topic: Optional[
        str
    ] = None

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    last_accessed: datetime = field(
        default_factory=datetime.utcnow
    )

    conversation_history: List[
        Dict
    ] = field(
        default_factory=list
    )

    selected_ticket_id: Optional[
        str
    ] = None

    escalation_count: int = 0