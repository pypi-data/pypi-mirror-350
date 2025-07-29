"""
Tests to verify that required modules are installed and available.
"""

import pytest


def test_redis_module_installed():
    """Test that the redis module is installed."""
    try:
        import redis
        assert redis.__version__, "Redis version should be available"
    except ImportError:
        pytest.fail("Redis module is not installed")


def test_fastmcp_module_installed():
    """Test that the FastMCP module is installed."""
    try:
        import fastmcp
        assert fastmcp.__version__, "FastMCP version should be available"
    except ImportError:
        pytest.fail("FastMCP module is not installed")


def test_redis_mcp_module_importable():
    """Test that the redis_mcp module is importable."""
    try:
        import redis_mcp
        assert redis_mcp.__version__ == "0.1.0", "Version should be 0.1.0"
    except ImportError:
        pytest.fail("redis_mcp module is not importable")


def test_redis_core_importable():
    """Test that the redis_core module is importable."""
    try:
        from redis_mcp import redis_core
        assert hasattr(redis_core, "redis_core"), "redis_core.redis_core should exist"
    except ImportError:
        pytest.fail("redis_core module is not importable")


def test_task_management_importable():
    """Test that the task_management module is importable."""
    try:
        from redis_mcp import task_management
        assert hasattr(task_management, "task_management"), "task_management.task_management should exist"
    except ImportError:
        pytest.fail("task_management module is not importable")


def test_server_importable():
    """Test that the server module is importable."""
    try:
        from redis_mcp import server
        assert hasattr(server, "mcp"), "server.mcp should exist"
    except ImportError:
        pytest.fail("server module is not importable")
