import fakeredis.aioredis
import unittest.mock
from redis_mcp import redis_core
import pytest

@pytest.fixture(scope="function")
async def redis_client():
    # Create a fakeredis client
    fake_redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    
    # Patch the get_redis_client function to use our fake Redis
    async def mock_get_redis_client(*args, **kwargs):
        return fake_redis
    
    # Apply the patch
    with unittest.mock.patch('redis_mcp.redis_core.get_redis_client', mock_get_redis_client):
        yield fake_redis
        
        # Clean up
        await fake_redis.flushall()
        await fake_redis.close()
