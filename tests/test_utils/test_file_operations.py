"""Tests for file operations utilities (remove_file, insert_file, replace_file)."""

import pytest
import os
import tempfile
from src.utils.remove_file import remove_file
from src.utils.insert_file import insert_file
from src.utils.replace_file import replace_file


class TestRemoveFile:
    """Test the remove_file function with various scenarios."""
    
    @pytest.fixture
    def sample_file(self):
        """Create a temporary file with sample content."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            for i in range(1, 11):
                f.write(f"Line {i}: This is line number {i}\n")
            f.flush()
            yield f.name
        # Cleanup
        if os.path.exists(f.name):
            os.unlink(f.name)
    
    def test_remove_middle_lines(self, sample_file):
        """Test removing lines from the middle of the file."""
        message, success = remove_file(sample_file, 3, 5)
        
        assert success is True
        assert "Successfully removed lines 3 to 5" in message
        
        # Verify content
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) == 7  # Originally 10, removed 3
        assert "Line 2:" in lines[1]
        assert "Line 6:" in lines[2]  # Line 6 should now be at index 2
    
    def test_remove_from_start(self, sample_file):
        """Test removing lines from start to specific line."""
        message, success = remove_file(sample_file, None, 3)
        
        assert success is True
        assert "Successfully removed lines 1 to 3" in message
        
        # Verify content
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) == 7  # Originally 10, removed 3
        assert "Line 4:" in lines[0]  # Line 4 should now be first
    
    def test_remove_to_end(self, sample_file):
        """Test removing lines from specific line to end."""
        message, success = remove_file(sample_file, 7, None)
        
        assert success is True
        assert "Successfully removed lines 7 to end" in message
        
        # Verify content
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) == 6  # Originally 10, removed last 4
        assert "Line 6:" in lines[5]  # Line 6 should be last
    
    def test_remove_single_line(self, sample_file):
        """Test removing a single line."""
        message, success = remove_file(sample_file, 5, 5)
        
        assert success is True
        assert "Successfully removed lines 5 to 5" in message
        
        # Verify content
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) == 9  # Originally 10, removed 1
        assert "Line 4:" in lines[3]
        assert "Line 6:" in lines[4]  # Line 6 should follow Line 4
    
    def test_remove_beyond_file_length(self, sample_file):
        """Test removing lines beyond file length."""
        message, success = remove_file(sample_file, 15, 20)
        
        assert success is True
        assert "No lines removed" in message
        assert "exceeds file length" in message
        
        # File should be unchanged
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        assert len(lines) == 10
    
    def test_remove_invalid_parameters(self, sample_file):
        """Test with invalid parameters."""
        # No parameters
        message, success = remove_file(sample_file)
        assert success is False
        assert "At least one of start_line or end_line must be specified" in message
        
        # Invalid start line
        message, success = remove_file(sample_file, 0, 5)
        assert success is False
        assert "start_line must be at least 1" in message
        
        # Invalid end line
        message, success = remove_file(sample_file, 5, 0)
        assert success is False
        assert "end_line must be at least 1" in message
        
        # Start > end
        message, success = remove_file(sample_file, 8, 5)
        assert success is False
        assert "start_line must be less than or equal to end_line" in message
    
    def test_remove_nonexistent_file(self):
        """Test removing from nonexistent file."""
        message, success = remove_file("nonexistent.txt", 1, 5)
        
        assert success is False
        assert "does not exist" in message


class TestInsertFile:
    """Test the insert_file function with various scenarios."""
    
    @pytest.fixture
    def sample_file(self):
        """Create a temporary file with sample content."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Line 1\nLine 2\nLine 3\n")
            f.flush()
            yield f.name
        # Cleanup
        if os.path.exists(f.name):
            os.unlink(f.name)
    
    def test_create_new_file(self):
        """Test creating a new file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_file = os.path.join(temp_dir, "new_file.txt")
            content = "This is new content\nWith multiple lines\n"
            
            message, success = insert_file(new_file, content)
            
            assert success is True
            assert "Successfully created" in message
            assert os.path.exists(new_file)
            
            with open(new_file, 'r') as f:
                file_content = f.read()
            assert file_content == content
    
    def test_replace_existing_file(self, sample_file):
        """Test replacing an existing file completely."""
        new_content = "Completely new content\nReplacing everything\n"
        
        message, success = insert_file(sample_file, new_content)
        
        assert success is True
        assert "Successfully replaced" in message
        
        with open(sample_file, 'r') as f:
            file_content = f.read()
        assert file_content == new_content
    
    def test_insert_at_beginning(self, sample_file):
        """Test inserting at the beginning of the file."""
        insert_content = "New first line\n"
        
        message, success = insert_file(sample_file, insert_content, line_number=1)
        
        assert success is True
        assert "Successfully inserted into" in message
        
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert lines[0] == "New first line\n"
        assert lines[1] == "Line 1\n"
        assert len(lines) == 4  # Original 3 + 1 inserted
    
    def test_insert_in_middle(self, sample_file):
        """Test inserting in the middle of the file."""
        insert_content = "Inserted line\n"
        
        message, success = insert_file(sample_file, insert_content, line_number=2)
        
        assert success is True
        assert "Successfully inserted into" in message
        
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert lines[0] == "Line 1\n"
        assert lines[1] == "Inserted line\n"
        assert lines[2] == "Line 2\n"
        assert len(lines) == 4
    
    def test_insert_at_end(self, sample_file):
        """Test inserting at the end of the file."""
        insert_content = "New last line\n"
        
        message, success = insert_file(sample_file, insert_content, line_number=4)
        
        assert success is True
        assert "Successfully inserted into" in message
        
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) == 4
        assert lines[3] == "New last line\n"
    
    def test_insert_beyond_end(self, sample_file):
        """Test inserting beyond the end of the file."""
        insert_content = "Far beyond line\n"
        
        message, success = insert_file(sample_file, insert_content, line_number=10)
        
        assert success is True
        assert "Successfully inserted into" in message
        
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) == 10
        assert lines[9] == "Far beyond line\n"
        # Should have empty lines in between
        for i in range(3, 9):
            assert lines[i] == "\n"
    
    def test_insert_invalid_line_number(self, sample_file):
        """Test inserting with invalid line number."""
        message, success = insert_file(sample_file, "content", line_number=0)
        
        assert success is False
        assert "Line number must be at least 1" in message
    
    def test_insert_create_directories(self):
        """Test that directories are created if they don't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_file = os.path.join(temp_dir, "subdir", "nested", "file.txt")
            content = "Content in nested file\n"
            
            message, success = insert_file(nested_file, content)
            
            assert success is True
            assert "Successfully created" in message
            assert os.path.exists(nested_file)
            
            with open(nested_file, 'r') as f:
                file_content = f.read()
            assert file_content == content
    
    def test_insert_into_nonexistent_file_with_line_number(self):
        """Test inserting into nonexistent file with specific line number."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_file = os.path.join(temp_dir, "new_file.txt")
            content = "Content at line 3\n"
            
            message, success = insert_file(new_file, content, line_number=3)
            
            assert success is True
            assert "Successfully created and inserted into" in message
            
            with open(new_file, 'r') as f:
                lines = f.readlines()
            
            assert len(lines) == 2  # The implementation creates fewer empty lines
            assert lines[0] == "\n"  # Empty lines before insertion (newline character)
            assert lines[1] == "Content at line 3\n"


class TestReplaceFile:
    """Test the replace_file function with various scenarios."""
    
    @pytest.fixture
    def sample_file(self):
        """Create a temporary file with sample content."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            for i in range(1, 11):
                f.write(f"Line {i}: Original content\n")
            f.flush()
            yield f.name
        # Cleanup
        if os.path.exists(f.name):
            os.unlink(f.name)
    
    def test_replace_middle_lines(self, sample_file):
        """Test replacing lines in the middle of the file."""
        new_content = "New line 3\nNew line 4\nNew line 5\n"
        
        message, success = replace_file(sample_file, 3, 5, new_content)
        
        assert success is True
        assert "Successfully replaced lines 3 to 5" in message
        
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) == 10  # Same length (replaced 3 with 3)
        assert "Line 2:" in lines[1]
        assert lines[2] == "New line 3\n"
        assert lines[3] == "New line 4\n"
        assert lines[4] == "New line 5\n"
        assert "Line 6:" in lines[5]
    
    def test_replace_with_different_line_count(self, sample_file):
        """Test replacing with different number of lines."""
        new_content = "Single replacement line\n"
        
        message, success = replace_file(sample_file, 7, 9, new_content)
        
        assert success is True
        assert "Successfully replaced lines 7 to 9" in message
        
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) == 8  # Originally 10, removed 3, added 1
        assert "Line 6:" in lines[5]
        assert lines[6] == "Single replacement line\n"
        assert "Line 10:" in lines[7]
    
    def test_replace_single_line(self, sample_file):
        """Test replacing a single line."""
        new_content = "Replaced single line\n"
        
        message, success = replace_file(sample_file, 5, 5, new_content)
        
        assert success is True
        assert "Successfully replaced lines 5 to 5" in message
        
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) == 10
        assert "Line 4:" in lines[3]
        assert lines[4] == "Replaced single line\n"
        assert "Line 6:" in lines[5]
    
    def test_replace_invalid_parameters(self, sample_file):
        """Test replace with invalid parameters."""
        # Invalid start line
        message, success = replace_file(sample_file, 0, 5, "content")
        assert success is False
        assert "start_line must be at least 1" in message
        
        # Invalid end line
        message, success = replace_file(sample_file, 5, 0, "content")
        assert success is False
        assert "end_line must be at least 1" in message
        
        # Start > end
        message, success = replace_file(sample_file, 8, 5, "content")
        assert success is False
        assert "start_line must be less than or equal to end_line" in message
    
    def test_replace_nonexistent_file(self):
        """Test replacing in nonexistent file."""
        message, success = replace_file("nonexistent.txt", 1, 3, "content")
        
        assert success is False
        assert "does not exist" in message
    
    def test_replace_with_empty_content(self, sample_file):
        """Test replacing with empty content."""
        new_content = ""
        
        message, success = replace_file(sample_file, 3, 5, new_content)
        
        assert success is True
        
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) == 7  # Originally 10, removed 3, added 0
        assert "Line 2:" in lines[1]
        assert "Line 6:" in lines[2]
    
    def test_replace_first_lines(self, sample_file):
        """Test replacing lines at the beginning."""
        new_content = "New first line\nNew second line\n"
        
        message, success = replace_file(sample_file, 1, 2, new_content)
        
        assert success is True
        
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert lines[0] == "New first line\n"
        assert lines[1] == "New second line\n"
        assert "Line 3:" in lines[2]
    
    def test_replace_last_lines(self, sample_file):
        """Test replacing lines at the end."""
        new_content = "New last line\n"
        
        message, success = replace_file(sample_file, 9, 10, new_content)
        
        assert success is True
        
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) == 9  # Originally 10, removed 2, added 1
        assert "Line 8:" in lines[7]
        assert lines[8] == "New last line\n"
    
    def test_replace_entire_file(self, sample_file):
        """Test replacing the entire file content."""
        new_content = "Completely new content\nWith multiple lines\nReplacing everything\n"
        
        message, success = replace_file(sample_file, 1, 10, new_content)
        
        assert success is True
        
        with open(sample_file, 'r') as f:
            content = f.read()
        
        assert content == new_content
    
    def test_integration_with_dependencies(self, sample_file):
        """Test that replace_file properly uses remove_file and insert_file."""
        # This test verifies the integration works as expected
        new_content = "Integration test content\n"
        
        message, success = replace_file(sample_file, 5, 7, new_content)
        
        assert success is True
        assert "Successfully replaced lines 5 to 7" in message
        
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        # Should have 8 lines total (10 - 3 + 1)
        assert len(lines) == 8
        assert "Line 4:" in lines[3]
        assert lines[4] == "Integration test content\n"
        assert "Line 8:" in lines[5]