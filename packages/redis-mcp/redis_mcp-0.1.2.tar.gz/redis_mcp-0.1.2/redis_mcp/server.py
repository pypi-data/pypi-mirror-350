"""
Main Redis MCP Server that combines Redis operations and task management.

This module mounts the Redis core operations and task management servers
to provide a unified interface with SSE support.
"""
import asyncio
import os
from typing import Any, Dict, List, Optional, Union
import redis.asyncio as redis
from fastmcp import FastMCP


class RedisMCPServer:
    """
    Redis core operations with connection pooling and bulk support.
    
    This class provides a clean interface for Redis operations without
    the redundancy of passing connection parameters to every method.
    """
    
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        db: Optional[int] = None,
        password: Optional[str] = None,
        username: Optional[str] = None,
        decode_responses: bool = True,
        max_connections: int = 50
    ):
        """
        Initialize Redis core with connection configuration.
        
        Args:
            host: Redis server hostname (default: from env or localhost)
            port: Redis server port (default: from env or 6379)
            db: Redis database number (default: from env or 0)
            password: Redis password (default: from env)
            username: Redis username (default: from env)
            decode_responses: Whether to decode responses to strings
            max_connections: Maximum number of connections in the pool
        """
        self.host = host or os.environ.get("REDIS_HOST", "localhost")
        self.port = port or int(os.environ.get("REDIS_PORT", "6379"))
        self.db = db or int(os.environ.get("REDIS_DB", "0"))
        self.password = password or os.environ.get("REDIS_PASSWORD")
        self.username = username or os.environ.get("REDIS_USERNAME")
        
        # Create connection pool
        self.pool = redis.ConnectionPool(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            username=self.username,
            decode_responses=decode_responses,
            max_connections=max_connections
        )
        
        # Create FastMCP server
        self.server = FastMCP("Redis Core Operations")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register all Redis operations as FastMCP tools."""
        # Single operations
        self.server.tool()(self.get)
        self.server.tool()(self.set)
        self.server.tool()(self.delete)
        self.server.tool()(self.list)
        
        # Bulk operations
        self.server.tool()(self.mget)
        self.server.tool()(self.mset)
        self.server.tool()(self.scan)
    
    async def _get_client(self) -> redis.Redis:
        """Get a Redis client from the connection pool."""
        return redis.Redis(connection_pool=self.pool)
    
    async def get(self, key: str) -> Optional[str]:
        """
        Get the value of a key from Redis.

        Args:
            key: The Redis key to retrieve

        Returns:
            The value of the key, or None if the key does not exist
            
        Raises:
            RuntimeError: If Redis operation fails
        """
        async with await self._get_client() as client:
            try:
                return await client.get(key)
            except redis.RedisError as e:
                raise RuntimeError(f"Redis error: {str(e)}")
    
    async def set(
        self,
        key: str,
        value: str,
        ex: Optional[int] = None,
        nx: bool = False,
        xx: bool = False
    ) -> bool:
        """
        Set the value of a key in Redis.

        Args:
            key: The Redis key to set
            value: The value to set
            ex: Expiry time in seconds
            nx: Only set if the key does not exist
            xx: Only set if the key already exists

        Returns:
            True if the operation was successful, False otherwise
            
        Raises:
            RuntimeError: If Redis operation fails
        """
        if nx and xx:
            return False
        
        async with await self._get_client() as client:
            try:
                result = await client.set(key, value, ex=ex, nx=nx, xx=xx)
                return result is not None
            except redis.RedisError as e:
                raise RuntimeError(f"Redis error: {str(e)}")
    
    async def delete(self, keys: Union[str, List[str]]) -> int:
        """
        Delete one or more keys from Redis.

        Args:
            keys: The key or list of keys to delete

        Returns:
            The number of keys that were deleted
            
        Raises:
            RuntimeError: If Redis operation fails
        """
        if isinstance(keys, str):
            keys = [keys]
        
        if not keys:
            return 0
        
        async with await self._get_client() as client:
            try:
                return await client.delete(*keys)
            except redis.RedisError as e:
                raise RuntimeError(f"Redis error: {str(e)}")
    
    async def list(self, pattern: str = "*") -> List[str]:
        """
        List keys in Redis matching a pattern.

        Args:
            pattern: Pattern to match keys (default: "*")

        Returns:
            List of keys matching the pattern
            
        Raises:
            RuntimeError: If Redis operation fails
        """
        async with await self._get_client() as client:
            try:
                return await client.keys(pattern)
            except redis.RedisError as e:
                raise RuntimeError(f"Redis error: {str(e)}")
    
    async def mget(self, keys: List[str]) -> Dict[str, Optional[str]]:
        """
        Get the values of multiple keys from Redis in a single operation.

        Args:
            keys: List of Redis keys to retrieve

        Returns:
            Dictionary mapping keys to their values (None if key doesn't exist)
            
        Raises:
            RuntimeError: If Redis operation fails
        """
        if not keys:
            return {}
        
        async with await self._get_client() as client:
            try:
                values = await client.mget(keys)
                return {key: value for key, value in zip(keys, values)}
            except redis.RedisError as e:
                raise RuntimeError(f"Redis error: {str(e)}")
    
    async def mset(self, mapping: Dict[str, Any]) -> bool:
        """
        Set multiple key-value pairs in Redis in a single operation.

        Args:
            mapping: Dictionary of key-value pairs to set

        Returns:
            True if the operation was successful
            
        Raises:
            RuntimeError: If Redis operation fails
        """
        if not mapping:
            return False
        
        async with await self._get_client() as client:
            try:
                resp = await client.mset(mapping)
                return resp
            except redis.RedisError as e:
                raise RuntimeError(f"Redis error: {str(e)}")
    
    async def scan(
        self,
        pattern: str = "*",
        count: int = 100,
        cursor: int = 0
    ) -> Dict[str, Any]:
        """
        Scan keys in Redis matching a pattern without blocking the server.

        Args:
            pattern: Pattern to match keys (default: "*")
            count: Approximate number of keys to return per scan
            cursor: Cursor position for pagination (0 to start)

        Returns:
            Dictionary with cursor, keys, and completion status
            
        Raises:
            RuntimeError: If Redis operation fails
        """
        async with await self._get_client() as client:
            try:
                next_cursor, keys = await client.scan(
                    cursor=cursor,
                    match=pattern,
                    count=count
                )
                return {
                    "cursor": next_cursor,
                    "keys": keys,
                    "complete": next_cursor == 0
                }
            except redis.RedisError as e:
                raise RuntimeError(f"Redis error: {str(e)}")
    
    @staticmethod
    def _serialize_result(result: Any) -> Any:
        """Convert Redis result to JSON-serializable format."""
        if isinstance(result, bool):
            return result
        elif result is None:
            return None
        elif isinstance(result, (list, dict)):
            return result
        else:
            return str(result)
    
    async def close(self) -> None:
        """Close the connection pool and release resources."""
        await self.pool.disconnect()

    def run(self, *args, **kwargs):
        self.server.run(*args, **kwargs)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Redis MCP Server")
    parser.add_argument("--transport", default="stdio", help="MCP Transport type, stdio, sse, or streamable-http")
    parser.add_argument("--host", default="localhost", help="Redis host")
    parser.add_argument("--port", default=6379, type=int, help="Redis port")
    parser.add_argument("--db", type=int, default=0, help="Port to bind to for SSE transport")
    args = parser.parse_args()

    RedisMCPServer(host=args.host, port=args.port, db=args.db).run(args.transport)
