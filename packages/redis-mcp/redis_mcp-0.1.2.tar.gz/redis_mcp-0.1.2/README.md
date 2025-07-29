# Redis MCP Server

A Model Context Protocol (MCP) server for Redis operations built with FastMCP.

## Features

- Core Redis operations: get, set, delete, list
- Bulk operations: mget, mset
- Pattern-based key scanning
- Connection pooling for efficient Redis access
- Multiple transport support (stdio, SSE, streamable-http)
- Environment-based configuration
- Type hints and comprehensive error handling

## Installation

### From PyPI

```bash
pip install redis-mcp
```

Or using uv:

```bash
uv tool install redis-mcp
```

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/redis-mcp.git
cd redis-mcp

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Configuration

The server can be configured via environment variables:

- `REDIS_HOST`: Redis server hostname (default: localhost)
- `REDIS_PORT`: Redis server port (default: 6379)
- `REDIS_DB`: Redis database number (default: 0)
- `REDIS_PASSWORD`: Redis password (optional)
- `REDIS_USERNAME`: Redis username (optional)

## Usage

### As a CLI Tool

```bash
# Using stdio transport (default)
redis-mcp

# Using SSE transport
redis-mcp --transport sse

# With custom Redis connection
redis-mcp --host redis.example.com --port 6380 --db 1
```

### In Claude Desktop

Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "redis": {
      "command": "uvx",
      "args": ["redis-mcp"],
      "env": {
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379"
      }
    }
  }
}
```

### Available Tools

- **get**: Retrieve a value by key
- **set**: Store a key-value pair with optional expiry and conditions
- **delete**: Remove one or more keys
- **list**: List keys matching a pattern
- **mget**: Get multiple values in one operation
- **mset**: Set multiple key-value pairs in one operation
- **scan**: Iterate through keys matching a pattern without blocking

### Example Usage

```python
from fastmcp import Client

async def main():
    async with Client("http://localhost:8000/sse") as client:
        # Set a value
        await client.call_tool("set", {"key": "user:123", "value": "John Doe"})
        
        # Get a value
        result = await client.call_tool("get", {"key": "user:123"})
        print(result)  # "John Doe"
        
        # List keys
        keys = await client.call_tool("list", {"pattern": "user:*"})
        print(keys)  # ["user:123"]
```

## Development

### Setup

```bash
# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black .
isort .

# Type checking
mypy .

# Linting
ruff check .
```

## Requirements

- Python 3.10+
- Redis server
- FastMCP 2.3.3+

## License

MIT
