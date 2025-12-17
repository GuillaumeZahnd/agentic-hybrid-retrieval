import os
import instructor
from mistralai import Mistral
from pydantic import BaseModel, Field
from typing import Literal


client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))
instructor_client = instructor.from_mistral(client, mode=instructor.Mode.MISTRAL_TOOLS)


class RouteDecision(BaseModel):
    """Decision made by the router, about when to be fast and when to take more time."""
    path: Literal["fast", "deep"] = Field(..., description="Which retrieval path was chosen.")
    reasoning: str = Field(..., description="The reson why this path was chosen.")


def agentic_router(user_query: str) -> RouteDecision:
    """Analyze the query to decide between Fast (BM25) and Deep (Vector + Rerank) retrieval."""
    return instructor_client.chat.completions.create(
        model="mistral-large-latest",
        response_model=RouteDecision,
        messages=[
            {"role": "system", "content": """You are an Efficient Retrieval Router.
             - Choose 'fast' for simple keyword lookups, greetings, or specific entity names.
             - Choose 'deep' for questions requiring conceptual understanding, comparison, or synthesis of multiple facts."""},
            {"role": "user", "content": f"Query: {user_query}"}
        ]
    )
