# Spec: History Formatter Testing

**Task**: Test history formatter  
**Duration**: 2 hours  
**Priority**: High  

## Overview
Create comprehensive unit tests for the `format_history_summary()` function in `flow.py` to ensure reliable history formatting across all action types and edge cases.

## Scope
Test the `format_history_summary()` function which:
- Formats action history for LLM context
- Handles multiple action types (read_file, edit_file, grep_search, list_dir, delete_file)
- Manages complex nested data structures
- Provides human-readable summaries

## Requirements

### Functional Requirements
- **FR1**: Test formatting for all supported action types
- **FR2**: Validate handling of empty and malformed history entries
- **FR3**: Test edge cases (missing fields, null values, unexpected data types)
- **FR4**: Verify output format consistency and readability
- **FR5**: Test performance with large history sets

### Non-Functional Requirements
- **NFR1**: Function should handle 100+ history entries efficiently
- **NFR2**: Output should be deterministic for identical inputs
- **NFR3**: Memory usage should remain constant regardless of history size
- **NFR4**: Function should never raise exceptions (graceful degradation)

## Technical Specifications

### Test File Structure
```
tests/
├── test_history_formatter.py    # Main test file
└── fixtures/
    └── history_samples.py       # Sample history data
```

### History Data Structure
The function processes history entries with this structure:
```python
{
    "tool": str,              # Action type
    "reason": str,            # Why the action was taken
    "params": dict,           # Action parameters
    "result": any,            # Action result (varies by tool)
    "timestamp": str          # ISO timestamp
}
```

### Expected Output Format
```
Action 1:
- Tool: read_file
- Reason: Reading configuration file
- Parameters:
  - target_file: config.yaml
- Result: Success
- Content: [file content]

Action 2:
- Tool: grep_search  
- Reason: Finding logger usage
- Parameters:
  - query: logger
  - include_pattern: *.py
- Result: Success
- Matches: 3
  1. main.py:15: logger = logging.getLogger()
  2. utils.py:23: logger.info("Processing complete")
  3. flow.py:45: logger.debug("Decision made")
```

## Implementation Tasks

### Task 1: Setup Test Infrastructure (30 minutes)
**File**: `tests/test_history_formatter.py`

#### Create Base Test Class
```python
import pytest
from flow import format_history_summary

class TestHistoryFormatter:
    """Test suite for format_history_summary function."""
    
    def test_empty_history(self):
        """Test formatting empty history."""
        result = format_history_summary([])
        assert result == "No previous actions."
    
    def test_none_history(self):
        """Test formatting None history."""
        result = format_history_summary(None)
        assert result == "No previous actions."
```

#### Create Sample Data Fixtures
**File**: `tests/fixtures/history_samples.py`
```python
# Sample history entries for different action types
SAMPLE_READ_FILE_SUCCESS = {
    "tool": "read_file",
    "reason": "Reading configuration file",
    "params": {"target_file": "config.yaml"},
    "result": {
        "success": True,
        "content": "database:\n  host: localhost\n  port: 5432"
    },
    "timestamp": "2024-01-01T10:00:00Z"
}

SAMPLE_GREP_SEARCH_SUCCESS = {
    "tool": "grep_search", 
    "reason": "Finding logger usage patterns",
    "params": {
        "query": "logger",
        "include_pattern": "*.py",
        "case_sensitive": False
    },
    "result": {
        "success": True,
        "matches": [
            {"file": "main.py", "line": 15, "content": "logger = logging.getLogger()"},
            {"file": "utils.py", "line": 23, "content": "logger.info('Processing')"}
        ]
    },
    "timestamp": "2024-01-01T10:01:00Z"
}

# Additional samples for all action types...
```

### Task 2: Test Action-Specific Formatting (60 minutes)

#### Test read_file Formatting
```python
def test_read_file_success_formatting(self):
    """Test formatting successful read_file action."""
    history = [SAMPLE_READ_FILE_SUCCESS]
    result = format_history_summary(history)
    
    assert "Action 1:" in result
    assert "Tool: read_file" in result
    assert "Reading configuration file" in result
    assert "target_file: config.yaml" in result
    assert "Result: Success" in result
    assert "database:" in result  # Content should be included

def test_read_file_failure_formatting(self):
    """Test formatting failed read_file action."""
    history = [{
        "tool": "read_file",
        "reason": "Reading missing file",
        "params": {"target_file": "missing.txt"},
        "result": {"success": False, "content": ""},
        "timestamp": "2024-01-01T10:00:00Z"
    }]
    
    result = format_history_summary(history)
    assert "Result: Failed" in result
    assert "Content:" not in result  # No content for failed reads
```

#### Test grep_search Formatting
```python
def test_grep_search_with_matches(self):
    """Test formatting grep_search with matches."""
    history = [SAMPLE_GREP_SEARCH_SUCCESS]
    result = format_history_summary(history)
    
    assert "Tool: grep_search" in result
    assert "Matches: 2" in result
    assert "1. main.py:15: logger = logging.getLogger()" in result
    assert "2. utils.py:23: logger.info('Processing')" in result

def test_grep_search_no_matches(self):
    """Test formatting grep_search with no matches."""
    history = [{
        "tool": "grep_search",
        "reason": "Searching for nonexistent pattern",
        "params": {"query": "nonexistent"},
        "result": {"success": True, "matches": []},
        "timestamp": "2024-01-01T10:00:00Z"
    }]
    
    result = format_history_summary(history)
    assert "Matches: 0" in result
```

#### Test edit_file Formatting
```python
def test_edit_file_success_formatting(self):
    """Test formatting successful edit_file action."""
    history = [{
        "tool": "edit_file",
        "reason": "Adding error handling",
        "params": {
            "target_file": "main.py",
            "instructions": "Add try-catch block",
            "code_edit": "try:\n    process()\nexcept Exception as e:\n    logger.error(e)"
        },
        "result": {
            "success": True,
            "operations": 3,
            "reasoning": "Added exception handling around process() call"
        },
        "timestamp": "2024-01-01T10:00:00Z"
    }]
    
    result = format_history_summary(history)
    assert "Operations: 3" in result
    assert "Reasoning: Added exception handling" in result
```

#### Test list_dir Formatting
```python
def test_list_dir_success_formatting(self):
    """Test formatting successful list_dir action."""
    tree_viz = """project/
├── main.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
└── tests/
    └── test_main.py"""
    
    history = [{
        "tool": "list_dir",
        "reason": "Exploring project structure",
        "params": {"relative_workspace_path": "."},
        "result": {
            "success": True,
            "tree_visualization": tree_viz
        },
        "timestamp": "2024-01-01T10:00:00Z"
    }]
    
    result = format_history_summary(history)
    assert "Directory structure:" in result
    assert "├── main.py" in result
    assert "└── helpers.py" in result
```

### Task 3: Test Edge Cases and Error Handling (30 minutes)

#### Test Malformed History Entries
```python
def test_missing_required_fields(self):
    """Test handling history entries with missing fields."""
    history = [{
        "tool": "read_file",
        # Missing reason, params, result
        "timestamp": "2024-01-01T10:00:00Z"
    }]
    
    result = format_history_summary(history)
    assert "Action 1:" in result
    assert "Tool: read_file" in result
    # Should handle gracefully without crashing

def test_unexpected_result_format(self):
    """Test handling unexpected result data types."""
    history = [{
        "tool": "read_file",
        "reason": "Test reason",
        "params": {"target_file": "test.txt"},
        "result": "Unexpected string result",  # Should be dict
        "timestamp": "2024-01-01T10:00:00Z"
    }]
    
    result = format_history_summary(history)
    assert "Result: Unexpected string result" in result

def test_null_values_handling(self):
    """Test handling null/None values in history."""
    history = [{
        "tool": None,
        "reason": None,
        "params": None,
        "result": None,
        "timestamp": None
    }]
    
    result = format_history_summary(history)
    # Should not crash, should handle gracefully
    assert "Action 1:" in result
```

#### Test Large History Sets
```python
def test_large_history_performance(self):
    """Test performance with large history sets."""
    import time
    
    # Create 100 history entries
    large_history = []
    for i in range(100):
        large_history.append({
            "tool": "read_file",
            "reason": f"Reading file {i}",
            "params": {"target_file": f"file_{i}.txt"},
            "result": {"success": True, "content": f"Content {i}"},
            "timestamp": f"2024-01-01T10:{i:02d}:00Z"
        })
    
    start_time = time.time()
    result = format_history_summary(large_history)
    execution_time = time.time() - start_time
    
    assert execution_time < 1.0  # Should complete in <1 second
    assert "Action 100:" in result
    assert len(result.split("Action")) == 101  # 100 actions + 1 for split
```

### Task 4: Test Output Format Validation (20 minutes)

#### Test Consistent Formatting
```python
def test_multiple_actions_formatting(self):
    """Test formatting multiple actions with consistent structure."""
    history = [
        SAMPLE_READ_FILE_SUCCESS,
        SAMPLE_GREP_SEARCH_SUCCESS
    ]
    
    result = format_history_summary(history)
    
    # Should have both actions
    assert "Action 1:" in result
    assert "Action 2:" in result
    
    # Should maintain consistent structure
    lines = result.split('\n')
    action_1_start = next(i for i, line in enumerate(lines) if "Action 1:" in line)
    action_2_start = next(i for i, line in enumerate(lines) if "Action 2:" in line)
    
    # Both actions should have similar structure
    assert any("- Tool:" in lines[action_1_start:action_2_start])
    assert any("- Reason:" in lines[action_1_start:action_2_start])

def test_parameter_formatting_consistency(self):
    """Test that parameters are formatted consistently."""
    history = [{
        "tool": "test_action",
        "reason": "Testing parameters",
        "params": {
            "simple_param": "value",
            "complex_param": {"nested": "data"},
            "list_param": ["item1", "item2"]
        },
        "result": {"success": True},
        "timestamp": "2024-01-01T10:00:00Z"
    }]
    
    result = format_history_summary(history)
    
    # All parameters should be indented consistently
    assert "  - simple_param: value" in result
    assert "  - complex_param:" in result
    assert "  - list_param:" in result
```

## Acceptance Criteria

### AC1: Core Functionality
- [ ] Empty history returns "No previous actions."
- [ ] Single action formatted correctly with all sections
- [ ] Multiple actions formatted with proper numbering
- [ ] All action types (read_file, edit_file, grep_search, list_dir, delete_file) formatted correctly

### AC2: Error Handling
- [ ] Missing fields handled gracefully (no exceptions)
- [ ] Null/None values don't cause crashes
- [ ] Unexpected data types handled appropriately
- [ ] Malformed history entries processed without errors

### AC3: Format Consistency
- [ ] Parameter indentation consistent across actions
- [ ] Result formatting consistent for success/failure cases
- [ ] Tool-specific details formatted correctly
- [ ] Action numbering sequential and correct

### AC4: Performance & Reliability
- [ ] Large history sets (100+ entries) processed in <1 second
- [ ] Memory usage remains stable with large inputs
- [ ] Output is deterministic for identical inputs
- [ ] No memory leaks with repeated calls

### AC5: Edge Cases
- [ ] Tree visualization formatting preserves structure
- [ ] Long content doesn't break formatting
- [ ] Special characters handled correctly
- [ ] Unicode content processed properly

## Success Metrics
- **Test Coverage**: 100% line and branch coverage for `format_history_summary()`
- **Performance**: <1 second for 100 history entries
- **Reliability**: No exceptions thrown for any input combination
- **Output Quality**: Human-readable, consistent formatting

## Dependencies
- Testing framework setup (Day 1, Task 1)
- Sample history data fixtures
- Performance measurement utilities

## Risks & Mitigations
- **Risk**: Complex nested data structures causing formatting issues
  - **Mitigation**: Test with deeply nested sample data
- **Risk**: Performance degradation with large histories
  - **Mitigation**: Include performance benchmarks in tests
- **Risk**: Unicode/encoding issues with file content
  - **Mitigation**: Test with various character encodings

## Validation Steps
1. Run `pytest tests/test_history_formatter.py -v --cov=flow`
2. Verify 100% coverage for `format_history_summary` function
3. Confirm all edge cases pass without exceptions
4. Validate output format with manual inspection of sample results