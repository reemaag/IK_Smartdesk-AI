from app.jira.create_ticket import (
    create_ticket
)

create_ticket(
    summary="VPN Issue",
    description=
    "Unable to connect from home",
    email=
    "john@company.com",
    category="IT"
)

create_ticket(
    summary="Leave Approval",
    description=
    "Leave request not approved",
    email=
    "john@company.com",
    category="HR"
)

print(
    "Mock tickets created"
)