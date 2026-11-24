import json

from pathlib import Path

from langchain.schema import (
    Document
)

from langchain_openai import (
    OpenAIEmbeddings
)

from langchain_community.vectorstores import (
    Chroma
)

from app.config import (
    CHROMA_DB_PATH
)


KB_FOLDER = Path(
    "knowledge_base"
)


def load_documents():

    documents = []

    for file_path in (
        KB_FOLDER.glob("*.json")
    ):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        for row in data:

            content = f"""
Category:
{row.get('category', '')}

Question:
{row['question']}

Answer:
{row['answer']}
"""

            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "source":
                        file_path.name
                    }
                )
            )

    return documents


def build_index():

    documents = load_documents()

    embeddings = (
        OpenAIEmbeddings()
    )

    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=
        CHROMA_DB_PATH
    )

    db.persist()

    print(
        f"Indexed "
        f"{len(documents)} documents"
    )


if __name__ == "__main__":

    build_index()