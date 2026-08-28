from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from chunking import create_chunks
from ingestion import load_markdown_files


VAULT_PATH = Path("data/vault")
CHROMA_PATH = "data/chroma_db"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def build_vector_store():
    print("Loading Markdown files...")

    documents = load_markdown_files(VAULT_PATH)

    print(f"Loaded {len(documents)} documents.")

    print("Creating chunks...")

    chunks = create_chunks(documents)

    print(f"Created {len(chunks)} chunks.")

    print("Loading embedding model...")

    model = SentenceTransformer(EMBEDDING_MODEL)

    print("Creating embeddings...")

    texts = [chunk["content"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    print("Connecting to ChromaDB...")

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name="obsidian_knowledge"
    )

    # Remove previous data to prevent duplicate chunks
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    ids = [
        f"{chunk['source']}_{chunk['chunk_id']}"
        for chunk in chunks
    ]

    metadatas = [
        {
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print("\nVector database created successfully!")
    print(f"Stored {len(chunks)} chunks in ChromaDB.")


if __name__ == "__main__":
    build_vector_store()