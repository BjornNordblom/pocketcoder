"""Tests for the dir_ops utility functions."""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from src.utils.dir_ops import list_dir, _build_tree_str


class TestListDir:
    """Test the list_dir function with various scenarios."""
    
    @pytest.fixture
    def test_directory_structure(self):
        """Create a temporary directory with a complex structure."""
        temp_dir = tempfile.mkdtemp()
        
        # Create files in root
        files = ['file1.txt', 'file2.py', 'config.yaml']
        for filename in files:
            with open(os.path.join(temp_dir, filename), 'w') as f:
                f.write(f"Content of {filename}")
        
        # Create subdirectories with files
        subdir1 = os.path.join(temp_dir, 'subdir1')
        os.makedirs(subdir1)
        with open(os.path.join(subdir1, 'nested_file.txt'), 'w') as f:
            f.write("Nested file content")
        
        subdir2 = os.path.join(temp_dir, 'subdir2')
        os.makedirs(subdir2)
        for i in range(3):
            with open(os.path.join(subdir2, f'file_{i}.txt'), 'w') as f:
                f.write(f"File {i} content")
        
        # Create empty subdirectory
        empty_dir = os.path.join(temp_dir, 'empty_dir')
        os.makedirs(empty_dir)
        
        yield temp_dir
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_list_existing_directory(self, test_directory_structure):
        """Test listing an existing directory."""
        success, tree_str = list_dir(test_directory_structure)
        
        assert success is True
        assert isinstance(tree_str, str)
        assert len(tree_str) > 0
        
        # Check that directories are shown with /
        assert "subdir1/" in tree_str
        assert "subdir2/" in tree_str
        assert "empty_dir/" in tree_str
        
        # Check that files are shown
        assert "file1.txt" in tree_str
        assert "file2.py" in tree_str
        assert "config.yaml" in tree_str
    
    def test_list_nonexistent_directory(self):
        """Test listing a nonexistent directory."""
        success, tree_str = list_dir("/nonexistent/directory")
        
        assert success is False
        assert tree_str == ""
    
    def test_list_file_instead_of_directory(self, test_directory_structure):
        """Test listing a file instead of a directory."""
        file_path = os.path.join(test_directory_structure, "file1.txt")
        success, tree_str = list_dir(file_path)
        
        assert success is False
        assert tree_str == ""
    
    def test_empty_directory(self):
        """Test listing an empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            success, tree_str = list_dir(temp_dir)
            
            assert success is True
            # Empty directory should produce empty tree string
            assert tree_str == ""
    
    def test_directory_with_many_files(self):
        """Test directory with more than 10 files (should show ellipsis)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create 15 files
            for i in range(15):
                with open(os.path.join(temp_dir, f"file_{i:02d}.txt"), 'w') as f:
                    f.write(f"Content {i}")
            
            success, tree_str = list_dir(temp_dir)
            
            assert success is True
            assert "... (5 more files)" in tree_str
    
    def test_directory_with_subdirectory_counts(self, test_directory_structure):
        """Test that subdirectories show content counts."""
        success, tree_str = list_dir(test_directory_structure)
        
        assert success is True
        # Should show counts for subdirectories
        assert "directory" in tree_str or "directories" in tree_str or "file" in tree_str
    
    def test_file_sizes_shown(self, test_directory_structure):
        """Test that file sizes are shown in KB."""
        success, tree_str = list_dir(test_directory_structure)
        
        assert success is True
        # Should show file sizes for some files
        assert "KB" in tree_str
    
    def test_relative_path_normalization(self, test_directory_structure):
        """Test that relative paths are normalized."""
        # Create a path with .. in it
        parent_dir = os.path.dirname(test_directory_structure)
        current_dir = os.path.basename(test_directory_structure)
        complex_path = os.path.join(parent_dir, ".", current_dir)
        
        success, tree_str = list_dir(complex_path)
        
        assert success is True
        assert len(tree_str) > 0
    
    def test_permission_denied_handling(self):
        """Test handling of permission denied errors."""
        # This test might not work on all systems
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a subdirectory
            restricted_dir = os.path.join(temp_dir, "restricted")
            os.makedirs(restricted_dir)
            
            try:
                # Remove read permissions
                os.chmod(restricted_dir, 0o000)
                
                # Should not crash
                success, tree_str = list_dir(temp_dir)
                assert success is True
                
            except OSError:
                # If we can't change permissions, skip this test
                pytest.skip("Cannot test permission denied on this system")
            finally:
                # Restore permissions for cleanup
                try:
                    os.chmod(restricted_dir, 0o755)
                except OSError:
                    pass
    
    def test_current_directory(self):
        """Test listing current directory."""
        success, tree_str = list_dir(".")
        
        assert success is True
        assert isinstance(tree_str, str)
        # Should contain some common project files
        assert any(name in tree_str for name in ["src", "tests"])


class TestBuildTreeStr:
    """Test the _build_tree_str helper function."""
    
    def test_empty_items_list(self):
        """Test building tree string with empty items."""
        result = _build_tree_str([])
        assert result == ""
    
    def test_single_file(self):
        """Test building tree string with single file."""
        items = [
            {
                "name": "test.txt",
                "type": "file",
                "size": 1024
            }
        ]
        
        result = _build_tree_str(items)
        
        assert "└── test.txt" in result
        assert "1.0 KB" in result
    
    def test_single_directory(self):
        """Test building tree string with single directory."""
        items = [
            {
                "name": "testdir",
                "type": "directory",
                "children": [
                    {"name": "file1.txt", "type": "file", "size": 500}
                ]
            }
        ]
        
        result = _build_tree_str(items)
        
        assert "testdir/" in result
        assert "1 file" in result
    
    def test_mixed_directories_and_files(self):
        """Test building tree string with mixed content."""
        items = [
            {
                "name": "dir1",
                "type": "directory",
                "children": [
                    {"name": "subfile.txt", "type": "file", "size": 100}
                ]
            },
            {
                "name": "file1.txt",
                "type": "file",
                "size": 2048
            },
            {
                "name": "file2.py",
                "type": "file",
                "size": 512
            }
        ]
        
        result = _build_tree_str(items)
        
        # Directories should come first
        assert result.find("dir1/") < result.find("file1.txt")
        assert "├── dir1/" in result
        assert "├── file1.txt" in result
        assert "└── file2.py" in result
        assert "2.0 KB" in result
        assert "0.5 KB" in result
    
    def test_directory_with_multiple_children(self):
        """Test directory with multiple files and subdirectories."""
        items = [
            {
                "name": "complex_dir",
                "type": "directory",
                "children": [
                    {"name": "subdir", "type": "directory"},
                    {"name": "file1.txt", "type": "file", "size": 100},
                    {"name": "file2.txt", "type": "file", "size": 200}
                ]
            }
        ]
        
        result = _build_tree_str(items)
        
        assert "complex_dir/" in result
        assert "1 directory, 2 files" in result
    
    def test_file_size_formatting(self):
        """Test file size formatting."""
        items = [
            {"name": "small.txt", "type": "file", "size": 0},
            {"name": "medium.txt", "type": "file", "size": 1536},  # 1.5 KB
            {"name": "large.txt", "type": "file", "size": 10240}   # 10.0 KB
        ]
        
        result = _build_tree_str(items)
        
        # Zero size files shouldn't show size
        assert "small.txt" in result
        assert "small.txt (" not in result
        
        # Other files should show size
        assert "1.5 KB" in result
        assert "10.0 KB" in result
    
    def test_more_than_ten_files(self):
        """Test handling of more than 10 files."""
        items = []
        for i in range(15):
            items.append({
                "name": f"file_{i:02d}.txt",
                "type": "file",
                "size": 100 * (i + 1)
            })
        
        result = _build_tree_str(items)
        
        # Should show first 10 files
        assert "file_00.txt" in result
        assert "file_09.txt" in result
        
        # Should show ellipsis for remaining files
        assert "... (5 more files)" in result
        
        # Should not show files beyond 10
        assert "file_14.txt" not in result
    
    def test_tree_connectors(self):
        """Test that tree connectors are used correctly."""
        items = [
            {"name": "dir1", "type": "directory", "children": []},
            {"name": "dir2", "type": "directory", "children": []},
            {"name": "file1.txt", "type": "file", "size": 100},
            {"name": "file2.txt", "type": "file", "size": 200}
        ]
        
        result = _build_tree_str(items)
        
        # Should use ├── for non-last items and └── for last item
        lines = result.strip().split('\n')
        last_line = lines[-1]
        assert "└──" in last_line
        
        # Other lines should use ├──
        for line in lines[:-1]:
            if line.strip():  # Skip empty lines
                assert "├──" in line
    
    def test_directory_summary_formatting(self):
        """Test directory summary formatting."""
        # Test singular vs plural
        items = [
            {
                "name": "single_dir",
                "type": "directory",
                "children": [
                    {"name": "subdir", "type": "directory"},
                    {"name": "file.txt", "type": "file", "size": 100}
                ]
            },
            {
                "name": "multiple_dir",
                "type": "directory",
                "children": [
                    {"name": "subdir1", "type": "directory"},
                    {"name": "subdir2", "type": "directory"},
                    {"name": "file1.txt", "type": "file", "size": 100},
                    {"name": "file2.txt", "type": "file", "size": 200}
                ]
            }
        ]
        
        result = _build_tree_str(items)
        
        # Check singular forms
        assert "1 directory, 1 file" in result
        
        # Check plural forms
        assert "2 directories, 2 files" in result