from app.rag.vector_store import (
    vector_store
)

from app.config import (
    RETRIEVAL_THRESHOLD
)


class RetrieverService:

    def __init__(self):

        self.retriever = (
            vector_store.get_retriever()
        )

    def retrieve(
        self,
        question: str
    ):

        return self.retriever.invoke(
            question
        )

    def retrieve_with_confidence(
        self,
        question: str
    ):

        results = (
            vector_store
            .similarity_search_with_scores(
                question,
                k=3
            )
        )

        if not results:

            return {
                "documents": [],
                "confidence": 0.0,
                "escalate": True
            }

        docs = []

        scores = []

        for doc, score in results:

            docs.append(doc)

            # Convert distance to confidence score
            confidence = max(
                0.0,
                1 - score
            )

            scores.append(confidence)

        top_confidence = max(scores)

        return {
            "documents": docs,
            "confidence": top_confidence,
            "escalate":
                top_confidence <
                RETRIEVAL_THRESHOLD
        }


retriever_service = RetrieverService()
