import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

@pytest.fixture
def temp_working_dir():
    """Create a temporary working directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def sample_shared_state():
    """Provide a standard shared state for testing."""
    return {
        "user_query": "test query",
        "working_dir": "/tmp/test",
        "history": [],
        "response": None
    }

@pytest.fixture
def mock_llm_response():
    """Mock LLM API responses."""
    with patch('src.utils.call_llm.call_llm') as mock:
        mock.return_value = "Mocked LLM response"
        yield mock

@pytest.fixture
def sample_history():
    """Provide sample action history for testing."""
    return [
        {
            "tool": "read_file",
            "reason": "Reading configuration file",
            "params": {"target_file": "config.yaml"},
            "result": {"success": True, "content": "sample: content"},
            "timestamp": "2024-01-01T10:00:00"
        }
    ]