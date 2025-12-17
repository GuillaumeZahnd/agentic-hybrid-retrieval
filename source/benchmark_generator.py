import os
import instructor
from mistralai import Mistral
from pydantic import BaseModel, Field


client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))
instructor_client = instructor.from_mistral(client, mode=instructor.Mode.MISTRAL_TOOLS)


class SyntheticDataPoint(BaseModel):
    question: str = Field(..., description="The generated question.")
    ground_truth: str = Field(..., description="The correct answer based on context.")
    complexity: str = Field(..., description="Type of question: Lexical, Semantic, or Reasoning.")
    is_answerable: bool = Field(True, description="Whether the question can be answered by the context.")
    verification_logic: str = Field(..., description="Brief reasoning why this question tests the specific complexity.")


def generate_synthetic_evaluation_test_suite(text_chunks: list[str]) -> list[SyntheticDataPoint]:
    benchmark_set = []

    for chunk in text_chunks:
        print("🧬 Processing chunk: {}...".format(chunk[:60]))
        try:
            response = instructor_client.chat.completions.create(
                model="mistral-large-latest",
                response_model=list[SyntheticDataPoint],
                messages=[
                    {"role": "system", "content": "You are a Senior QA Engineer for RAG systems. Your task is to generate high-quality, adversarial benchmark data."},
                    {"role": "user", "content": f"""
                        Task:
                        - Create 3 test points from this context.
                        Strict complexity definitions:
                        - 'Lexical': Must use exact keywords and phrases from the text. This tests BM25/keyword retrieval.
                        - 'Semantic': Can not use the unique nouns or verbs from the context. Use synonyms only. This tests Vector search.
                        - 'Reasoning': Must require synthesis of facts from at least two different sentences.
                        Formatting constraints:
                        - Ensure the 'ground_truth' is concise.

                        Context: {chunk}
                    """}
                ]
            )
            benchmark_set.extend(response)

        except Exception as e:
            print(f"⚠️ Error: {e}")

    return benchmark_set
