import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

# ---------------------------------------------------------
# INIT VECTOR STORE
# ---------------------------------------------------------

def init_vector_store(messages):
    client = chromadb.Client()

    # Use Chroma's built-in lightweight embedding model
    embedding_fn = DefaultEmbeddingFunction()

    # Create collection
    collection = client.create_collection(
        name="aurora_messages",
        metadata={"hnsw:space": "cosine"},
        embedding_function=embedding_fn
    )

    # Prepare the documents
    docs = [m["text"] for m in messages]
    ids = [str(m["id"]) for m in messages]

    # Add to vector store
    collection.add(
        ids=ids,
        documents=docs
    )

    return client, collection


# ---------------------------------------------------------
# SEMANTIC SEARCH
# ---------------------------------------------------------

def search_similar_messages(collection, query: str, top_k: int = 3):

    result = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "distances"]
    )

    output = []
    for doc, dist in zip(result["documents"][0], result["distances"][0]):
        output.append({
            "text": doc,
            "score": 1 - dist
        })

    return output
