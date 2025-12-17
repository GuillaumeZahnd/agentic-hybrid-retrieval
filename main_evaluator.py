import os
import json

from source.evaluator import run_evaluation_suite


if __name__ == "__main__":

    test_suite_path = "benchmark_data"
    test_suite_filename = "synthetic_evaluation_test_suite.json"
    chunks_filename = "raw_chunks.txt"    

    with open(os.path.join(test_suite_path, chunks_filename), "r") as fid:
        documents = [line.rstrip() for line in fid]    

    with open(os.path.join(test_suite_path, test_suite_filename), "r") as f:
        test_suite = json.load(f)    

    evaluation_report = run_evaluation_suite(
        benchmark=test_suite, documents=documents)
