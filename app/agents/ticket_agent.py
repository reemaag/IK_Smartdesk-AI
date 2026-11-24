from langchain_openai import (
    ChatOpenAI
)

from app.jira.create_ticket import (
    create_ticket
)


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)


class TicketAgent:

    def classify_category(
        self,
        issue: str
    ) -> str:

        prompt = f"""
Classify this issue.

Possible categories:

IT
HR

Issue:

{issue}

Return ONLY:

IT

or

HR
"""

        response = llm.invoke(
            prompt
        )

        category = (
            response.content
            .strip()
            .upper()
        )

        if category not in [
            "IT",
            "HR"
        ]:
            category = "IT"

        return category

    def classify_priority(
        self,
        issue: str
    ) -> str:

        prompt = f"""
Determine ticket priority.

Allowed values:

Low
Medium
High
Critical

Issue:

{issue}

Return only one value.
"""

        response = llm.invoke(
            prompt
        )

        priority = (
            response.content
            .strip()
            .title()
        )

        valid_values = [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]

        if priority not in valid_values:
            priority = "Medium"

        return priority

    def build_ticket(
        self,
        email: str,
        issue: str,
        conversation_context: str = ""
    ) -> dict:

        category = (
            self.classify_category(
                issue
            )
        )

        priority = (
            self.classify_priority(
                issue
            )
        )

        description = f"""
Issue:
{issue}

Employee Email:
{email}

Conversation History:
{conversation_context}
"""

        return {

            "email":
            email,

            "summary":
            issue[:120],

            "description":
            description,

            "category":
            category,

            "priority":
            priority
        }

    def build_confirmation(
        self,
        ticket_data: dict
    ) -> str:

        return f"""
Please review the ticket below.

Email:
{ticket_data['email']}

Summary:
{ticket_data['summary']}

Category:
{ticket_data['category']}

Priority:
{ticket_data['priority']}

Description:
{ticket_data['description']}

Reply YES to create the ticket.
"""

    def create(
        self,
        ticket_data: dict
    ) -> str:

        try:

            ticket_id = (
                create_ticket(
                    summary=
                    ticket_data[
                        "summary"
                    ],

                    description=
                    ticket_data[
                        "description"
                    ],

                    email=
                    ticket_data[
                        "email"
                    ],

                    category=
                    ticket_data[
                        "category"
                    ]
                )
            )

            return f"""
✅ Ticket created successfully.

Ticket ID:
{ticket_id}

You can check its status anytime.
"""

        except Exception as e:

            return (
                "Sorry, I was unable "
                "to create the ticket.\n\n"
                f"Error: {str(e)}"
            )


ticket_agent = TicketAgent()