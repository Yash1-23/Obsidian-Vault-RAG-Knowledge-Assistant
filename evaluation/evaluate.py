import os
import sys
import json
import re

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from rag import agent_answer 

from groq import Groq  

JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "openai/gpt-oss-120b")

QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "questions.json")
REFUSAL_MARKERS = ("couldn't find enough information", "insufficient information")

JUDGE_SYSTEM = (
    "You are a strict, literal evaluator of a retrieval-augmented answer. "
    "Judge ONLY whether the answer is supported by the provided context and "
    "whether it addresses the question. A claim that is true in general but "
    "NOT present in the context counts as UNSUPPORTED -- never use outside "
    "knowledge. Return ONLY a JSON object, no prose, no markdown."
)

JUDGE_TEMPLATE = """Question:
{question}

Retrieved context (the ONLY allowed source of truth):
{context}

Answer to evaluate:
{answer}

Return a JSON object with exactly these keys:
- "faithfulness": float 0.0-1.0 = fraction of the answer's factual claims that
  are directly supported by the context above.
- "unsupported_claims": list of short strings, each an answer claim NOT found
  in the context (empty list if none).
- "relevancy": float 0.0-1.0 = how completely the answer addresses the question.
- "reason": one short sentence explaining the faithfulness score.
"""


def is_refusal(answer: str) -> bool:
    a = answer.lower()
    return any(marker in a for marker in REFUSAL_MARKERS)


def extract_json(text: str) -> dict:
    """Pull a JSON object out of a model reply, tolerating fences and stray prose."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no JSON object in judge reply")
    return json.loads(text[start:end + 1])


def judge_one(client, question, contexts, answer):
    context_block = "\n\n".join(f"[{i}] {c}" for i, c in enumerate(contexts)) or "(no context retrieved)"
    prompt = JUDGE_TEMPLATE.format(question=question, context=context_block, answer=answer)
    resp = client.chat.completions.create(
        model=JUDGE_MODEL,
        temperature=0,
        # Remove the next line if your judge model rejects it.
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM},
            {"role": "user", "content": prompt},
        ],
    )
    return extract_json(resp.choices[0].message.content)


def main():
    if not os.environ.get("GROQ_API_KEY"):
        sys.exit("Set GROQ_API_KEY in your environment first.")

    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
    answerable = [q for q in questions if q["expected"] == "answerable"]

    client = Groq()
    scored, refused, errors = [], [], []

    print("=" * 74)
    print(f"LLM-AS-JUDGE ANSWER-QUALITY EVALUATION  (judge: {JUDGE_MODEL})")
    print("=" * 74)

    for item in answerable:
        question = item["question"]
        answer, _meta, documents, _dist, _steps = agent_answer(question)

        if is_refusal(answer):
            refused.append(question)
            continue

        try:
            verdict = judge_one(client, question, list(documents), answer)
            scored.append((question, float(verdict["faithfulness"]),
                           float(verdict["relevancy"]),
                           verdict.get("unsupported_claims", []),
                           verdict.get("reason", "")))
        except Exception as exc:  
            errors.append((question, str(exc)))

    print(f"\nAnswered & scored:            {len(scored)}")
    print(f"Wrongly refused (excluded):   {len(refused)}")
    for q in refused:
        print(f"    refused: {q}")
    if errors:
        print(f"Judge errors (excluded):      {len(errors)}")
        for q, e in errors:
            print(f"    error: {q}  ->  {e}")

    if not scored:
        sys.exit("\nNothing scored. Fix the gate or the judge call before reading numbers.")

    n = len(scored)
    mean_faith = sum(s[1] for s in scored) / n
    mean_rel = sum(s[2] for s in scored) / n

    print("\n" + "-" * 74)
    print("PER-QUESTION")
    print("-" * 74)
    for q, faith, rel, unsupported, reason in scored:
        print(f"\nQ: {q}")
        print(f"   faithfulness={faith:.2f}  relevancy={rel:.2f}")
        if unsupported:
            print(f"   unsupported claims: {unsupported}")
        if reason:
            print(f"   reason: {reason}")

    print("\n" + "=" * 74)
    print(f"MEAN faithfulness: {mean_faith:.2f}   MEAN relevancy: {mean_rel:.2f}   (n={n}, LLM-judged)")
    print("=" * 74)


if __name__ == "__main__":
    main()