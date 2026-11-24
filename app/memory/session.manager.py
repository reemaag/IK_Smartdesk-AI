from datetime import datetime
from typing import Dict

from app.models.session import SessionState


class SessionManager:

    SESSION_TIMEOUT_MINUTES = 60

    def __init__(self):

        self.sessions: Dict[
            str,
            SessionState
        ] = {}

    def create_session(
        self,
        session_id: str
    ) -> SessionState:

        session = SessionState(
            session_id=session_id
        )

        self.sessions[
            session_id
        ] = session

        return session

    def get(
        self,
        session_id: str
    ) -> SessionState:

        if (
            session_id
            not in self.sessions
        ):
            return self.create_session(
                session_id
            )

        session = self.sessions[
            session_id
        ]

        session.last_accessed = (
            datetime.utcnow()
        )

        return session

    def update(
        self,
        session: SessionState
    ):

        session.last_accessed = (
            datetime.utcnow()
        )

        self.sessions[
            session.session_id
        ] = session

    def delete(
        self,
        session_id: str
    ):

        self.sessions.pop(
            session_id,
            None
        )

    def exists(
        self,
        session_id: str
    ) -> bool:

        return (
            session_id
            in self.sessions
        )

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):

        session = self.get(
            session_id
        )

        session.conversation_history.append(
            {
                "role": role,
                "content": content,
                "timestamp":
                datetime.utcnow().isoformat()
            }
        )

        # keep last 50 messages

        if (
            len(
                session.conversation_history
            ) > 50
        ):
            session.conversation_history = (
                session.conversation_history[
                    -50:
                ]
            )

        self.update(session)

    def get_history(
        self,
        session_id: str
    ):

        session = self.get(
            session_id
        )

        return (
            session.conversation_history
        )

    def clear_history(
        self,
        session_id: str
    ):

        session = self.get(
            session_id
        )

        session.conversation_history = []

        self.update(session)

    def clean_expired_sessions(
        self
    ):

        now = datetime.utcnow()

        expired = []

        for (
            session_id,
            session
        ) in self.sessions.items():

            age_minutes = (
                now -
                session.last_accessed
            ).total_seconds() / 60

            if (
                age_minutes >
                self.SESSION_TIMEOUT_MINUTES
            ):
                expired.append(
                    session_id
                )

        for session_id in expired:

            self.delete(
                session_id
            )


session_manager = SessionManager()