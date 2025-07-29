import requests
import time
from typing import List, Dict

def benchmark_rest(endpoints: List[Dict]) -> Dict:
    print("Benchmarking REST endpoints...")
    total_time = 0
    for ep in endpoints:
        method = ep.get("method", "GET")
        url = ep["url"]
        start = time.time()
        response = requests.request(method, url)
        end = time.time()
        duration = round((end - start) * 1000, 2)
        total_time += duration
        print(f"✔ {method} {url} -> {duration}ms ({response.status_code})")
    avg = round(total_time / len(endpoints), 2)
    return {"type": "REST", "average_latency_ms": avg}

def benchmark_graphql(queries: List[Dict]) -> Dict:
    print("Benchmarking GraphQL endpoints...")
    total_time = 0
    for q in queries:
        url = q["url"]
        query = q["query"]
        start = time.time()
        response = requests.post(url, json={"query": query})
        end = time.time()
        duration = round((end - start) * 1000, 2)
        total_time += duration
        print(f"✔ POST {url} -> {duration}ms ({response.status_code})")
    avg = round(total_time / len(queries), 2)
    return {"type": "GraphQL", "average_latency_ms": avg}
