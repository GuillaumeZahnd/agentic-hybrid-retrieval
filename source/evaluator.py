import os
import instructor
from mistralai import Mistral
from pydantic import BaseModel, Field

from source.hybrid_retrieval import hybrid_rag_pipeline

client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))
instructor_client = instructor.from_mistral(client, mode=instructor.Mode.MISTRAL_TOOLS)


class EvaluationScore(BaseModel):
    score: int = Field(..., description="Score from 1 to 5.")
    reasoning: str = Field(..., description="Explanation for the score.")


def evaluate_faithfulness(question: str, context: str, answer: str) -> EvaluationScore:
    """Checks if the answer is supported only by the context."""
    return instructor_client.chat.completions.create(
        model="mistral-large-latest",
        response_model=EvaluationScore,
        messages=[
            {"role": "system", "content": "You are a strict grader. Give a score in a scale from 1 to 5. A score of 5 is the best, and corresponds to a case where the answer is fully supported by the context. A score of 1 is the worst, and corresponds to a case that contains hallucinations."},
            {"role": "user", "content": f"Context: {context}\nQuestion: {question}\nAnswer: {answer}"}
        ]
    )


def run_evaluation_suite(benchmark, documents):

    results = []

    for test_case in benchmark:

        actual_context, actual_answer, route_taken = unified_rag_pipeline(
            query=test_case['question'], documents=documents)

        evaluation_result = evaluate_faithfulness(
            test_case['question'], actual_context, actual_answer)

        results.append({
            "question": test_case['question'],
            "score": evaluation_result.score,
            "route_taken": route_taken,
            "complexity": test_case['complexity']
        })

    return results


def print_detailed_logs(evaluation_report):
    for r in evaluation_report:
        if len(r['question']) > 64:
            question_string = r['question'][:64] + "..."
        else:
            question_string = r['question']

        print("🔍 Query: {}\nComplexity: {} | Route taken: {} | Decision faithfulness: {}/5\n".format(
            question_string, r['complexity'], r["route_taken"], r["score"]))
