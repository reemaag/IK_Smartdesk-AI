from langchain_openai import ChatOpenAI

from app.prompts.router_prompt import (
    ROUTER_PROMPT
)

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)


class RouterAgent:

    def detect_intent(
        self,
        query: str
    ) -> str:

        prompt = f"""
{ROUTER_PROMPT}

Query:
{query}
"""

        response = llm.invoke(
            prompt
        )

        return (
            response.content
            .strip()
            .lower()
        )


router_agent = RouterAgent()