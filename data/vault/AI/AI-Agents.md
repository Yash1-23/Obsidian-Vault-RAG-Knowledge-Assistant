# AI Agents

## Overview

An AI agent is a software system that uses an LLM together with tools and actions to accomplish a goal.

Unlike a simple chatbot, an agent can decide what actions are required to complete a task.

## Basic Agent Loop

A typical agent follows this process:

1. Understand the user's request
2. Determine the required action
3. Select an appropriate tool
4. Execute the tool
5. Observe the result
6. Decide whether another action is required
7. Generate the final response

## Tools

Agents can use external tools such as:

- Search engines
- Databases
- APIs
- Calculators
- File systems
- Vector databases
- Code execution environments

Tools allow an LLM to interact with information and systems outside its own knowledge.

## Function Calling

Function calling allows an LLM to request that a specific function or tool be executed.

For example, an agent could decide:

User asks for an order status.

Agent → call get_order_status()

Tool → returns order information.

Agent → explains the result to the user.

## Planning

Some agents break complex tasks into smaller steps.

For example:

Research question

→ Search documents

→ Retrieve relevant information

→ Compare information

→ Summarize findings

→ Produce final answer

## Memory

Agents can use memory to maintain information across interactions.

Types of memory can include:

- Conversation history
- User preferences
- Retrieved knowledge
- Task state

## Multi-Agent Systems

A multi-agent system contains multiple specialized agents.

For example:

Research Agent → gathers information

Analysis Agent → analyzes information

Writing Agent → produces the final report

A coordinator can determine which agent should handle each task.

## Agentic RAG

Agentic RAG combines retrieval with agent-based decision making.

Instead of always performing the same retrieval process, an agent can decide:

- Whether retrieval is needed
- Which knowledge source to search
- Whether another search is necessary
- Whether the retrieved information is sufficient
- When to provide the final answer

## Risks

Agentic systems can fail because of:

- Incorrect tool selection
- Poor planning
- Hallucinated tool arguments
- Infinite loops
- Incorrect retrieved information
- Excessive API calls

Therefore, agents should have clear tool definitions, validation, limits, and fallback mechanisms.