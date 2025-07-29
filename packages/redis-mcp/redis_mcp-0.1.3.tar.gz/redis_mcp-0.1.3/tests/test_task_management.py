"""
Tests for task management operations.
"""

import pytest
from fastmcp import Client

from redis_mcp.task_management import task_management


@pytest.mark.asyncio
async def test_create_project():
    """Test the create_project operation."""
    async with Client(task_management) as client:
        with pytest.raises(NotImplementedError):
            await client.call_tool(
                "create_project", 
                {
                    "project_id": "test_project", 
                    "title": "Test Project", 
                    "description": "A test project"
                }
            )


@pytest.mark.asyncio
async def test_add_task():
    """Test the add_task operation."""
    async with Client(task_management) as client:
        with pytest.raises(NotImplementedError):
            await client.call_tool(
                "add_task", 
                {
                    "project_id": "test_project", 
                    "task_id": "test_task", 
                    "title": "Test Task", 
                    "description": "A test task"
                }
            )


@pytest.mark.asyncio
async def test_start_task():
    """Test the start_task operation."""
    async with Client(task_management) as client:
        with pytest.raises(NotImplementedError):
            await client.call_tool(
                "start_task", 
                {
                    "project_id": "test_project", 
                    "task_id": "test_task"
                }
            )


@pytest.mark.asyncio
async def test_complete_task():
    """Test the complete_task operation."""
    async with Client(task_management) as client:
        with pytest.raises(NotImplementedError):
            await client.call_tool(
                "complete_task", 
                {
                    "project_id": "test_project", 
                    "task_id": "test_task", 
                    "notes": "Task completed"
                }
            )


@pytest.mark.asyncio
async def test_get_project_tasks():
    """Test the get_project_tasks operation."""
    async with Client(task_management) as client:
        with pytest.raises(NotImplementedError):
            await client.call_tool(
                "get_project_tasks", 
                {
                    "project_id": "test_project"
                }
            )
