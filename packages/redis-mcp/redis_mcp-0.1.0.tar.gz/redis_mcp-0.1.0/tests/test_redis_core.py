"""
Tests for Redis core operations.
"""

import os
import pytest
from fastmcp import Client
import json

from redis_mcp.redis_core import redis_core

# Test Redis configuration - use environment variables or defaults
TEST_REDIS_HOST = os.environ.get("TEST_REDIS_HOST", "localhost")
TEST_REDIS_PORT = int(os.environ.get("TEST_REDIS_PORT", "6379"))
TEST_REDIS_DB = int(os.environ.get("TEST_REDIS_DB", "0"))


async def _get_all_matching_keys(client, pattern):
    """Helper function to get all keys matching a pattern."""
    result = await client.call_tool(
        "redis_list",
        {
            "pattern": pattern,
            "host": TEST_REDIS_HOST,
            "port": TEST_REDIS_PORT,
            "db": TEST_REDIS_DB
        }
    )
    
    # Result is a TextContent with a string representation of the list
    # Convert it to an actual list
    if result and result[0].text:
        try:
            # Handle case where it might be a JSON string
            return json.loads(result[0].text)
        except json.JSONDecodeError:
            # Handle case where it's a string representation of a Python list
            text = result[0].text.strip("[]").replace("'", "\"")
            if text:
                return [item.strip() for item in text.split(",")]
            return []
    return []


@pytest.mark.asyncio
async def test_redis_get(redis_client):
    """Test the redis_get operation."""
    # First set a value using the Redis client directly
    await redis_client.set("test_get_key", "test_get_value")
    
    async with Client(redis_core) as client:
        # Retrieve the value using the tool
        result = await client.call_tool(
            "redis_get",
            {
                "key": "test_get_key",
                "host": TEST_REDIS_HOST,
                "port": TEST_REDIS_PORT,
                "db": TEST_REDIS_DB
            }
        )
        
        # Verify the value matches what we set
        assert result[0].text == "test_get_value"
        
        # Test non-existent key
        result = await client.call_tool(
            "redis_get",
            {
                "key": "test_nonexistent_key",
                "host": TEST_REDIS_HOST,
                "port": TEST_REDIS_PORT,
                "db": TEST_REDIS_DB
            }
        )
        
        # Should return None for non-existent key
        assert result[0].text is None or result[0].text == "None"


@pytest.mark.asyncio
async def test_redis_set(redis_client):
    """Test the redis_set operation."""
    async with Client(redis_core) as client:
        # Test basic set
        result = await client.call_tool(
            "redis_set",
            {
                "key": "test_set_key",
                "value": "test_value",
                "host": TEST_REDIS_HOST,
                "port": TEST_REDIS_PORT,
                "db": TEST_REDIS_DB
            }
        )
        
        # Should return True for success
        assert result[0].text == "True"
        
        # Verify the value was set correctly
        value = await redis_client.get("test_set_key")
        assert value == "test_value"
        
        # Test set with NX option (key doesn't exist)
        result = await client.call_tool(
            "redis_set",
            {
                "key": "test_set_nx_key",
                "value": "test_value",
                "nx": True,
                "host": TEST_REDIS_HOST,
                "port": TEST_REDIS_PORT,
                "db": TEST_REDIS_DB
            }
        )
        
        # Should return True for success
        assert result[0].text == "True"
        
        # Verify the value was set
        value = await redis_client.get("test_set_nx_key")
        assert value == "test_value"
        
        # Test set with NX option (key exists)
        result = await client.call_tool(
            "redis_set",
            {
                "key": "test_set_nx_key",
                "value": "updated_value",
                "nx": True,
                "host": TEST_REDIS_HOST,
                "port": TEST_REDIS_PORT,
                "db": TEST_REDIS_DB
            }
        )
        
        # Should return False for failure
        assert result[0].text == "False"
        
        # Verify the value was not updated
        value = await redis_client.get("test_set_nx_key")
        assert value == "test_value"


@pytest.mark.asyncio
async def test_redis_delete(redis_client):
    """Test the redis_delete operation."""
    # Set up some test keys
    await redis_client.set("test_delete_key1", "value1")
    await redis_client.set("test_delete_key2", "value2")
    
    async with Client(redis_core) as client:
        # Delete a single key
        result = await client.call_tool(
            "redis_delete",
            {
                "keys": "test_delete_key1",
                "host": TEST_REDIS_HOST,
                "port": TEST_REDIS_PORT,
                "db": TEST_REDIS_DB
            }
        )
        
        # Should return 1 for deleting 1 key
        assert result[0].text == "1"
        
        # Verify the key was deleted
        value = await redis_client.get("test_delete_key1")
        assert value is None
        
        # Test deleting multiple keys
        await redis_client.set("test_delete_multi1", "multi1")
        await redis_client.set("test_delete_multi2", "multi2")
        
        result = await client.call_tool(
            "redis_delete",
            {
                "keys": ["test_delete_multi1", "test_delete_multi2"],
                "host": TEST_REDIS_HOST,
                "port": TEST_REDIS_PORT,
                "db": TEST_REDIS_DB
            }
        )
        
        # Should return 2 for deleting 2 keys
        assert result[0].text == "2"
        
        # Verify the keys were deleted
        multi1 = await redis_client.get("test_delete_multi1")
        multi2 = await redis_client.get("test_delete_multi2")
        assert multi1 is None
        assert multi2 is None


@pytest.mark.asyncio
async def test_redis_list(redis_client):
    """Test the redis_list operation."""
    # Clean up any existing test keys
    keys = await redis_client.keys("test_list_*")
    if keys:
        await redis_client.delete(*keys)
    
    # Create some test keys
    await redis_client.set("test_list_key1", "value1")
    await redis_client.set("test_list_key2", "value2")
    await redis_client.set("test_list_abc", "abc")
    await redis_client.set("test_list_def", "def")
    
    async with Client(redis_core) as client:
        # Test listing with pattern matching all test keys
        result = await client.call_tool(
            "redis_list",
            {
                "pattern": "test_list_*",
                "host": TEST_REDIS_HOST,
                "port": TEST_REDIS_PORT,
                "db": TEST_REDIS_DB
            }
        )
        
        # Parse the response and verify it contains all test keys
        # Response format might be a string representation of a list
        keys = []
        if result and result[0].text:
            try:
                # Handle case where it might be a JSON string
                keys = json.loads(result[0].text)
            except json.JSONDecodeError:
                # Handle case where it's a string representation of a Python list
                text = result[0].text.strip("[]").replace("'", "\"")
                if text:
                    keys = [item.strip() for item in text.split(",")]
        
        assert len(keys) == 4
        assert "test_list_key1" in keys
        assert "test_list_key2" in keys
        assert "test_list_abc" in keys
        assert "test_list_def" in keys
        
        # Test listing with more specific pattern
        result = await client.call_tool(
            "redis_list",
            {
                "pattern": "test_list_a*",
                "host": TEST_REDIS_HOST,
                "port": TEST_REDIS_PORT,
                "db": TEST_REDIS_DB
            }
        )
        
        # Parse the response
        keys = []
        if result and result[0].text:
            try:
                keys = json.loads(result[0].text)
            except json.JSONDecodeError:
                text = result[0].text.strip("[]").replace("'", "\"")
                if text:
                    keys = [item.strip() for item in text.split(",")]
        
        assert len(keys) == 1
        assert "test_list_abc" in keys
