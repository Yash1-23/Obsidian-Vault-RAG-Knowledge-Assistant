# Obsidian AI Knowledge Assistant

An agentic Retrieval-Augmented Generation (RAG) application that allows users to ask questions about an Obsidian Markdown knowledge base.

Unlike a basic RAG chatbot that retrieves documents and immediately generates an answer, this system introduces an evidence evaluation and adaptive retrieval layer.

The agent first retrieves relevant knowledge and evaluates whether the retrieved context contains enough evidence to answer the question. If the evidence is insufficient, it automatically refines the search query and performs another retrieval attempt. If sufficient evidence still cannot be found, the system refuses to answer rather than generating an unsupported response.

The project focuses on **grounded generation, adaptive retrieval, and reducing hallucinations in knowledge-base question answering**.

---

## Key Features

* Obsidian Markdown knowledge-base ingestion
* Document preprocessing and chunking
* Semantic embeddings using Sentence Transformers
* Persistent ChromaDB vector store
* Semantic similarity retrieval
* LLM-based evidence evaluation
* Adaptive query refinement
* Second retrieval attempt when evidence is insufficient
* Grounded answer generation
* Source and chunk attribution
* Explicit refusal for unsupported questions
* Streamlit web interface
* LLM-as-a-Judge answer-quality evaluation

---

# Why This Is More Than a Basic RAG Application

A traditional RAG pipeline commonly follows:

```text
User Question
      ↓
Retrieve Documents
      ↓
Generate Answer
```

This project introduces an additional decision-making layer:

```text
User Question
      ↓
Initial Retrieval
      ↓
Evidence Evaluation
      ↓
   ┌───────────────┐
   │               │
SUFFICIENT     INSUFFICIENT
   │               │
   ↓               ↓
Generate       Refine Query
Answer             ↓
               Second Retrieval
                    ↓
              Evidence Evaluation
                    ↓
              ┌─────┴─────┐
              │           │
         SUFFICIENT   INSUFFICIENT
              │           │
              ↓           ↓
        Generate       Refuse to
         Answer          Answer
```

The system therefore does not assume that retrieving a related document automatically means there is enough evidence to answer the question.

---

# System Architecture

```text
                     Obsidian Vault
                           │
                           ▼
                   Markdown Documents
                           │
                           ▼
                       Chunking
                           │
                           ▼
                Sentence Transformer
                           │
                           ▼
                      Embeddings
                           │
                           ▼
                       ChromaDB
                           │
                           │
                    User Question
                           │
                           ▼
                   Query Embedding
                           │
                           ▼
                  Initial Retrieval
                           │
                           ▼
                Evidence Evaluation
                           │
              ┌────────────┴────────────┐
              │                         │
         SUFFICIENT                INSUFFICIENT
              │                         │
              │                         ▼
              │                  Query Refinement
              │                         │
              │                         ▼
              │                  Second Retrieval
              │                         │
              │                         ▼
              │                  Evidence Evaluation
              │                         │
              │                  ┌──────┴──────┐
              │                  │             │
              │             SUFFICIENT    INSUFFICIENT
              │                  │             │
              └──────────────────┤             ▼
                                 │          Refusal
                                 ▼
                         Grounded Generation
                                 │
                                 ▼
                         Source Attribution
                                 │
                                 ▼
                            Streamlit UI
```

---

# Agent Workflow

## 1. Initial Retrieval

The user's question is converted into an embedding using:

```text
all-MiniLM-L6-v2
```

The embedding is compared against the vectors stored in ChromaDB.

The initial retrieval returns the most relevant chunks together with their metadata and retrieval distances.

Example:

```text
Retrieved sources:

- Neural-Networks.md
  chunk 0
  distance = 0.8080

- Neural-Networks.md
  chunk 1
  distance = 0.9681

- Neural-Networks.md
  chunk 2
  distance = 1.2152
```

---

## 2. Evidence Evaluation

The retrieved context is passed to an LLM-based evidence evaluator.

The evaluator is instructed to:

* Use only the retrieved knowledge.
* Avoid general knowledge.
* Avoid assumptions.
* Reject information that is merely related.
* Return `SUFFICIENT` only when enough evidence exists.

The evaluator returns:

```text
SUFFICIENT
```

or:

```text
INSUFFICIENT
```

This creates a decision layer between retrieval and generation.

---

## 3. Adaptive Query Refinement

When the initial evidence is insufficient, the agent does not immediately refuse.

It first attempts to improve retrieval by refining the original question.

Example:

```text
Original:

What are stages of ML life cycle and why it important to ML Models?

Refined:

machine learning lifecycle stages importance
```

The refined query is then used for another vector search.

---

## 4. Second Retrieval

The refined query is used to perform a second retrieval.

The second retrieval can use a larger number of chunks than the initial search.

```text
Initial retrieval:
top_k = 3

Adaptive retrieval:
top_k = 5
```

The newly retrieved context is evaluated again.

---

## 5. Grounded Answer Generation

If the evidence evaluator determines that the context is sufficient, the retrieved documents are passed to the LLM.

The generation prompt instructs the model to:

* Use only the retrieved knowledge.
* Avoid unsupported information.
* Avoid hallucinating.
* Provide a concise answer.
* Use the supplied knowledge-base context as the source of truth.

---

## 6. Grounded Refusal

If the second evidence evaluation is still insufficient, the system refuses to answer.

Example:

```text
I couldn't find enough information in the knowledge base.
```

This is an intentional design decision.

The application prioritizes:

```text
Groundedness > Answering every question
```

---

# Source Attribution

Every retrieved chunk contains metadata such as:

```text
source
chunk_id
```

The application uses this metadata to display the source associated with the generated answer.

Example:

```text
Sources

Machine-Learning/Neural-Networks.md
Chunk: 0
```

This allows users to understand where the retrieved knowledge came from.

---

# Evaluation

The project uses **LLM-as-a-Judge evaluation** to measure the quality of answers generated by the RAG system.

The evaluation is performed only on questions labelled as `answerable` that the agent actually answered.

Questions that were wrongly refused are reported separately and excluded from answer-quality scoring.

The evaluation measures two main dimensions.

## 1. Faithfulness

Faithfulness measures whether factual claims in the generated answer are supported by the retrieved context.

A claim that may be generally true but is not present in the retrieved knowledge is treated as unsupported.

This directly evaluates the project's main grounding objective.

## 2. Answer Relevancy

Answer relevancy measures whether the generated response actually addresses the user's question.

A response can be factually grounded but still fail to properly answer the user's question, so relevancy is evaluated separately.

---

# LLM-as-a-Judge Results

Current evaluation results:

```text
Answered & scored:      8
Wrongly refused:        1

Mean Faithfulness:      0.75
Mean Relevancy:         0.97
```

The results show that the generated answers generally address the user's questions well, while faithfulness still has room for improvement.

The evaluation identified cases where the LLM added generally plausible information that was not explicitly present in the retrieved context.

For example, some neural-network answers introduced statements about input and output layer behavior that were not directly supported by the retrieved chunks.

This demonstrates how evaluation can be used not only to report performance but also to identify areas for improvement.

---

# Example Evaluation Finding

For one neural-network question, the judge reported:

```text
Faithfulness: 0.40
Relevancy:    1.00
```

The answer was highly relevant to the question but contained several claims that were not directly supported by the retrieved context.

This highlights an important RAG problem:

```text
Relevant answer ≠ Fully grounded answer
```

The system therefore evaluates both dimensions separately.

---

# Example Agent Execution

## Supported Question

```text
Question:
What is Retrieval-Augmented Generation?
```

Agent workflow:

```text
Agent started
        ↓
Initial retrieval completed
        ↓
Evidence evaluation:
SUFFICIENT
        ↓
Grounded answer generated
        ↓
Sources displayed
```

---

## Unsupported Question

```text
Question:
Why were transformers created and why are they
useful for building GPT?
```

Agent workflow:

```text
Agent started
        ↓
Initial retrieval
        ↓
INSUFFICIENT
        ↓
Query refinement
        ↓
Second retrieval
        ↓
INSUFFICIENT
        ↓
Refuse to answer
```

The system does not use the LLM's general knowledge to answer the question when the knowledge base cannot support it.

---

# Technology Stack

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| Python                | Application and RAG pipeline |
| Streamlit             | Web interface                |
| Sentence Transformers | Text embeddings              |
| all-MiniLM-L6-v2      | Embedding model              |
| ChromaDB              | Persistent vector database   |
| Groq API              | LLM inference                |
| Obsidian              | Knowledge source             |
| JSON                  | Evaluation configuration     |

---

# Project Structure

```text
Obsidian-Vault-RAG-Knowledge-Assistant/
│
├── data/
│   └── vault/
│       ├── AI/
│       └── Machine-Learning/
│
├── src/
│   ├── app.py
│   ├── rag.py
│   ├── chunking.py
│   └── vector_store.py
│
├── evaluation/
│   ├── questions.json
│   └── llm_judge_eval.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Yash1-23/Obsidian-Vault-RAG-Knowledge-Assistant.git
```

```bash
cd Obsidian-Vault-RAG-Knowledge-Assistant
```

---

## 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Configure the API Key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_api_key_here
```

Do not commit `.env` or API keys to GitHub.

---

# Build the Vector Store

Place Markdown files inside:

```text
data/vault/
```

Run:

```powershell
python src/chunking.py
```

Then:

```powershell
python src/vector_store.py
```

This creates the embeddings and stores them in ChromaDB.

---

# Run the Application

Start Streamlit:

```powershell
streamlit run src/app.py
```

The application opens a browser interface where users can ask questions about the Obsidian knowledge base.

---

# Run LLM-as-a-Judge Evaluation

Make sure the `GROQ_API_KEY` environment variable is configured.

Run:

```powershell
python evaluation/llm_judge_eval.py
```

The evaluator:

1. Loads the evaluation questions.
2. Runs answerable questions through the RAG agent.
3. Excludes questions the agent refuses.
4. Sends the answer and retrieved context to an independent judge prompt.
5. Calculates faithfulness and relevancy scores.
6. Reports per-question results.
7. Calculates mean scores.

---

# Design Decisions

## Why RAG?

RAG allows the application to retrieve information from the user's own knowledge base before generating an answer.

This makes the system useful for private or domain-specific knowledge that may not be available directly from the model's pretrained knowledge.

---

## Why ChromaDB?

ChromaDB provides a lightweight persistent vector database that works well for a local MVP.

It stores embeddings together with metadata and supports similarity search.

---

## Why Sentence Transformers?

Sentence Transformers convert text into semantic vector representations.

This allows the system to retrieve conceptually related information even when the question and document use different wording.

---

## Why an Evidence Evaluation Agent?

Similarity search alone does not guarantee that the retrieved documents contain enough information to answer a question.

The evidence evaluator introduces a decision layer:

```text
Retrieved context
       ↓
Evidence evaluation
       ↓
Is there enough evidence?
```

This helps the system distinguish between **related context** and **sufficient evidence**.

---

## Why Query Refinement?

A user's natural-language question may not always produce optimal retrieval results.

The query refinement step allows the agent to reformulate the search query while preserving the original intent.

This gives the system another opportunity to retrieve the required evidence.

---

## Why Refuse Unsupported Questions?

An AI knowledge assistant should not present the LLM's general knowledge as if it came from the user's knowledge base.

The refusal mechanism makes the system conservative when evidence is unavailable.

---

# Limitations

The current MVP has several limitations:

* The knowledge source is currently Markdown-based.
* Retrieval quality depends on chunking and embedding quality.
* The evaluation dataset is relatively small.
* The evidence evaluator depends on LLM judgment.
* LLM-as-a-Judge scores can vary depending on the judge model and prompt.
* The current vector database is designed for local MVP usage.
* The system does not currently provide multi-user authentication.
* Conversation memory is not implemented.
* The application is not optimized for production-scale concurrent workloads.

---

# Future Improvements

## Retrieval Improvements

* Hybrid keyword and vector retrieval
* Reranking retrieved chunks
* Metadata-aware filtering
* Improved chunking strategies
* Query expansion

## Agent Improvements

* Multiple retrieval strategies
* Confidence scoring
* Better retrieval planning
* Agent tracing
* Tool-based knowledge-base exploration

## Evaluation Improvements

* Larger evaluation datasets
* Retrieval precision and recall
* Automated regression testing
* More comprehensive faithfulness evaluation
* Answer correctness evaluation
* Human evaluation

## Application Improvements

* Streaming responses
* Conversation memory
* Search history
* Knowledge-base management interface
* Authentication
* Multi-user vault support

## Production Improvements

* Cloud deployment
* Scalable vector database
* API backend
* Observability
* Monitoring
* Error tracking
* Rate limiting

---

# What Makes This Project Different?

The project is not simply:

```text
Question → Vector Search → LLM
```

It implements a decision-making retrieval loop:

```text
Question
   ↓
Retrieve
   ↓
Evaluate Evidence
   ↓
Sufficient?
   │
   ├── YES
   │    ↓
   │  Generate Grounded Answer
   │
   └── NO
        ↓
     Refine Query
        ↓
     Retrieve Again
        ↓
     Evaluate Evidence
        │
        ├── YES → Generate
        │
        └── NO  → Refuse
```

This demonstrates practical Generative AI engineering concepts including:

* Retrieval-Augmented Generation
* Semantic search
* Vector databases
* Embeddings
* Prompt engineering
* LLM-based evaluation
* Agentic decision making
* Adaptive retrieval
* Grounded generation
* Hallucination prevention
* Source attribution
* Answer-quality evaluation

---

# Conclusion

The Obsidian AI Knowledge Assistant is an end-to-end agentic RAG MVP designed around a simple principle:

> **The system should only answer when the knowledge base provides sufficient supporting evidence.**

The project combines:

```text
Obsidian Knowledge
        +
Semantic Retrieval
        +
Evidence Evaluation
        +
Adaptive Query Refinement
        +
Grounded Generation
        +
Source Attribution
        +
LLM-as-a-Judge Evaluation
```

The current evaluation shows a **0.97 mean answer relevancy** and **0.75 mean faithfulness** across 8 successfully answered evaluation questions.

Rather than treating evaluation as a final checkbox, the project uses it to identify concrete weaknesses in grounding and guide future improvements.
