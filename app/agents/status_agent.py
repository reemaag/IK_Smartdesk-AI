from app.jira.status import (
    get_tickets
)


class StatusAgent:

    def get_status(
        self,
        email: str
    ):

        tickets = get_tickets(
            email
        )

        if not tickets:

            return (
                "No tickets found "
                "for this email."
            )

        response = []

        for ticket in tickets:

            response.append(
                f"""
Ticket ID:
{ticket['id']}

Summary:
{ticket['summary']}

Priority:
{ticket['priority']}

Status:
{ticket['status']}
"""
            )

        return "\n".join(
            response
        )


status_agent = StatusAgent()    