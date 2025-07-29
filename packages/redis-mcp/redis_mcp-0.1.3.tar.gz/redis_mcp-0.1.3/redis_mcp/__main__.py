"""
Redis MCP Server: A FastMCP-based server with SSE support for Redis operations.

This module provides a FastMCP-based implementation of Redis operations and
task management with real-time updates via SSE.
"""

from redis_mcp.server import RedisMCPServer
import argparse

def cli():
    parser = argparse.ArgumentParser(description="Redis MCP Server")
    parser.add_argument("--transport", default="stdio", help="MCP Transport type, stdio, sse, or streamable-http")
    parser.add_argument("--host", default="localhost", help="Redis host")
    parser.add_argument("--port", default=6379, type=int, help="Redis port")
    parser.add_argument("--db", type=int, default=0, help="Port to bind to for SSE transport")
    args = parser.parse_args()
    RedisMCPServer(host=args.host, port=args.port, db=args.db).run(args.transport)

if __name__ == "__main__":
    cli()

