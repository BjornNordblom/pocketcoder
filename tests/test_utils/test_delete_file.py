"""Tests for the delete_file utility function."""

import pytest
import os
import tempfile
from pathlib import Path
from src.utils.delete_file import delete_file


class TestDeleteFile:
    """Test the delete_file function with various scenarios."""
    
    @pytest.fixture
    def temp_file(self):
        """Create a temporary file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test content for deletion")
            f.flush()
            yield f.name
        # Cleanup in case test doesn't delete the file
        if os.path.exists(f.name):
            os.unlink(f.name)
    
    def test_delete_existing_file(self, temp_file):
        """Test deleting an existing file."""
        # Verify file exists
        assert os.path.exists(temp_file)
        
        # Delete the file
        message, success = delete_file(temp_file)
        
        # Verify successful deletion
        assert success is True
        assert "Successfully deleted" in message
        assert temp_file in message
        assert not os.path.exists(temp_file)
    
    def test_delete_nonexistent_file(self):
        """Test deleting a file that doesn't exist."""
        nonexistent_file = "/tmp/nonexistent_file_xyz.txt"
        
        # Ensure file doesn't exist
        if os.path.exists(nonexistent_file):
            os.unlink(nonexistent_file)
        
        message, success = delete_file(nonexistent_file)
        
        assert success is False
        assert "does not exist" in message
        assert nonexistent_file in message
    
    def test_delete_directory_fails(self):
        """Test that attempting to delete a directory fails appropriately."""
        with tempfile.TemporaryDirectory() as temp_dir:
            message, success = delete_file(temp_dir)
            
            assert success is False
            assert "Error deleting file" in message
            # Directory should still exist
            assert os.path.exists(temp_dir)
    
    def test_delete_file_permission_denied(self):
        """Test deleting a file with no write permissions."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test content")
            f.flush()
            temp_file = f.name
        
        try:
            # Remove write permissions from parent directory
            parent_dir = os.path.dirname(temp_file)
            original_mode = os.stat(parent_dir).st_mode
            
            # Skip if we can't change permissions on /tmp
            if parent_dir.startswith('/tmp'):
                pytest.skip("Cannot test permission denied on /tmp")
            
            try:
                os.chmod(parent_dir, 0o444)  # Read-only
                
                message, success = delete_file(temp_file)
                
                # Should fail due to permissions
                assert success is False
                assert "Error deleting file" in message
                
            except (OSError, PermissionError):
                # If we can't change permissions, skip this test
                pytest.skip("Cannot test permission denied on this system")
            finally:
                # Restore permissions
                os.chmod(parent_dir, original_mode)
                
        finally:
            # Cleanup
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_delete_file_with_unicode_name(self):
        """Test deleting a file with unicode characters in name."""
        unicode_filename = "test_file_ñiño_世界.txt"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            unicode_file = os.path.join(temp_dir, unicode_filename)
            
            # Create file with unicode name
            with open(unicode_file, 'w', encoding='utf-8') as f:
                f.write("Unicode test content")
            
            # Verify file exists
            assert os.path.exists(unicode_file)
            
            # Delete the file
            message, success = delete_file(unicode_file)
            
            # Verify successful deletion
            assert success is True
            assert "Successfully deleted" in message
            assert not os.path.exists(unicode_file)
    
    def test_delete_file_with_spaces_in_name(self):
        """Test deleting a file with spaces in the name."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spaced_file = os.path.join(temp_dir, "file with spaces.txt")
            
            # Create file with spaces in name
            with open(spaced_file, 'w') as f:
                f.write("File with spaces content")
            
            # Verify file exists
            assert os.path.exists(spaced_file)
            
            # Delete the file
            message, success = delete_file(spaced_file)
            
            # Verify successful deletion
            assert success is True
            assert "Successfully deleted" in message
            assert not os.path.exists(spaced_file)
    
    def test_delete_large_file(self):
        """Test deleting a large file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            # Write a large amount of data
            for i in range(10000):
                f.write(f"Line {i}: This is a test line with some content.\n")
            f.flush()
            large_file = f.name
        
        try:
            # Verify file exists and is large
            assert os.path.exists(large_file)
            assert os.path.getsize(large_file) > 100000  # > 100KB
            
            # Delete the file
            message, success = delete_file(large_file)
            
            # Verify successful deletion
            assert success is True
            assert "Successfully deleted" in message
            assert not os.path.exists(large_file)
            
        finally:
            # Cleanup in case deletion failed
            if os.path.exists(large_file):
                os.unlink(large_file)
    
    def test_delete_empty_file(self):
        """Test deleting an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            # Don't write anything, file will be empty
            f.flush()
            empty_file = f.name
        
        try:
            # Verify file exists and is empty
            assert os.path.exists(empty_file)
            assert os.path.getsize(empty_file) == 0
            
            # Delete the file
            message, success = delete_file(empty_file)
            
            # Verify successful deletion
            assert success is True
            assert "Successfully deleted" in message
            assert not os.path.exists(empty_file)
            
        finally:
            # Cleanup in case deletion failed
            if os.path.exists(empty_file):
                os.unlink(empty_file)
    
    def test_delete_readonly_file(self):
        """Test deleting a read-only file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Read-only file content")
            f.flush()
            readonly_file = f.name
        
        try:
            # Make file read-only
            os.chmod(readonly_file, 0o444)
            
            # Verify file exists and is read-only
            assert os.path.exists(readonly_file)
            
            # Delete the file (should still work)
            message, success = delete_file(readonly_file)
            
            # Verify successful deletion (os.remove should work on read-only files)
            assert success is True
            assert "Successfully deleted" in message
            assert not os.path.exists(readonly_file)
            
        except OSError:
            # If we can't change permissions, clean up and skip
            if os.path.exists(readonly_file):
                os.chmod(readonly_file, 0o644)
                os.unlink(readonly_file)
            pytest.skip("Cannot test read-only file on this system")
    
    def test_delete_file_absolute_path(self):
        """Test deleting a file using absolute path."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Absolute path test")
            f.flush()
            temp_file = f.name
        
        try:
            # Get absolute path
            abs_path = os.path.abspath(temp_file)
            
            # Verify file exists
            assert os.path.exists(abs_path)
            
            # Delete using absolute path
            message, success = delete_file(abs_path)
            
            # Verify successful deletion
            assert success is True
            assert "Successfully deleted" in message
            assert abs_path in message
            assert not os.path.exists(abs_path)
            
        finally:
            # Cleanup in case deletion failed
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_delete_file_relative_path(self, temp_file):
        """Test deleting a file using relative path."""
        # Create a symlink in current directory for testing
        relative_name = "test_relative_delete.txt"
        if os.path.exists(relative_name):
            os.unlink(relative_name)
        
        try:
            os.symlink(temp_file, relative_name)
            
            # Verify symlink exists
            assert os.path.exists(relative_name)
            
            # Delete using relative path
            message, success = delete_file(relative_name)
            
            # Verify successful deletion of symlink
            assert success is True
            assert "Successfully deleted" in message
            assert not os.path.exists(relative_name)
            
            # Original file should still exist
            assert os.path.exists(temp_file)
            
        finally:
            if os.path.exists(relative_name):
                os.unlink(relative_name)
    
    def test_delete_multiple_files_sequentially(self):
        """Test deleting multiple files in sequence."""
        temp_files = []
        
        try:
            # Create multiple temporary files
            for i in range(5):
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                    f.write(f"Content for file {i}")
                    f.flush()
                    temp_files.append(f.name)
            
            # Verify all files exist
            for temp_file in temp_files:
                assert os.path.exists(temp_file)
            
            # Delete all files
            for temp_file in temp_files:
                message, success = delete_file(temp_file)
                assert success is True
                assert "Successfully deleted" in message
                assert not os.path.exists(temp_file)
            
        finally:
            # Cleanup any remaining files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
    
    def test_return_value_format(self, temp_file):
        """Test that return values are properly formatted."""
        message, success = delete_file(temp_file)
        
        # Check return types
        assert isinstance(message, str)
        assert isinstance(success, bool)
        
        # Check message format
        assert len(message) > 0
        assert temp_file in message
        
        # For successful deletion
        assert success is True
        assert message.startswith("Successfully deleted")
    
    def test_error_message_format(self):
        """Test error message formatting."""
        nonexistent_file = "/tmp/definitely_nonexistent_file.txt"
        
        message, success = delete_file(nonexistent_file)
        
        # Check return types
        assert isinstance(message, str)
        assert isinstance(success, bool)
        
        # Check error format
        assert success is False
        assert len(message) > 0
        assert nonexistent_file in message