import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "obsidian_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def search_knowledge_base(query, top_k=3):

    print("Loading embedding model...")

    model = SentenceTransformer(EMBEDDING_MODEL)

    print("Connecting to ChromaDB...")

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    # Convert the user's question into an embedding
    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    ).tolist()

    # Chroma expects a list containing the embedding
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    question = input("\nAsk a question: ")

    results = search_knowledge_base(question)

    print("\n" + "=" * 60)
    print("RETRIEVED KNOWLEDGE")
    print("=" * 60)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1
    ):
        print(f"\nResult {i}")
        print("-" * 60)
        print(f"Source: {metadata['source']}")
        print(f"Chunk: {metadata['chunk_id']}")
        print(f"Distance: {distance:.4f}")
        print("\nContent:")
        print(document)