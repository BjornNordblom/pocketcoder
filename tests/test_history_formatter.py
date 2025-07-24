"""Tests for the format_history_summary function."""

import pytest
from src.flow import format_history_summary


class TestFormatHistorySummary:
    """Test the format_history_summary function with various scenarios."""
    
    def test_empty_history(self):
        """Test formatting empty history."""
        result = format_history_summary([])
        assert result == "No previous actions."
    
    def test_single_read_file_action(self):
        """Test formatting a single read_file action."""
        history = [
            {
                "tool": "read_file",
                "reason": "Reading configuration file",
                "params": {"target_file": "config.yaml"},
                "result": {
                    "success": True,
                    "content": "app:\n  name: test\n  version: 1.0"
                },
                "timestamp": "2024-01-01T10:00:00"
            }
        ]
        
        result = format_history_summary(history)
        
        assert "Action 1:" in result
        assert "Tool: read_file" in result
        assert "Reason: Reading configuration file" in result
        assert "target_file: config.yaml" in result
        assert "Result: Success" in result
        assert "app:\n  name: test\n  version: 1.0" in result
    
    def test_failed_action(self):
        """Test formatting a failed action."""
        history = [
            {
                "tool": "read_file",
                "reason": "Reading missing file",
                "params": {"target_file": "missing.txt"},
                "result": {
                    "success": False,
                    "error": "File not found"
                },
                "timestamp": "2024-01-01T10:00:00"
            }
        ]
        
        result = format_history_summary(history)
        
        assert "Action 1:" in result
        assert "Tool: read_file" in result
        assert "Result: Failed" in result
    
    def test_grep_search_action(self):
        """Test formatting a grep_search action with matches."""
        history = [
            {
                "tool": "grep_search",
                "reason": "Searching for function definitions",
                "params": {"pattern": "def main", "directory": "."},
                "result": {
                    "success": True,
                    "matches": [
                        {
                            "file": "main.py",
                            "line": 10,
                            "content": "def main():"
                        },
                        {
                            "file": "utils/helper.py",
                            "line": 25,
                            "content": "def main_helper():"
                        }
                    ]
                },
                "timestamp": "2024-01-01T10:00:00"
            }
        ]
        
        result = format_history_summary(history)
        
        assert "Tool: grep_search" in result
        assert "Matches: 2" in result
        assert "main.py:10: def main():" in result
        assert "utils/helper.py:25: def main_helper():" in result
    
    def test_edit_file_action(self):
        """Test formatting an edit_file action."""
        history = [
            {
                "tool": "edit_file",
                "reason": "Adding new function",
                "params": {"target_file": "utils.py"},
                "result": {
                    "success": True,
                    "operations": 3,
                    "reasoning": "Added helper function for data processing"
                },
                "timestamp": "2024-01-01T10:00:00"
            }
        ]
        
        result = format_history_summary(history)
        
        assert "Tool: edit_file" in result
        assert "Operations: 3" in result
        assert "Reasoning: Added helper function for data processing" in result
    
    def test_list_dir_action(self):
        """Test formatting a list_dir action."""
        history = [
            {
                "tool": "list_dir",
                "reason": "Exploring project structure",
                "params": {"directory": "./src"},
                "result": {
                    "success": True,
                    "tree_visualization": "src/\n├── main.py\n├── utils.py\n└── config/\n    └── settings.yaml"
                },
                "timestamp": "2024-01-01T10:00:00"
            }
        ]
        
        result = format_history_summary(history)
        
        assert "Tool: list_dir" in result
        assert "Directory structure:" in result
        assert "src/" in result
        assert "├── main.py" in result
        assert "└── config/" in result
    
    def test_list_dir_empty_tree(self):
        """Test formatting list_dir with empty or invalid tree."""
        history = [
            {
                "tool": "list_dir",
                "reason": "Exploring empty directory",
                "params": {"directory": "./empty"},
                "result": {
                    "success": True,
                    "tree_visualization": ""
                },
                "timestamp": "2024-01-01T10:00:00"
            }
        ]
        
        result = format_history_summary(history)
        
        assert "Tool: list_dir" in result
        assert "Directory structure:" in result
        assert "(Empty or inaccessible directory)" in result
    
    def test_multiple_actions(self):
        """Test formatting multiple actions."""
        history = [
            {
                "tool": "read_file",
                "reason": "Reading main file",
                "params": {"target_file": "main.py"},
                "result": {"success": True, "content": "print('hello')"},
                "timestamp": "2024-01-01T10:00:00"
            },
            {
                "tool": "edit_file",
                "reason": "Adding comments",
                "params": {"target_file": "main.py"},
                "result": {"success": True, "operations": 1},
                "timestamp": "2024-01-01T10:01:00"
            }
        ]
        
        result = format_history_summary(history)
        
        assert "Action 1:" in result
        assert "Action 2:" in result
        assert result.count("Tool:") == 2
    
    def test_action_without_params(self):
        """Test formatting action without parameters."""
        history = [
            {
                "tool": "custom_action",
                "reason": "Performing custom operation",
                "result": {"success": True},
                "timestamp": "2024-01-01T10:00:00"
            }
        ]
        
        result = format_history_summary(history)
        
        assert "Tool: custom_action" in result
        assert "Reason: Performing custom operation" in result
        assert "Parameters:" not in result
    
    def test_action_with_non_dict_result(self):
        """Test formatting action with non-dictionary result."""
        history = [
            {
                "tool": "simple_action",
                "reason": "Simple operation",
                "params": {"param": "value"},
                "result": "Simple string result",
                "timestamp": "2024-01-01T10:00:00"
            }
        ]
        
        result = format_history_summary(history)
        
        assert "Tool: simple_action" in result
        assert "Result: Simple string result" in result
    
    def test_malformed_history_entry(self):
        """Test handling malformed history entries."""
        history = [
            {
                "tool": "broken_action",
                "reason": "This entry is missing result",
                "params": {"test": "value"}
                # Missing result field
            }
        ]
        
        result = format_history_summary(history)
        
        # Should not crash and should include basic info
        assert "Tool: broken_action" in result
        assert "Reason: This entry is missing result" in result
    
    def test_large_history_performance(self):
        """Test performance with large history datasets."""
        # Create a large history with 100 entries
        history = []
        for i in range(100):
            history.append({
                "tool": f"action_{i}",
                "reason": f"Performing action {i}",
                "params": {"index": i},
                "result": {"success": True, "data": f"result_{i}"},
                "timestamp": f"2024-01-01T10:{i:02d}:00"
            })
        
        # This should complete quickly without issues
        result = format_history_summary(history)
        
        assert "Action 1:" in result
        assert "Action 100:" in result
        assert result.count("Tool:") == 100