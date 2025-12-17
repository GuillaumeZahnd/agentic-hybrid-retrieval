import os
import re
import numpy as np
import faiss
from rank_bm25 import BM25Okapi
from mistralai import Mistral
from nltk.stem import PorterStemmer

from source.agentic_router import agentic_router


client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))


def preprocess_text(text: str):
    stemmer = PorterStemmer()
    STOP_WORDS = {"how", "many", "do", "have", "the", "a", "is", "are", "of"}
    text = re.sub(r'[^\w\s]', '', text.lower())
    tokens = text.split()
    return [stemmer.stem(w) for w in tokens if w not in STOP_WORDS]


def get_embeddings(texts: list[str]):
    res = client.embeddings.create(model="mistral-embed", inputs=texts)
    return np.array([e.embedding for e in res.data]).astype('float32')


def run_fast_path(query: str, documents: list[str], top_k=1):
    """BM25 Lexical Search: Extremely fast, keyword-based."""
    print("⚡ Executing Fast Path (BM25)")
    tokenized_query = preprocess_text(query)
    tokenized_corpus = [preprocess_text(doc) for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)
    results = bm25.get_top_n(tokenized_query, documents, n=top_k)
    return results


def run_deep_path(query: str, documents: list[str], top_k=5):
    """Vector Search + Rerank: Semantic, handles conceptual queries."""
    print("🧠 Executing Deep Path (Vector Search + Reranking)")
    
    document_embeddings = get_embeddings(documents)
    index = faiss.IndexFlatL2(document_embeddings.shape[1])
    index.add(document_embeddings)

    query_embeddings = get_embeddings([query])
    distances, indices = index.search(query_embeddings, top_k)
    
    candidates = [documents[i] for i in indices[0] if i != -1]
    
    # TODO: Add reranking
    return [candidates[0]] 



def unified_retrieval(query: str, documents: list[str]):
    route_decision = agentic_router(query)
    if route_decision.path == "fast":
        return run_fast_path(query=query, documents=documents)
    elif route_decision.path == "deep":
        return run_deep_path(query=query, documents=documents)
    else:
        raise ValueError("Invalid route decision: '{}'. Expected either 'fast' or 'deep'.".format(route_decision.path))

        
def unified_rag_pipeline(query: str, documents: list[str]) -> tuple[str, str]:
    """
    Combines routing, retrieval, and generation to return both the context and the final answer.
    """

    retrieved_chunks = unified_retrieval(query=query, documents=documents) 
    context_str = " ".join(retrieved_chunks)
        
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "system", "content": "Answer the question using ONLY the provided context."},
            {"role": "user", "content": f"Context: {context_str}\n\nQuestion: {query}"}
        ]
    )
    actual_answer = response.choices[0].message.content
    
    return context_str, actual_answer        
