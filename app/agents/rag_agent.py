from typing import Dict

from langchain_openai import (
    ChatOpenAI
)

from app.rag.retriever import (
    retriever_service
)

from app.prompts.rag_prompt import (
    RAG_PROMPT
)


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)


class RAGAgent:

    def answer(
        self,
        question: str,
        history: str = ""
    ) -> Dict:

        retrieval_result = (
            retriever_service
            .retrieve_with_confidence(
                question
            )
        )

        confidence = (
            retrieval_result[
                "confidence"
            ]
        )

        escalate = (
            retrieval_result[
                "escalate"
            ]
        )

        documents = (
            retrieval_result[
                "documents"
            ]
        )

        if escalate:

            return {
                "answer": (
                    "I do not have enough "
                    "information to answer "
                    "this question.\n\n"
                    "Would you like me to "
                    "create a support ticket?"
                ),
                "confidence":
                confidence,
                "escalate":
                True
            }

        context = "\n\n".join(
            [
                doc.page_content
                for doc in documents
            ]
        )

        prompt = f"""
{RAG_PROMPT}

Conversation History:

{history}

Knowledge Base Context:

{context}

Current Question:

{question}
"""

        response = llm.invoke(
            prompt
        )

        return {

            "answer":
            response.content,

            "confidence":
            confidence,

            "escalate":
            False
        }


rag_agent = RAGAgent()