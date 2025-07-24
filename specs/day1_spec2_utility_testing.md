# Spec: Utility Function Testing

**Task**: Test utility functions  
**Duration**: 4 hours  
**Priority**: High  

## Overview
Create comprehensive unit tests for all utility functions in the `utils/` directory to ensure reliability and enable safe refactoring.

## Scope
Test the following utility modules:
- `utils/call_llm.py` - LLM API integration
- `utils/read_file.py` - File reading operations  
- `utils/replace_file.py` - File content replacement
- `utils/search_ops.py` - Grep-like search functionality
- `utils/dir_ops.py` - Directory listing and tree visualization
- `utils/delete_file.py` - File deletion operations

## Requirements

### Functional Requirements
- **FR1**: Test all public functions with valid inputs
- **FR2**: Test error handling for invalid inputs and edge cases
- **FR3**: Mock external dependencies (LLM APIs, file system)
- **FR4**: Validate return value types and structures
- **FR5**: Test file system operations with temporary files

### Non-Functional Requirements
- **NFR1**: Achieve 95%+ code coverage for utility functions
- **NFR2**: All tests must be isolated (no shared state)
- **NFR3**: Tests should complete in <10 seconds total
- **NFR4**: Mock all external API calls and file system dependencies

## Technical Specifications

### Test Files Structure
```
tests/test_utils/
├── test_call_llm.py         # LLM API testing
├── test_file_operations.py  # read_file, replace_file, delete_file
├── test_search_ops.py       # grep_search functionality
└── test_dir_ops.py          # list_dir and tree operations
```

### Testing Patterns

#### LLM API Testing (`test_call_llm.py`)
```python
import pytest
from unittest.mock import patch, Mock
from utils.call_llm import call_llm

class TestCallLLM:
    @patch('utils.call_llm.anthropic.Client')
    def test_successful_llm_call(self, mock_client):
        # Test successful API call
        pass
        
    @patch('utils.call_llm.anthropic.Client')
    def test_api_error_handling(self, mock_client):
        # Test API failures and retries
        pass
        
    def test_prompt_formatting(self):
        # Test prompt structure and encoding
        pass
```

#### File Operations Testing (`test_file_operations.py`)
```python
import pytest
import tempfile
import os
from pathlib import Path
from utils.read_file import read_file
from utils.replace_file import replace_file
from utils.delete_file import delete_file

class TestFileOperations:
    def test_read_existing_file(self, temp_working_dir):
        # Test reading valid files
        pass
        
    def test_read_nonexistent_file(self):
        # Test error handling for missing files
        pass
        
    def test_replace_file_content(self, temp_working_dir):
        # Test line-based content replacement
        pass
        
    def test_delete_file_success(self, temp_working_dir):
        # Test successful file deletion
        pass
```

## Implementation Tasks

### Task 1: LLM API Testing (1 hour)
**File**: `tests/test_utils/test_call_llm.py`

#### Test Cases
1. **Successful API Call**
   - Mock Anthropic client response
   - Verify correct prompt formatting
   - Validate response parsing

2. **API Error Handling**
   - Mock API failures (network, rate limits, auth)
   - Test retry mechanisms
   - Verify error propagation

3. **Input Validation**
   - Test with empty prompts
   - Test with oversized prompts
   - Test with special characters

#### Implementation Details
```python
@pytest.fixture
def mock_anthropic_response():
    """Mock successful Anthropic API response."""
    mock_response = Mock()
    mock_response.content = [Mock()]
    mock_response.content[0].text = "Test response"
    return mock_response

def test_call_llm_success(mock_anthropic_response):
    with patch('utils.call_llm.anthropic.Client') as mock_client:
        mock_client.return_value.messages.create.return_value = mock_anthropic_response
        
        result = call_llm("Test prompt")
        
        assert result == "Test response"
        mock_client.return_value.messages.create.assert_called_once()
```

### Task 2: File Operations Testing (1.5 hours)
**File**: `tests/test_utils/test_file_operations.py`

#### Test Cases
1. **read_file() Tests**
   - Read existing file successfully
   - Handle non-existent files
   - Handle permission errors
   - Read empty files
   - Read binary files (error case)

2. **replace_file() Tests**
   - Replace single line
   - Replace multiple lines
   - Replace with empty content
   - Handle invalid line numbers
   - Handle file write permissions

3. **delete_file() Tests**
   - Delete existing file
   - Handle non-existent files
   - Handle permission errors
   - Verify file is actually deleted

#### Implementation Details
```python
@pytest.fixture
def sample_file_content():
    return """line 1
line 2
line 3
line 4
line 5"""

def test_read_file_success(temp_working_dir, sample_file_content):
    file_path = os.path.join(temp_working_dir, "test.txt")
    with open(file_path, 'w') as f:
        f.write(sample_file_content)
    
    content, success = read_file(file_path)
    
    assert success is True
    assert content == sample_file_content

def test_replace_file_single_line(temp_working_dir, sample_file_content):
    file_path = os.path.join(temp_working_dir, "test.txt")
    with open(file_path, 'w') as f:
        f.write(sample_file_content)
    
    success, message = replace_file(file_path, 2, 2, "new line 2")
    
    assert success is True
    with open(file_path, 'r') as f:
        updated_content = f.read()
    assert "new line 2" in updated_content
```

### Task 3: Search Operations Testing (1 hour)
**File**: `tests/test_utils/test_search_ops.py`

#### Test Cases
1. **grep_search() Tests**
   - Search with simple string pattern
   - Search with regex patterns
   - Case sensitive/insensitive searches
   - File pattern inclusion/exclusion
   - Handle empty results
   - Handle search errors

#### Implementation Details
```python
@pytest.fixture
def sample_project_structure(temp_working_dir):
    """Create a sample project with multiple files for searching."""
    files = {
        "main.py": "import logging\nlogger = logging.getLogger()\nprint('Hello')",
        "utils.py": "def helper():\n    logger.info('Helper called')\n    return True",
        "test.txt": "This is a test file\nwith some content"
    }
    
    for filename, content in files.items():
        file_path = os.path.join(temp_working_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return temp_working_dir

def test_grep_search_basic(sample_project_structure):
    success, matches = grep_search(
        query="logger",
        working_dir=sample_project_structure
    )
    
    assert success is True
    assert len(matches) >= 2  # Should find in main.py and utils.py
    assert all("logger" in match["content"] for match in matches)
```

### Task 4: Directory Operations Testing (30 minutes)
**File**: `tests/test_utils/test_dir_ops.py`

#### Test Cases
1. **list_dir() Tests**
   - List directory with files and subdirectories
   - Handle non-existent directories
   - Handle permission errors
   - Generate proper tree visualization
   - Handle empty directories

#### Implementation Details
```python
def test_list_dir_with_structure(temp_working_dir):
    # Create nested directory structure
    os.makedirs(os.path.join(temp_working_dir, "subdir"))
    with open(os.path.join(temp_working_dir, "file1.txt"), 'w') as f:
        f.write("content")
    with open(os.path.join(temp_working_dir, "subdir", "file2.py"), 'w') as f:
        f.write("print('hello')")
    
    success, tree_str = list_dir(temp_working_dir)
    
    assert success is True
    assert "file1.txt" in tree_str
    assert "subdir" in tree_str
    assert "file2.py" in tree_str
```

## Acceptance Criteria

### AC1: LLM API Testing
- [ ] All API call scenarios tested with mocks
- [ ] Error handling verified for common failure modes
- [ ] Input validation covers edge cases
- [ ] No actual API calls made during testing

### AC2: File Operations Testing
- [ ] All file operations tested with temporary files
- [ ] Error cases handled (permissions, missing files)
- [ ] File system state properly isolated between tests
- [ ] Return value formats validated

### AC3: Search Operations Testing
- [ ] Search functionality tested with sample projects
- [ ] Pattern matching validated (strings and regex)
- [ ] File filtering options tested
- [ ] Performance acceptable for typical codebases

### AC4: Directory Operations Testing
- [ ] Tree visualization format validated
- [ ] Nested directory structures handled correctly
- [ ] Error cases covered (permissions, missing dirs)
- [ ] Output format consistent and parseable

### AC5: Overall Test Quality
- [ ] 95%+ code coverage for all utility functions
- [ ] All tests pass consistently
- [ ] Tests complete in <10 seconds
- [ ] No external dependencies (mocked)

## Success Metrics
- **Code Coverage**: 95%+ for utils/ directory
- **Test Execution Time**: <10 seconds for all utility tests
- **Test Reliability**: 100% pass rate across 10 consecutive runs
- **Error Coverage**: All error paths tested

## Dependencies
- Testing framework setup (Day 1, Task 1)
- Temporary file fixtures
- Mock objects for external APIs
- Sample project structures for testing

## Risks & Mitigations
- **Risk**: File system tests interfering with each other
  - **Mitigation**: Use isolated temporary directories per test
- **Risk**: Mock objects not matching real API behavior
  - **Mitigation**: Keep mocks simple, validate against real API docs
- **Risk**: Search tests too slow with large file sets
  - **Mitigation**: Use small, focused test data sets

## Validation Steps
1. Run `pytest tests/test_utils/ -v --cov=utils` 
2. Verify coverage report shows 95%+ for all utility modules
3. Confirm all tests pass without external dependencies
4. Validate test isolation by running tests in random order