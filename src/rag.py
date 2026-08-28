
import os
from typing import Callable,Optional

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


# --------------------------------------------------
# Load embedding model once
# --------------------------------------------------

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


# --------------------------------------------------
# Retrieve documents
# --------------------------------------------------

def retrieve_documents(query, top_k=3):

    chroma_client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = chroma_client.get_collection(
        name=COLLECTION_NAME
    )

    query_embedding = embedding_model.encode(
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


# --------------------------------------------------
# Evaluate retrieved context
# --------------------------------------------------

def evaluate_context(question, documents,distances):

    context = "\n\n---\n\n".join(documents)

    evaluation_prompt = f"""
You are a strict knowledge-base evidence evaluator.

Your job is to determine whether the retrieved documents
contain enough explicit information to answer the user's
question.

IMPORTANT RULES:

1. The answer must be supported directly by the retrieved
   knowledge.
2. Information that is merely related to the question is
   NOT sufficient.
3. Do NOT use your general knowledge.
4. Do NOT assume missing facts.
5. If the retrieved documents only mention a related topic
   but do not provide enough information to answer the
   actual question, return INSUFFICIENT.
6. Only return SUFFICIENT when the retrieved knowledge
   contains enough evidence to construct a factual answer.

User question:
{question}

Retrieved knowledge:
{context}

Return ONLY one word:

SUFFICIENT

or

INSUFFICIENT
"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict evidence evaluator. "
                    "Never treat related information as sufficient."
                )
            },
            {
                "role": "user",
                "content": evaluation_prompt
            }
        ],
        temperature=0
    )

    decision = (
        response.choices[0]
        .message.content
        .strip()
        .upper()
    )

    if decision == "SUFFICIENT":
        return "SUFFICIENT"

    return "INSUFFICIENT"





# --------------------------------------------------
# Refine search query
# --------------------------------------------------

def refine_query(question):

    prompt = f"""
You are a search query optimization agent.

Rewrite the user's question into a concise search
query that will improve retrieval from a technical
knowledge base.

Preserve the original meaning.

Return ONLY the rewritten search query.

Original question:
{question}
"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return (
        response.choices[0]
        .message.content
        .strip()
    )


# --------------------------------------------------
# Generate grounded answer
# --------------------------------------------------

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


# --------------------------------------------------
# Agent
# --------------------------------------------------
# --------------------------------------------------
# Agent
# --------------------------------------------------

def agent_answer(
    question,
    status_callback: Optional[Callable[[str], None]] = None
):

    agent_steps = []

    def update_status(message):

        print(message)
        agent_steps.append(message)

        if status_callback:
            status_callback(message)

    update_status("\nAgent started")
    update_status(
        f"Original question: {question}"
    )

    # ----------------------------------------------
    # Step 1: Initial retrieval
    # ----------------------------------------------

    documents, metadatas, distances = retrieve_documents(
        question,
        top_k=3
    )

    update_status(
        "Initial retrieval completed"
    )

    print("\nRetrieved sources:")

    for metadata, distance in zip(
        metadatas,
        distances
    ):

        print(
            f"- {metadata['source']} "
            f"(chunk {metadata['chunk_id']}, "
            f"distance={distance:.4f})"
        )

    decision = evaluate_context(
        question,
        documents,
        distances
    )

    update_status(
        f"Initial evidence evaluation: {decision}"
    )

    # ----------------------------------------------
    # Step 2: Adaptive retrieval
    # ----------------------------------------------

    if decision == "INSUFFICIENT":

        update_status(
            "Evidence insufficient — refining search query..."
        )

        refined_query = refine_query(
            question
        )

        update_status(
            f"Refined query: {refined_query}"
        )

        documents, metadatas, distances = retrieve_documents(
            refined_query,
            top_k=5
        )

        update_status(
            "Second retrieval completed"
        )

        decision = evaluate_context(
            question,
            documents,
            distances
        )

        update_status(
            f"Second evidence evaluation: {decision}"
        )

    # ----------------------------------------------
    # Step 3: Reject unsupported question
    # ----------------------------------------------

    if decision == "INSUFFICIENT":

        update_status(
            "Knowledge base does not contain "
            "sufficient evidence."
        )

        return (
            "I couldn't find enough information "
            "in the knowledge base.",
            metadatas,
            documents,
            distances,
            agent_steps
        )

    # ----------------------------------------------
    # Step 4: Generate grounded answer
    # ----------------------------------------------

    update_status(
        "Evidence sufficient — generating "
        "grounded answer..."
    )

    answer = generate_answer(
        question,
        documents,
        metadatas
    )

    update_status(
        "Grounded answer generated successfully"
    )

    return (
        answer,
        metadatas,
        documents,
        distances,
        agent_steps
    )



# --------------------------------------------------
# CLI testing
# --------------------------------------------------

if __name__ == "__main__":

    question = input(
        "\nAsk a question: "
    )

    answer, metadatas, documents, distances,agent_steps = agent_answer(
        question
    )

    print("\n" + "=" * 60)
    print("AI ANSWER")
    print("=" * 60)

    print(answer)

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    shown_sources = set()

    for metadata in metadatas:

        source = metadata["source"]

        if source not in shown_sources:

            print(
                f"- {source} "
                f"(chunk {metadata['chunk_id']})"
            )

            shown_sources.add(source)

