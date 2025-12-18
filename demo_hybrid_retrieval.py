import os

from source.hybrid_retrieval import hybrid_rag_pipeline


if __name__ == "__main__":

    test_suite_path = "benchmark_data"
    chunks_filename = "raw_chunks.txt"

    with open(os.path.join(test_suite_path, chunks_filename), "r") as fid:
        documents = [line.rstrip() for line in fid]

    test_queries = [
        {"query": "How many legs do tardigrades have?", "expectation": "Fast"},
        {"query": "Why are some of the tardigrade proteins of interest to biomedical research?", "expectation": "Deep"}
    ]

    for q in test_queries:

        print("🔍 Query: {}".format(q["query"]))
        print("🎯 Expected route: {}".format(q["expectation"].upper()))

        retrieved_context, answer = unified_rag_pipeline(q["query"], documents)

        print("📚 Retrieved context: {}".format(retrieved_context))
        print("💬 Answer: {}".format(answer))
        print("\n")
