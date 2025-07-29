import json
from apibeat.monitor import benchmark_rest, benchmark_graphql

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_results(data):
    with open("results/output.json", "w") as f:
        json.dump(data, f, indent=2)

def main():
    rest_tests = load_json("benchmarks/rest_tests.json")
    graphql_tests = load_json("benchmarks/graphql_tests.json")

    rest_result = benchmark_rest(rest_tests)
    graphql_result = benchmark_graphql(graphql_tests)

    print("\n📊 Results:")
    print(f"REST Average Latency: {rest_result['average_latency_ms']}ms")
    print(f"GraphQL Average Latency: {graphql_result['average_latency_ms']}ms")

    winner = (
        "REST" if rest_result["average_latency_ms"] < graphql_result["average_latency_ms"]
        else "GraphQL"
    )
    print(f"\n🏆 Winner: {winner} is faster.")

    save_results({
        "rest": rest_result,
        "graphql": graphql_result,
        "winner": winner
    })

if __name__ == "__main__":
    main()
