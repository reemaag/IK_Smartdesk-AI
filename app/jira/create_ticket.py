import uuid

from app.jira.db import (
    get_connection
)


def create_ticket(
    summary,
    description,
    email,
    category="IT",
    priority="Medium"
):

    ticket_id = (
        f"{category}-"
        f"{str(uuid.uuid4())[:8]}"
    )

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tickets(
        id,
        email,
        summary,
        description,
        category,
        priority,
        status
    )

    VALUES(
        ?, ?, ?, ?, ?, ?, ?
    )
    """,
    (
        ticket_id,
        email,
        summary,
        description,
        category,
        priority,
        "Open"
    ))

    conn.commit()

    conn.close()

    return ticket_id