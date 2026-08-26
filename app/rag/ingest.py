from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector

from app.core.config import get_settings

import glob

from dotenv import load_dotenv
load_dotenv()

DOCS_PATH = "app/rag/documents"
COLLECTION_NAME = "knowledge_base"

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")


def get_pg_connection_string() -> str:
    # langchain-postgres needs the "+psycopg" driver marker in the URL

    settings = get_settings()

    return settings.database_url.replace("postgresql://", "postgresql+psycopg://")


def ingest() -> None:

    docs = []

    for filepath in glob.glob(f"{DOCS_PATH}/*.md"):
        with open(filepath, "r", encoding="utf-8") as f:
            docs.append({"content" : f.read(), "source" : filepath})


    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )


    texts, metadatas = [], []

    for doc in docs:
        chunks = splitter.split_text(doc["content"])
        texts.extend(chunks)
        metadatas.extend([{"source" : doc["source"]}] * len(chunks) )

    print(f"Ingesting {len(texts)} chunks from {len(docs)} documents into pgvector...")


    # pre_delete_collection=True -- wipes and re-creates the collection each run,
    # so re-running ingest.py after editing docs doesn't create duplicate chunks

    PGVector.from_texts(
        texts=texts,
        metadatas=metadatas,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=get_pg_connection_string(),
        pre_delete_collection=True,
    )

    print("Done. Stored in Neon Postgres (pgvector), collection : ", COLLECTION_NAME)


if __name__ == "__main__":
    ingest()