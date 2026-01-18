from qdrant_store import get_client

def hybrid_search(query, model, top_k=5):
    client = get_client()
    qv = model.encode(query).tolist()

    results = client.search(
        collection_name="jira_docs",
        query_vector=qv,
        limit=top_k
    )

    return [
        {
            "text": r.payload["text"],
            "score": r.score
        }
        for r in results
    ]

def build_context(results, max_chunks=3):
    blocks = []
    for r in results[:max_chunks]:
        blocks.append(r["text"])
    return "\n\n".join(blocks)

def get_total_ticket_count():
    return "Qdrant"
