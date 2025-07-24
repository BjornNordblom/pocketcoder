"""Tests for the read_file utility function."""

import pytest
import os
import tempfile
from pathlib import Path
from utils.read_file import read_file


class TestReadFile:
    """Test the read_file function with various scenarios."""
    
    @pytest.fixture
    def sample_file(self):
        """Create a temporary file with sample content."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            content = """Line 1: First line
Line 2: Second line
Line 3: Third line
Line 4: Fourth line
Line 5: Fifth line
"""
            f.write(content)
            f.flush()
            yield f.name
        # Cleanup
        os.unlink(f.name)
    
    @pytest.fixture
    def empty_file(self):
        """Create an empty temporary file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            yield f.name
        # Cleanup
        os.unlink(f.name)
    
    @pytest.fixture
    def large_file(self):
        """Create a large file with many lines."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            for i in range(300):
                f.write(f"Line {i+1}: This is line number {i+1}\n")
            f.flush()
            yield f.name
        # Cleanup
        os.unlink(f.name)
    
    def test_read_entire_file_default(self, sample_file):
        """Test reading entire file with default parameters."""
        content, success = read_file(sample_file)
        
        assert success is True
        assert "1: Line 1: First line" in content
        assert "5: Line 5: Fifth line" in content
        assert content.count('\n') == 5  # Should have line numbers
    
    def test_read_entire_file_explicit(self, sample_file):
        """Test reading entire file with explicit parameter."""
        content, success = read_file(sample_file, should_read_entire_file=True)
        
        assert success is True
        assert "1: Line 1: First line" in content
        assert "5: Line 5: Fifth line" in content
    
    def test_read_specific_lines(self, sample_file):
        """Test reading specific line range."""
        content, success = read_file(sample_file, 2, 4)
        
        assert success is True
        assert "2: Line 2: Second line" in content
        assert "3: Line 3: Third line" in content
        assert "4: Line 4: Fourth line" in content
        assert "1: Line 1: First line" not in content
        assert "5: Line 5: Fifth line" not in content
    
    def test_read_single_line(self, sample_file):
        """Test reading a single line."""
        content, success = read_file(sample_file, 3, 3)
        
        assert success is True
        assert content == "3: Line 3: Third line\n"
    
    def test_read_nonexistent_file(self):
        """Test reading a file that doesn't exist."""
        content, success = read_file("nonexistent_file.txt")
        
        assert success is False
        assert "does not exist" in content
    
    def test_read_empty_file(self, empty_file):
        """Test reading an empty file."""
        content, success = read_file(empty_file)
        
        assert success is True
        assert content == ""
    
    def test_invalid_start_line(self, sample_file):
        """Test with invalid start line (less than 1)."""
        content, success = read_file(sample_file, 0, 3)
        
        assert success is False
        assert "must be at least 1" in content
    
    def test_invalid_line_range(self, sample_file):
        """Test with end line less than start line."""
        content, success = read_file(sample_file, 4, 2)
        
        assert success is False
        assert "must be >= start_line_one_indexed" in content
    
    def test_line_range_too_large(self, large_file):
        """Test reading more than 250 lines at once."""
        content, success = read_file(large_file, 1, 251)
        
        assert success is False
        assert "Cannot read more than 250 lines" in content
    
    def test_start_line_exceeds_file_length(self, sample_file):
        """Test with start line beyond file length."""
        content, success = read_file(sample_file, 10, 15)
        
        assert success is False
        assert "exceeds file length" in content
    
    def test_end_line_exceeds_file_length(self, sample_file):
        """Test with end line beyond file length (should be clamped)."""
        content, success = read_file(sample_file, 3, 10)
        
        assert success is True
        assert "3: Line 3: Third line" in content
        assert "4: Line 4: Fourth line" in content
        assert "5: Line 5: Fifth line" in content
        assert content.count('\n') == 3  # Lines 3, 4, 5
    
    def test_read_lines_at_file_boundary(self, sample_file):
        """Test reading lines at the exact file boundary."""
        content, success = read_file(sample_file, 5, 5)
        
        assert success is True
        assert content == "5: Line 5: Fifth line\n"
    
    def test_none_parameters_read_entire_file(self, sample_file):
        """Test that None parameters result in reading entire file."""
        content1, success1 = read_file(sample_file, None, None)
        content2, success2 = read_file(sample_file, should_read_entire_file=True)
        
        assert success1 is True
        assert success2 is True
        assert content1 == content2
    
    def test_partial_none_parameters(self, sample_file):
        """Test with one parameter None (should read entire file)."""
        content, success = read_file(sample_file, 2, None)
        
        assert success is True
        assert "1: Line 1: First line" in content  # Should read entire file
        assert "5: Line 5: Fifth line" in content
    
    def test_unicode_content(self):
        """Test reading file with unicode content."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            unicode_content = "Line 1: Hello 世界\nLine 2: Café ñiño\nLine 3: 🚀 emoji"
            f.write(unicode_content)
            f.flush()
            
            try:
                content, success = read_file(f.name)
                
                assert success is True
                assert "世界" in content
                assert "Café ñiño" in content
                assert "🚀 emoji" in content
                assert "1: Line 1: Hello 世界" in content
            finally:
                os.unlink(f.name)
    
    def test_file_with_no_newline_at_end(self):
        """Test reading file that doesn't end with newline."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Line without newline")
            f.flush()
            
            try:
                content, success = read_file(f.name)
                
                assert success is True
                assert content == "1: Line without newline"
            finally:
                os.unlink(f.name)
    
    def test_relative_path(self, sample_file):
        """Test reading with relative path."""
        # Create a symlink in current directory for testing
        relative_name = "test_relative_file.txt"
        if os.path.exists(relative_name):
            os.unlink(relative_name)
        
        try:
            os.symlink(sample_file, relative_name)
            content, success = read_file(relative_name)
            
            assert success is True
            assert "1: Line 1: First line" in content
        finally:
            if os.path.exists(relative_name):
                os.unlink(relative_name)
    
    def test_absolute_path(self, sample_file):
        """Test reading with absolute path."""
        absolute_path = os.path.abspath(sample_file)
        content, success = read_file(absolute_path)
        
        assert success is True
        assert "1: Line 1: First line" in content
    
    def test_line_numbering_accuracy(self, sample_file):
        """Test that line numbering is accurate."""
        content, success = read_file(sample_file, 2, 4)
        
        assert success is True
        lines = content.strip().split('\n')
        assert len(lines) == 3
        assert lines[0].startswith("2: ")
        assert lines[1].startswith("3: ")
        assert lines[2].startswith("4: ")
    
    def test_error_handling_permission_denied(self):
        """Test handling of permission denied errors."""
        # This test might not work on all systems
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("test content")
            f.flush()
            
            try:
                # Remove read permissions
                os.chmod(f.name, 0o000)
                content, success = read_file(f.name)
                
                assert success is False
                assert "Error reading file" in content
            except OSError:
                # If we can't change permissions, skip this test
                pytest.skip("Cannot test permission denied on this system")
            finally:
                # Restore permissions for cleanup
                os.chmod(f.name, 0o644)
                os.unlink(f.name)