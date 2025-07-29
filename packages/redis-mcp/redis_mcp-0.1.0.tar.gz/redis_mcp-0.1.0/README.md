# Redis MCP Server

A FastMCP-based server with Server-Sent Events (SSE) support for Redis operations and task management.

## Features

- Core Redis operations (get, set, list, delete)
- Task management system built on Redis
- Real-time updates via SSE
- Clean separation of concerns using the mounting pattern
- Comprehensive testing

## Requirements

- Python 3.10+
- Redis server
- FastMCP 2.3.3+

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/redis-mcp.git
cd redis-mcp

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package with development dependencies
pip install -e ".[dev]"
```

## Usage

```python
from fastmcp import Client

async def main():
    # Connect via SSE
    async with Client("http://localhost:8000/sse") as client:
        # Use Redis operations
        result = await client.call_tool("redis_get", {"key": "my_key"})
        print(f"Result: {result}")
```

## Development

```bash
# Run tests
pytest

# Format code
black .
isort .
```

## License

MIT
