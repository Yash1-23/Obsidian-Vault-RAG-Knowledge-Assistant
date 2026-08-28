import json
import sys
import os

sys.path.append(
  os.path.abspath(
    os.path.join(
      os.path.dirname(__file__),
      "..",
      "src"
    )
  )
)
from rag import agent_answer

QUESTIONS_FILE = os.path.join(
  os.path.dirname(__file__),
  "questions.json"
)


def load_questions():
  with open(
    QUESTIONS_FILE,
    "r",
    encoding="utf-8"
  ) as file:
    
    return json.load(file)
  
  
  
def evaluate():
  questions = load_questions()
  
  total = len(questions)
  
  correct =0
  answerable_total = 0 
  answerable_correct = 0 
  unanswerable_total = 0 
  unanswerable_correct = 0 
  
  print("\n") 
  print("=" * 70) 
  print("RAG EVALUATION") 
  print("=" * 70) 
  for index, item in enumerate( 
          questions, 
          start=1 
  ):
    
    question = item["question"]
    expected = item["expected"]
    
    
    
    print("\n" + "-" * 70)
    print(f"Test {index}/{total}")
    print(f"Question: {question}")
    print(f"Expected: {expected}")
    
    
    
    answer, metadatas, documents, distances,agent_steps = agent_answer(
            question
        )
    
    rejected = (
            "couldn't find enough information"
            in answer.lower()
            or
            "insufficient information"
            in answer.lower()
        )
    if rejected:
        actual = "unanswerable"
    else:
        actual = "answerable"
        
    passed = actual == expected
    
    print(f"Actual: {actual}")
    print(
            f"Result: "
            f"{'PASS' if passed else 'FAIL'}"
        )
        
    if passed:

            correct += 1


    if expected == "answerable":

            answerable_total += 1

            if actual == "answerable":

                answerable_correct += 1

    else:

            unanswerable_total += 1

            if actual == "unanswerable":

                unanswerable_correct += 1


    overall_accuracy = (
        correct / total * 100
        if total
        else 0
    )


    answerable_accuracy = (
        answerable_correct
        / answerable_total
        * 100
        if answerable_total
        else 0
    )


    unanswerable_accuracy = (
        unanswerable_correct
        / unanswerable_total
        * 100
        if unanswerable_total
        else 0
    )


    print("\n")
    print("=" * 70)
    print("EVALUATION RESULTS")
    print("=" * 70)


    print(
        f"Overall accuracy: "
        f"{overall_accuracy:.2f}%"
    )


    print(
        f"Answerable question accuracy: "
        f"{answerable_accuracy:.2f}%"
    )


    print(
        f"Unanswerable question detection: "
        f"{unanswerable_accuracy:.2f}%"
    )


    print("=" * 70)


if __name__ == "__main__":

    evaluate()
