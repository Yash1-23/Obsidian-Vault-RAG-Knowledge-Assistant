# Large Language Models (LLMs)

## Overview

Large Language Models are deep learning models trained on large amounts of text data.

They can perform tasks such as:

- Question answering
- Summarization
- Text generation
- Classification
- Information extraction
- Translation
- Code generation
- Reasoning

Examples of modern LLM families include GPT, Claude, Gemini, and Llama.

## Tokens

LLMs process text as tokens rather than directly processing complete sentences.

A token can represent a complete word, part of a word, punctuation, or another text unit.

The number of tokens that can be processed in one request depends on the model's context window.

## Prompting

Prompt engineering involves designing instructions that guide an LLM toward a desired output.

A good prompt can contain:

- Role
- Task
- Context
- Constraints
- Examples
- Output format

For example:

You are an AI assistant.
Answer the user's question using only the provided context.
If the answer is not present, say that you do not have enough information.

## Temperature

Temperature controls the randomness of generated responses.

Lower temperature values generally produce more deterministic responses.

Higher temperature values can produce more diverse responses.

For factual knowledge assistants, a relatively low temperature is often preferred.

## Hallucination

Hallucination occurs when an LLM generates information that is unsupported, incorrect, or fabricated.

RAG can reduce hallucination by providing relevant external context, but it cannot completely eliminate hallucinations.

## LLM Applications

LLMs can be used to build:

- Chatbots
- AI assistants
- Document analysis systems
- Coding assistants
- Research assistants
- Customer support agents
- Content generation systems
- RAG applications
- AI agents

## LLM + RAG

An LLM can be combined with a retrieval system to create a domain-specific assistant.

The retrieval system provides relevant context and the LLM generates a natural-language response.

This architecture is useful when the knowledge changes frequently or belongs to a private organization.