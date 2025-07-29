import argparse
from apibeat.monitor import benchmark_rest, benchmark_graphql

def main():
    parser = argparse.ArgumentParser(description="Benchmark REST and GraphQL APIs")
    parser.add_argument('--url', required=True, help="API endpoint to test")
    parser.add_argument('--method', default='GET', help="HTTP method (for REST)")
    parser.add_argument('--query', help="GraphQL query string")
    parser.add_argument('--type', choices=['rest', 'graphql'], default='rest', help="API type")

    args = parser.parse_args()

    if args.type == 'rest':
        result = benchmark_rest([{"url": args.url, "method": args.method.upper()}])
    else:
        if not args.query:
            print("❌ Please provide a GraphQL query using --query")
            return
        result = benchmark_graphql([{"url": args.url, "query": args.query}])

    print("\n📊 Result:")
    print(f"{result['type']} Average Latency: {result['average_latency_ms']}ms")
