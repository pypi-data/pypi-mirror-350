"""
Tests for the main server.
"""

import pytest
from fastmcp import Client

from redis_mcp.server import mcp


@pytest.mark.asyncio
async def test_server_info():
    """Test the server_info operation."""
    async with Client(mcp) as client:
        result = await client.call_tool("server_info", {})
        assert result[0].text is not None
        data = eval(result[0].text)  # Convert string representation to dict
        assert isinstance(data, dict)
        assert data["name"] == "Redis MCP Server"
        assert data["version"] == "0.1.0"
        assert "redis_operations" in data["components"]
        assert "task_management" in data["components"]
        assert "stdio" in data["transports"]
        assert "sse" in data["transports"]


@pytest.mark.asyncio
async def test_mounted_redis_get():
    """Test the mounted redis_get operation."""
    async with Client(mcp) as client:
        with pytest.raises(NotImplementedError):
            await client.call_tool("redis_redis_get", {"key": "test_key"})


@pytest.mark.asyncio
async def test_mounted_redis_get_implemented():
    """Test the mounted redis_get operation when implemented."""
    # This test will be skipped until the implementation is ready
    pytest.skip("Implementation not ready")
    
    async with Client(mcp) as client:
        # Test the mounted redis_get through the main server
        await client.call_tool("redis_redis_set", {"key": "mounted_test_key", "value": "mounted_test_value"})
        result = await client.call_tool("redis_redis_get", {"key": "mounted_test_key"})
        assert result[0].text == "mounted_test_value", "Mounted redis_get should return correct value"


@pytest.mark.asyncio
async def test_mounted_create_project():
    """Test the mounted create_project operation."""
    async with Client(mcp) as client:
        with pytest.raises(NotImplementedError):
            await client.call_tool(
                "task_create_project", 
                {
                    "project_id": "test_project", 
                    "title": "Test Project", 
                    "description": "A test project"
                }
            )


@pytest.mark.asyncio
async def test_mounted_create_project_implemented():
    """Test the mounted create_project operation when implemented."""
    # This test will be skipped until the implementation is ready
    pytest.skip("Implementation not ready")
    
    async with Client(mcp) as client:
        # Test the mounted create_project through the main server
        result = await client.call_tool(
            "task_create_project", 
            {
                "project_id": "mounted_test_project", 
                "title": "Mounted Test Project", 
                "description": "A test project created through mounting"
            }
        )
        
        # Verify project was created by getting project tasks
        result = await client.call_tool(
            "task_get_project_tasks", 
            {
                "project_id": "mounted_test_project"
            }
        )
        
        assert result[0].text is not None, "Should return project tasks"
        data = eval(result[0].text)
        assert isinstance(data, dict), "Should return a dictionary"
        assert data.get("pending", []) is not None, "Should have pending tasks list"


@pytest.mark.asyncio
async def test_cross_component_interaction():
    """Test interaction between mounted components."""
    # This test will be skipped until the implementation is ready
    pytest.skip("Implementation not ready")
    
    async with Client(mcp) as client:
        # Create a project
        await client.call_tool(
            "task_create_project", 
            {
                "project_id": "cross_test_project", 
                "title": "Cross-Component Test", 
                "description": "Testing cross-component interaction"
            }
        )
        
        # Use Redis to store and retrieve project metadata
        await client.call_tool(
            "redis_redis_set", 
            {
                "key": "project:cross_test_project:priority", 
                "value": "high"
            }
        )
        
        result = await client.call_tool(
            "redis_redis_get", 
            {
                "key": "project:cross_test_project:priority"
            }
        )
        
        assert result[0].text == "high", "Should store and retrieve cross-component data"
