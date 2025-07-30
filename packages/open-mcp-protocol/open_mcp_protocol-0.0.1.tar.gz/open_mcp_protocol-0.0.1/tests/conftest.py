# tests/conftest.py
"""Pytest configuration and fixtures."""

import asyncio
import pytest
from unittest.mock import Mock, AsyncMock
from typing import Dict, Any, List

from open_mcp.models.base import Tool, Resource, Prompt


@pytest.fixture
def sample_tool():
    """Sample tool for testing."""
    return Tool(
        name="calculator",
        description="Basic calculator tool",
        parameters={
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["operation", "a", "b"]
        }
    )


@pytest.fixture
def sample_resource():
    """Sample resource for testing."""
    return Resource(
        uri="file://test.json",
        name="test_data",
        description="Test data file",
        mime_type="application/json"
    )


@pytest.fixture
def sample_prompt():
    """Sample prompt for testing."""
    return Prompt(
        name="summarize",
        description="Summarize text",
        arguments=[
            {"name": "text", "type": "string", "required": True},
            {"name": "max_words", "type": "integer", "required": False}
        ]
    )


@pytest.fixture
def mock_httpx_client():
    """Mock HTTPX client for testing."""
    client = AsyncMock()
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"result": {"status": "ok"}}
    response.raise_for_status.return_value = None
    client.post.return_value = response
    return client


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()