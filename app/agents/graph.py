from app.agents.router import (
    router_agent
)

from app.agents.rag_agent import (
    rag_agent
)

from app.agents.ticket_agent import (
    ticket_agent
)

from app.agents.status_agent import (
    status_agent
)

from app.memory.session_manager import (
    session_manager
)

from app.models.session import (
    SessionState
)


EMAIL_PROMPT = (
    "Please provide your company "
    "email address."
)


class AgentGraph:

    def _is_email(
        self,
        text: str
    ) -> bool:

        text = text.strip()

        return (
            "@" in text
            and "." in text
        )

    def _add_assistant_message(
        self,
        session_id: str,
        response: str
    ):

        session_manager.add_message(
            session_id=session_id,
            role="assistant",
            content=response
        )

    def _get_recent_context(
        self,
        session: SessionState,
        max_messages: int = 6
    ) -> str:

        history = (
            session.conversation_history[
                -max_messages:
            ]
        )

        if not history:
            return ""

        context_messages = []

        for msg in history:

            context_messages.append(
                f"{msg['role']}: "
                f"{msg['content']}"
            )

        return "\n".join(
            context_messages
        )

    def _handle_confirmation(
        self,
        session: SessionState,
        query: str
    ) -> str:

        confirmation_words = [
            "yes",
            "y",
            "confirm",
            "create",
            "proceed",
            "go ahead"
        ]

        if (
            query.strip().lower()
            in confirmation_words
        ):

            response = (
                ticket_agent.create(
                    session.pending_ticket
                )
            )

            session.pending_ticket = None

            session.awaiting_confirmation = False

            session_manager.update(
                session
            )

            return response

        session.pending_ticket = None

        session.awaiting_confirmation = False

        session_manager.update(
            session
        )

        return (
            "Ticket creation cancelled."
        )

    def _handle_ticket_creation(
        self,
        session: SessionState,
        query: str,
        conversation_context: str
    ) -> str:

        if session.email is None:

            session.last_query = query

            session_manager.update(
                session
            )

            return (
                "I'd be happy to create "
                "a support ticket.\n\n"
                f"{EMAIL_PROMPT}"
            )

        ticket_data = (
            ticket_agent.build_ticket(
                email=session.email,
                issue=query,
                conversation_context=
                conversation_context
            )
        )

        session.pending_ticket = (
            ticket_data
        )

        session.awaiting_confirmation = True

        session_manager.update(
            session
        )

        return (
            ticket_agent
            .build_confirmation(
                ticket_data
            )
        )

    def _handle_status(
        self,
        session: SessionState
    ) -> str:

        if not session.email:

            return (
                "Please provide your "
                "company email address "
                "to retrieve your "
                "ticket status."
            )

        return (
            status_agent.get_status(
                session.email
            )
        )

    def _handle_escalation(
        self,
        session: SessionState,
        query: str,
        rag_result: dict,
        conversation_context: str
    ) -> str:

        session.escalation_count += 1

        if session.email is None:

            session.last_query = query

            session_manager.update(
                session
            )

            return (
                f"{rag_result['answer']}\n\n"
                "Please provide your "
                "company email address "
                "and I will prepare "
                "a support ticket."
            )

        ticket_data = (
            ticket_agent.build_ticket(
                email=session.email,
                issue=query,
                conversation_context=
                conversation_context
            )
        )

        session.pending_ticket = (
            ticket_data
        )

        session.awaiting_confirmation = True

        session_manager.update(
            session
        )

        return (
            f"{rag_result['answer']}\n\n"
            f"{ticket_agent.build_confirmation(ticket_data)}"
        )

    def process_query(
        self,
        session_id: str,
        query: str
    ) -> str:

        session = (
            session_manager.get(
                session_id
            )
        )

        query = query.strip()

        # --------------------------------------------------
        # Save user message
        # --------------------------------------------------

        session_manager.add_message(
            session_id=session_id,
            role="user",
            content=query
        )

        # --------------------------------------------------
        # Email Capture Flow
        # --------------------------------------------------

        if (
            self._is_email(query)
            and session.email is None
        ):

            session.email = query

            session_manager.update(
                session
            )

            if session.last_query:

                previous_issue = (
                    session.last_query
                )

                conversation_context = (
                    self._get_recent_context(
                        session
                    )
                )

                ticket_data = (
                    ticket_agent
                    .build_ticket(
                        email=session.email,
                        issue=
                        previous_issue,
                        conversation_context=
                        conversation_context
                    )
                )

                session.pending_ticket = (
                    ticket_data
                )

                session.awaiting_confirmation = True

                session.last_query = None

                session_manager.update(
                    session
                )

                response = (
                    "Thank you.\n\n"
                    +
                    ticket_agent
                    .build_confirmation(
                        ticket_data
                    )
                )

                self._add_assistant_message(
                    session_id,
                    response
                )

                return response

            response = (
                "Email saved successfully."
            )

            self._add_assistant_message(
                session_id,
                response
            )

            return response

        # --------------------------------------------------
        # Human-In-The-Loop Confirmation
        # --------------------------------------------------

        if (
            session.awaiting_confirmation
        ):

            response = (
                self._handle_confirmation(
                    session,
                    query
                )
            )

            self._add_assistant_message(
                session_id,
                response
            )

            return response

        # --------------------------------------------------
        # Conversation Context
        # --------------------------------------------------

        conversation_context = (
            self._get_recent_context(
                session
            )
        )

        # --------------------------------------------------
        # Context-Aware Intent Detection
        # --------------------------------------------------

        intent = (
            router_agent.detect_intent(
                f"""
Conversation History:

{conversation_context}

Current Message:

{query}
"""
            )
        )

        # --------------------------------------------------
        # Greeting
        # --------------------------------------------------

        if intent == "greeting":

            response = (
                "Hello! I'm SmartDesk AI. "
                "How can I assist you today?"
            )

            self._add_assistant_message(
                session_id,
                response
            )

            return response

        # --------------------------------------------------
        # Status Lookup Flow
        # --------------------------------------------------

        if intent == "ticket_status":

            response = (
                self._handle_status(
                    session
                )
            )

            self._add_assistant_message(
                session_id,
                response
            )

            return response

        # --------------------------------------------------
        # Explicit Ticket Creation
        # --------------------------------------------------

        if (
            intent
            == "ticket_creation"
        ):

            response = (
                self
                ._handle_ticket_creation(
                    session=session,
                    query=query,
                    conversation_context=
                    conversation_context
                )
            )

            self._add_assistant_message(
                session_id,
                response
            )

            return response

        # --------------------------------------------------
        # Knowledge Base + RAG
        # --------------------------------------------------

        rag_result = (
            rag_agent.answer(
                question=query,
                history=
                conversation_context
            )
        )

        # --------------------------------------------------
        # Escalation Flow
        # --------------------------------------------------

        if rag_result[
            "escalate"
        ]:

            response = (
                self._handle_escalation(
                    session=session,
                    query=query,
                    rag_result=
                    rag_result,
                    conversation_context=
                    conversation_context
                )
            )

            self._add_assistant_message(
                session_id,
                response
            )

            return response

        # --------------------------------------------------
        # Normal RAG Response
        # --------------------------------------------------

        response = (
            rag_result["answer"]
        )

        self._add_assistant_message(
            session_id,
            response
        )

        return response


agent_graph = AgentGraph()