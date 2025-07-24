"""Smoke tests to validate testing framework setup."""

import pytest
import os
from pathlib import Path


def test_framework_setup():
    """Test that the testing framework is properly configured."""
    assert True


def test_fixtures_available(sample_shared_state, sample_history):
    """Test that fixtures are available and working."""
    assert sample_shared_state["user_query"] == "test query"
    assert len(sample_history) == 1
    assert sample_history[0]["tool"] == "read_file"


def test_temp_directory_fixture(temp_working_dir):
    """Test that temporary directory fixture works."""
    assert os.path.exists(temp_working_dir)
    assert os.path.isdir(temp_working_dir)
    
    # Test writing to temp directory
    test_file = Path(temp_working_dir) / "test.txt"
    test_file.write_text("test content")
    assert test_file.exists()
    assert test_file.read_text() == "test content"


def test_mock_llm_fixture(mock_llm_response):
    """Test that LLM mocking fixture works."""
    # Import here to avoid import issues if utils aren't ready
    try:
        from src.utils.call_llm import call_llm
        result = call_llm("test prompt")
        assert result == "Mocked LLM response"
        mock_llm_response.assert_called_once_with("test prompt")
    except ImportError:
        pytest.skip("Utils not available yet - expected during framework setup")


def test_project_structure():
    """Test that the project structure is as expected."""
    project_root = Path(__file__).parent.parent
    
    # Check main files exist
    assert (project_root / "src" / "main.py").exists()
    assert (project_root / "src" / "flow.py").exists()
    assert (project_root / "requirements.txt").exists()
    
    # Check utils directory exists
    assert (project_root / "src" / "utils").is_dir()
    
    # Check test structure
    assert (project_root / "tests").is_dir()
    assert (project_root / "tests" / "conftest.py").exists()
    assert (project_root / "pytest.ini").exists()


class TestClassBasedTests:
    """Test class-based test organization."""
    
    def test_class_method(self):
        """Test that class-based tests work."""
        assert hasattr(self, 'test_class_method')
    
    def test_with_fixture(self, sample_shared_state):
        """Test that fixtures work in class methods."""
        assert sample_shared_state is not None