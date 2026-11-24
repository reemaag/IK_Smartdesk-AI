# app/jira/admin.py

from app.jira.db import (
    get_connection
)


def update_ticket_status(
    ticket_id,
    status
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tickets

    SET status=?

    WHERE id=?
    """,
    (
        status,
        ticket_id
    )
    )

    conn.commit()

    conn.close()