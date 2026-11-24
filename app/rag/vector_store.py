from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from app.config import (
    CHROMA_DB_PATH
)


class VectorStoreManager:

    def __init__(self):

        self.embeddings = OpenAIEmbeddings()

        self.db = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=self.embeddings
        )

    def get_retriever(
        self,
        k: int = 5
    ):

        return self.db.as_retriever(
            search_kwargs={"k": k}
        )

    def similarity_search(
        self,
        query: str,
        k: int = 5
    ):

        return self.db.similarity_search(
            query,
            k=k
        )

    def similarity_search_with_scores(
        self,
        query: str,
        k: int = 5
    ):

        return self.db.similarity_search_with_score(
            query,
            k=k
        )


vector_store = VectorStoreManager()