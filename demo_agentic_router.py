from source.agentic_router import agentic_router

if __name__ == "__main__":

    test_queries = [
        {"query": "How many legs do tardigrades have?", "expectation": "Fast"},
        {"query": "Why are some of the tardigrade proteins of interest to biomedical research?", "expectation": "Deep"}
    ]

    for q in test_queries:
        decision = agentic_router(q["query"])
        print("🔍 Query: {}\n🎯 Expected decision: {}\n🤖 Agent decision: {}\n💡 Reason: {}\n".format(
            q["query"], q["expectation"].upper(), decision.path.upper(), decision.reasoning))
