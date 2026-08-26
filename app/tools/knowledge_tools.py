from langchain_postgres import PGVector
from app.rag.ingest import get_pg_connection_string, embeddings, COLLECTION_NAME


def search_knowledge_base_tool(query: str) -> list[dict]:
    """Search the knowledge base (FAQs, policies) for chunks relevant to the query.
    Returns an empty list if nothing relevant found -- not an error."""

    vector_store = PGVector(
        embeddings = embeddings,
        collection_name=COLLECTION_NAME,
        connection=get_pg_connection_string(),
    )

    results = vector_store.similarity_search( query=query, k=3 )

    return [{"Content" : doc.page_content, "source" : doc.metadata["source"]} for doc in results]