from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

CHROMA_DB_PATH = os.getenv(
    "CHROMA_DB_PATH",
    "./chroma_db"
)

RETRIEVAL_THRESHOLD = float(
    os.getenv(
        "RETRIEVAL_THRESHOLD",
        "0.75"
    )
)