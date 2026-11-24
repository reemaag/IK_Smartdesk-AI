from app.agents.ticket_agent import (
    ticket_agent
)


def test_ticket_generation():

    ticket = (
        ticket_agent.build_ticket(
            email="john@company.com",
            issue="VPN not working"
        )
    )

    assert (
        ticket["email"]
        ==
        "john@company.com"
    )

    assert (
        len(ticket["summary"]) > 0
    )