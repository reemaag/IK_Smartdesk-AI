from app.jira.db import (
    get_connection
)


def get_tickets(
    email
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *

    FROM tickets

    WHERE email=?

    ORDER BY created_at DESC
    """,
    (email,)
    )

    rows = cursor.fetchall()

    conn.close()

    results = []

    for row in rows:

        results.append({

            "id":
            row["id"],

            "summary":
            row["summary"],

            "description":
            row["description"],

            "priority":
            row["priority"],

            "status":
            row["status"],

            "category":
            row["category"]
        })

    return results
