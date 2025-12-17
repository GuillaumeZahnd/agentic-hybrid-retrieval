import os

from source.two_path_retrieval import unified_rag_pipeline


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
    
        retrieved_context, answer = unified_rag_pipeline(q["query"], documents)

        print("Query: {}".format(q["query"]))
        print("Retrieved context: {}".format(retrieved_context))
        print("Expected route: {}".format(q["expectation"]))
        print("Answer: {}".format(answer))
        print("\n")
