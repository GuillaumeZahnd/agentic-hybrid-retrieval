import os
import json

from source.benchmark_generator import generate_synthetic_evaluation_test_suite


if __name__ == "__main__":

    test_suite_path = "benchmark_data"
    chunks_filename = "raw_chunks.txt"
    test_suite_filename = "synthetic_evaluation_test_suite.json"

    with open(os.path.join(test_suite_path, chunks_filename)) as fid:
        raw_chunks = [line.rstrip() for line in fid]
        
    benchmark = generate_synthetic_evaluation_test_suite(raw_chunks)

    if not os.path.exists(test_suite_path):
        os.makedirs(test_suite_path)

    with open(os.path.join(test_suite_path, test_suite_filename), "w") as fid:
        json.dump([item.model_dump() for item in benchmark], fid, indent=4)

    print("✅ Created a synthetic evaluation test suite of {} data points.".format(len(benchmark)))
