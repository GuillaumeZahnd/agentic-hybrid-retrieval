# Agentic Hybrid Retrieval

This toy project is an **Agentic Hybrid Retrieval Framework** 🤖 designed to balance operational cost with response depth. It addresses the "one-size-fits-all" limitation of standard Retrieval-Augmented Generation (RAG) by implementing a dynamic, two-path architecture that optimizes for both computational efficiency and answer quality.

The framework functions as an autonomous decision engine, calibrating computational expenditure based on self-assessed query complexity. It directs simple factual lookups through a "Fast" ⚡ lightweight path to minimize latency and cost, while shifting to a "Deep" 🧠 high-resource path when the demand for precision requires sophisticated synthesis and reranking.

🛠️ Key technical pillars

- **Adaptive routing:** An intelligent gateway that classifies queries on-the-fly (either "Fast" or "Deep") to optimize latency and resource allocation, while preserving answer quality.

- **Cold-start benchmarking:** Synthetic generation of test cases to build a robust evaluation suite from scratch.

- **Label-free evaluation:** Implementing "LLM-as-a-judge" to grade production performance (faithfulness and routing accuracy) without human-annotated data.

- **Precision engineering:** Enhancing the retrieval layer with rerank models to eliminate hallucinations in high-complexity scenarios.

🐻🦠 Also, the toy documents are about tardigrades 👽🔬

![tardigrade](https://github.com/user-attachments/assets/58a30f46-78bb-4a09-a380-f005a8e776f8)

## Running the scripts

### `generate_benchmark.py`

> This script automates the creation of a high-quality, cold-start RAG evaluation suite by generating synthetic test cases from raw text chunks. It uses LLM-as-a-Judge logic to categorize adversarial data points into specific complexity tiers—Lexical, Semantic, and Reasoning—to rigorously test retrieval and synthesis performance.
> 
> 📋 Key features:
> 
> **Structured outputs:** Uses Pydantic to ensure every test point includes ground truth and verification logic.
> 
> **Adversarial benchmarking:** Specifically targets the weaknesses of different retrieval methods (BM25 vs. Vector Search).
> 
> **Automated ground truth:** Eliminates the need for manual labeling in production environments.

🧬 Processing chunk: Tardigrades, known colloquially as water bears or moss pigle...

🧬 Processing chunk: Tardigrades are among the most resilient animals known, with...

🧬 Processing chunk: In 1773, Johann August Ephraim Goeze named the tardigrade Kl...

🧬 Processing chunk: Tardigrade DNA is protected from radiation by the Dsup ("dam...

✅ Created a synthetic evaluation test suite of 12 data points.

#### Example 1 (Lexical)

**`question:`** "What are tardigrades known for in terms of their ability to withstand harsh environments?",
**`ground_truth:`** "They are among the most resilient animals known, able to survive severe conditions like extreme temperatures, pressures, air deprivation, radiation, dehydration, and starvation.",
**`complexity:`** "Lexical",
**`is_answerable:`** true,
**`verification_logic:`** "This question uses exact keywords and phrases from the context, such as 'tardigrades,' 'resilient,' 'survive,' 'severe conditions,' and 'extreme temperatures.' This tests keyword-based retrieval like BM25."

#### Example 2 (Semantic)

**`question:`** "Which molecule helps shield genetic material in water bears from harmful radiation effects?",
**`ground_truth:`** "Dsup protein",
**`complexity:`** "Semantic",
**`is_answerable:`** true,
**`verification_logic:`** "The question avoids unique nouns like 'tardigrade' (replaced with 'water bears') and 'Dsup' (replaced with 'molecule'). It uses synonyms and rephrased terms to test vector search capabilities."

#### Example 3 (Reasoning)

**`question:`** "How does the Dsup protein of Ramazzottius varieornatus contribute to both radiation resistance and DNA repair?",
**`ground_truth:`** "It protects chromosomal DNA from hydroxyl radicals and upregulates DNA repair genes.",
**`complexity:`** "Reasoning",
**`is_answerable:`** true,
**`verification_logic:`** "This question requires synthesizing information from two different sentences: (1) Dsup protects chromosomal DNA from hydroxyl radicals, and (2) it upregulates DNA repair genes to confer resistance to ultraviolet-C. This tests multi-fact synthesis."

### `demo_agentic_router.py`

> This script implements an agentic gateway that autonomously classifies user queries to optimize the RAG pipeline's computational efficiency. By analyzing query complexity on-the-fly, it directs traffic to either a "fast" path for simple lookups or a "deep" path for tasks requiring complex synthesis and reranking.
> 
> ⚙️ Core mechanics:
> 
> **Dynamic resource allocation:** Minimizes latency and cost by reserving high-compute resources only for reasoning-heavy queries.
>
> **Structured metadata:** Returns a Pydantic-validated RouteDecision containing both the chosen path and the model's underlying rationale.

#### Example 1

🔍 **Query:** How many legs do tardigrades have?

🎯 **Expected decision:** FAST

🤖 **Agent decision:** FAST

💡 **Reason:** The question is a simple factual lookup about a specific attribute (number of legs) of a well-defined entity (tardigrades). It does not require conceptual understanding or synthesis of multiple facts.

#### Example 2

🔍 **Query:** Why are some of the tardigrade proteins of interest to biomedical research?

🎯 **Expected decision:** DEEP

🤖 **Agent decision:** DEEP

💡 **Reason:** The query requires a conceptual understanding of tardigrade biology, specifically their proteins, and how these relate to broader biomedical research. This involves synthesizing information about tardigrade survival mechanisms, the role of their proteins, and their potential applications in medicine.

### `demo_hybrid_retrieval.py`

> This script provides the operational core of the Hybrid RAG Pipeline, orchestrating the execution of two different retrieval strategies based on real-time agentic routing. It manages the bifurcation between a "Fast Path" utilizing BM25 lexical search for keyword efficiency and a "Deep Path" employing FAISS vector search and reranking for nuanced semantic synthesis.
> 
> ⚙️ Core mechanics:
>
> **Multi-modal retrieval:** Integrates both token-based (BM25) and embedding-based (FAISS) retrieval methods.
>
> **Intelligent bifurcation:** Wraps the agentic_router to dynamically select the retrieval depth, returning the context, the final answer, and the path metadata for evaluation.
>
> **Contextual generation:** Filters input through the chosen path to ensure the final generation is grounded strictly in retrieved chunks.

#### Example 1

🔍 **Query:** How many legs do tardigrades have?

🎯 **Expected route:** FAST

⚡ Executing Fast Path (BM25)

📚 **Retrieved context:** Tardigrades, known colloquially as water bears or moss piglets, are a phylum of eight-legged segmented micro-animals.

💬 **Answer:** Tardigrades have eight legs.

#### Example 2

🔍 **Query:** Why are some of the tardigrade proteins of interest to biomedical research?

🎯 **Expected route:** DEEP

🧠 Executing Deep Path (Vector Search + Reranking)

📚 **Retrieved context:** Tardigrade DNA is protected from radiation by the Dsup ("damage suppressor") protein. The Dsup proteins of Ramazzottius varieornatus and H. exemplaris promote survival by binding to nucleosomes and protecting chromosomal DNA from hydroxyl radicals. The Dsup protein of R. varieornatus confers resistance to ultraviolet-C by upregulating DNA repair genes.

💬 **Answer:** Based on the provided context, some tardigrade proteins, like the Dsup protein, are of interest to biomedical research because they protect DNA from damage caused by radiation (such as hydroxyl radicals) and ultraviolet-C light. Additionally, they can promote survival by binding to nucleosomes and upregulating DNA repair genes.

### `main_evaluator.py`

> This script implements an LLM-as-a-Judge evaluation framework to audit the RAG pipeline's performance in production without labeled data. It automates the verification of faithfulness—identifying hallucinations by cross-referencing generated answers against retrieved contexts—while logging the accuracy of agentic routing decisions across different query complexities.
> 
> 🛠️ Key technical pillars:
>
> "Production audit:" Uses high-reasoning models (Mistral Large) to grade pipeline outputs on a strict 1-5 scale.
>
> "Routing verification:" Tracks which path "Fast" vs. "Deep" was taken and compares it to the predefined query complexity.
>
> "Granular telemetry:" Provides detailed logs to visualize the relationship between retrieval depth, question difficulty, and final answer quality.

🔍 Query: What are tardigrades commonly referred to as?

Complexity: Lexical | Route taken: fast | Decision faithfulness: 5/5

🔍 Query: What is the informal name for these microscopic eight-legged cre...

Complexity: Semantic | Route taken: fast | Decision faithfulness: 5/5

🔍 Query: How many legs do tardigrades have, and what are they often calle...

Complexity: Reasoning | Route taken: fast | Decision faithfulness: 3/5

🔍 Query: What are tardigrades known for in terms of their ability to with...

Complexity: Lexical | Route taken: deep | Decision faithfulness: 5/5

🔍 Query: Which microscopic creatures can endure exposure to the vacuum an...

Complexity: Semantic | Route taken: deep | Decision faithfulness: 5/5

🔍 Query: How do tardigrades' survival abilities in space relate to their ...

Complexity: Reasoning | Route taken: deep | Decision faithfulness: 5/5

🔍 Query: What did Johann August Ephraim Goeze name the tardigrade in 1773...

Complexity: Lexical | Route taken: fast | Decision faithfulness: 5/5

🔍 Query: What term did a German scientist use for a microscopic organism ...

Complexity: Semantic | Route taken: fast | Decision faithfulness: 5/5

🔍 Query: Why is the tardigrade referred to as both a 'water bear' and a '...

Complexity: Reasoning | Route taken: deep | Decision faithfulness: 5/5

🔍 Query: What protein protects tardigrade DNA from radiation according to...

Complexity: Lexical | Route taken: fast | Decision faithfulness: 5/5

🔍 Query: Which molecule helps shield genetic material in water bears from...

Complexity: Semantic | Route taken: fast | Decision faithfulness: 5/5

🔍 Query: How does the Dsup protein of Ramazzottius varieornatus contribut...

Complexity: Reasoning | Route taken: deep | Decision faithfulness: 5/5

## Python environment

```sh
python -m pip install --upgrade setuptools pip
mkdir .venv
pipenv install -d --python 3.12
```
