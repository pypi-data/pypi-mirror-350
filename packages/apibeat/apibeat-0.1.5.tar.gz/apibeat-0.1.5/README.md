# 📦 apibeat

**A simple CLI tool to benchmark and compare REST vs GraphQL API performance by measuring average latency.**



## Features

- Measure average latency of REST and GraphQL endpoints  
- Support custom HTTP methods (GET, POST, etc.) for REST  
- Accept GraphQL queries via CLI  
- Simple, clean CLI interface  
- Useful for API optimization and performance comparisons  

---

## Installation

### Install from PyPI

```bash
pip install apibeat



### Use a different HTTP method (REST)

```bash
apibeat --url https://api.example.com/data --method POST


### Use a different HTTP method (GraphQL Apis)


```bash
apibeat --type graphql --url https://api.example.com/graphql --query "{ users { id name } }"

## CLI Arguments

| Argument  | Description                                   | Required            | Default |
|-----------|-----------------------------------------------|---------------------|---------|
| `--url`   | The API endpoint URL to benchmark              | Yes                 | —       |
| `--type`  | API type: `rest` or `graphql`                  | No                  | `rest`  |
| `--method`| HTTP method for REST requests                   | No (only for REST)  | `GET`   |
| `--query` | GraphQL query string (required if `--type graphql`) | Conditional         | —       |


For any questions or support, please open an issue or contact [demonking15543@gmail.com](mailto:demonking15543@gmail.com).
