# Retrieval-Augmented Generation (RAG)

## Overview

Retrieval-Augmented Generation, commonly called RAG, is an architecture that combines information retrieval with a Large Language Model (LLM).

Instead of asking an LLM to answer a question only from its pretrained knowledge, a RAG system first retrieves relevant information from an external knowledge base. The retrieved information is then provided to the LLM as context.

This helps the system produce answers that are more relevant to a specific knowledge base.

## RAG Pipeline

A typical RAG pipeline contains these stages:

1. Document ingestion
2. Document preprocessing
3. Document chunking
4. Embedding generation
5. Vector database storage
6. Query embedding
7. Similarity search
8. Context retrieval
9. Prompt construction
10. LLM response generation

## Document Ingestion

Documents can come from many sources including:

- Markdown files
- PDF documents
- Websites
- Word documents
- Databases
- Internal company documentation

The first step is to load these documents into the RAG pipeline.

## Chunking

Large documents are divided into smaller pieces called chunks.

Chunking is important because sending an entire large document to an LLM can be inefficient and may exceed the model's context window.

A common strategy is to use chunks of approximately 500–1000 tokens with some overlap between chunks.

Overlap helps preserve context between neighboring chunks.

## Embeddings

An embedding converts text into a numerical vector representation.

Texts with similar meanings generally have embeddings that are close together in vector space.

For example:

"How does retrieval augmented generation work?"

and

"Explain the process used by a RAG system."

should have relatively similar embeddings.

## Vector Database

Embeddings are stored in a vector database.

Common vector databases include:

- Chroma
- FAISS
- Pinecone
- Weaviate
- Milvus

The vector database allows the application to perform similarity searches efficiently.

## Retrieval

When a user asks a question, the question is converted into an embedding.

The system compares the query embedding against document embeddings and retrieves the most relevant chunks.

The number of retrieved documents is often called Top-K.

For example:

Top-K = 5 means the system retrieves the five most relevant chunks.

## Generation

The retrieved chunks are inserted into the prompt given to the LLM.

The LLM uses the retrieved context to generate the final response.

A simplified process is:

User Question → Retrieval → Relevant Context → LLM → Answer

## Advantages

RAG provides several benefits:

- Uses domain-specific information
- Can work with private documents
- Reduces reliance on model memory
- Knowledge can be updated without retraining the LLM
- Can provide source references
- Can improve factual grounding

## Limitations

RAG does not automatically guarantee correct answers.

Common problems include:

- Poor document chunking
- Incorrect retrieval
- Missing information
- Irrelevant context
- Outdated documents
- Hallucination by the LLM

Therefore, retrieval quality and evaluation are important.

## Evaluation

RAG systems can be evaluated using metrics such as:

- Retrieval precision
- Retrieval recall
- Hit Rate
- Mean Reciprocal Rank
- Answer relevance
- Faithfulness

A good RAG system should retrieve relevant information and generate answers that are supported by that information.