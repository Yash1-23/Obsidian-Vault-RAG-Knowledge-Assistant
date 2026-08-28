import os

import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from groq import Groq


load_dotenv()


CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "obsidian_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def retrieve_documents(query, top_k=3):

    model = SentenceTransformer(EMBEDDING_MODEL)

    chroma_client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = chroma_client.get_collection(
        name=COLLECTION_NAME
    )

    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    return documents, metadatas, distances


def evaluate_context(question, documents):

    context = "\n\n---\n\n".join(documents)

    evaluation_prompt = f"""
You are evaluating whether a knowledge base contains
enough information to answer a user's question.

User question:
{question}

Retrieved knowledge:
{context}

Determine whether the retrieved knowledge contains
enough information to answer the question.

Return ONLY one word:

SUFFICIENT

or

INSUFFICIENT
"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": evaluation_prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip().upper()


def generate_answer(question, documents, metadatas):

    context_parts = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        context_parts.append(
            f"Source: {metadata['source']}\n"
            f"{document}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are an AI knowledge assistant.

Answer the user's question using ONLY the
provided knowledge base context.

Do not invent information.

If the information is not available,
say that you could not find enough
information in the knowledge base.

Knowledge Base Context:

{context}

User Question:

{question}

Provide a concise and accurate answer.
"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a grounded knowledge assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


def agent_answer(question):

    documents, metadatas, distances = retrieve_documents(
        question
    )

    decision = evaluate_context(
        question,
        documents
    )

    print(f"\nAgent decision: {decision}")

    if decision == "INSUFFICIENT":

        return (
            "I couldn't find enough information "
            "in the knowledge base.",
            metadatas,
            documents,
            distances
        )

    answer = generate_answer(
        question,
        documents,
        metadatas
    )

    return (
        answer,
        metadatas,
        documents,
        distances
    )


if __name__ == "__main__":

    question = input("\nAsk a question: ")

    answer, metadatas, documents, distances = agent_answer(
        question
    )

    print("\n" + "=" * 60)
    print("AI ANSWER")
    print("=" * 60)

    print(answer)

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    for metadata in metadatas:
        print(
            f"- {metadata['source']} "
            f"(chunk {metadata['chunk_id']})"
        )