ROUTER_PROMPT = """
Classify the user query.

Categories:

knowledge

ticket_status

ticket_creation

greeting

Return ONLY one category.

Examples:

How do I reset password?
knowledge

What is my ticket status?
ticket_status

Create a ticket
ticket_creation

Hello
greeting
"""