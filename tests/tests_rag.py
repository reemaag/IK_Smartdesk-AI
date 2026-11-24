from app.agents.rag_agent import (
    rag_agent
)


def test_password_query():

    result = rag_agent.answer(
        "How do I reset my password?"
    )

    assert result["escalate"] is False


def test_vpn_query():

    result = rag_agent.answer(
        "How do I connect to VPN?"
    )

    assert result["escalate"] is False


def test_unknown_query():

    result = rag_agent.answer(
        "My monitor is flickering badly"
    )

    assert result["escalate"] is True