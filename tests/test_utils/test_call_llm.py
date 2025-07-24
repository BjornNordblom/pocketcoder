"""Tests for the call_llm utility function."""

import pytest
import os
import json
import tempfile
from unittest.mock import Mock, patch, mock_open
from src.utils.call_llm import call_llm, clear_cache


class TestCallLLM:
    """Test the call_llm function with various scenarios."""
    
    @pytest.fixture
    def mock_anthropic_response(self):
        """Mock Anthropic API response."""
        mock_response = Mock()
        mock_response.content = [Mock(), Mock()]
        mock_response.content[1].text = "Test response from API"
        return mock_response
    
    @pytest.fixture
    def temp_cache_file(self):
        """Create a temporary cache file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            cache_file = f.name
        yield cache_file
        # Cleanup
        if os.path.exists(cache_file):
            os.remove(cache_file)
    
    @patch('src.utils.call_llm.cache_file')
    @patch('src.utils.call_llm.AnthropicVertex')
    def test_call_llm_without_cache(self, mock_anthropic_class, mock_cache_file, mock_anthropic_response, temp_cache_file):
        """Test LLM call without cache."""
        mock_cache_file.return_value = temp_cache_file
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_anthropic_response
        mock_anthropic_class.return_value = mock_client
        
        result = call_llm("test prompt", use_cache=False)
        
        assert result == "Test response from API"
        mock_client.messages.create.assert_called_once()
        
        # Verify the call parameters
        call_args = mock_client.messages.create.call_args
        assert call_args[1]['max_tokens'] == 20000
        assert call_args[1]['messages'] == [{"role": "user", "content": "test prompt"}]
    
    @patch('src.utils.call_llm.AnthropicVertex')
    def test_call_llm_with_cache_miss(self, mock_anthropic_class, mock_anthropic_response, temp_cache_file):
        """Test LLM call with cache miss."""
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_anthropic_response
        mock_anthropic_class.return_value = mock_client
        
        with patch('src.utils.call_llm.cache_file', temp_cache_file):
            result = call_llm("test prompt", use_cache=True)
            
            assert result == "Test response from API"
            mock_client.messages.create.assert_called_once()
            
            # Verify cache was updated
            assert os.path.exists(temp_cache_file)
            with open(temp_cache_file, 'r') as f:
                cache = json.load(f)
            assert cache["test prompt"] == "Test response from API"
    
    def test_call_llm_with_cache_hit(self, temp_cache_file):
        """Test LLM call with cache hit."""
        # Pre-populate cache
        cache_data = {"test prompt": "Cached response"}
        with open(temp_cache_file, 'w') as f:
            json.dump(cache_data, f)
        
        with patch('src.utils.call_llm.cache_file', temp_cache_file):
            with patch('src.utils.call_llm.AnthropicVertex') as mock_anthropic:
                result = call_llm("test prompt", use_cache=True)
                
                assert result == "Cached response"
                mock_anthropic.assert_not_called()  # Should not call API
    
    @patch('src.utils.call_llm.AnthropicVertex')
    def test_call_llm_cache_file_corruption(self, mock_anthropic_class, mock_anthropic_response, temp_cache_file):
        """Test handling of corrupted cache file."""
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_anthropic_response
        mock_anthropic_class.return_value = mock_client
        
        # Create corrupted cache file
        with open(temp_cache_file, 'w') as f:
            f.write("invalid json content")
        
        with patch('src.utils.call_llm.cache_file', temp_cache_file):
            result = call_llm("test prompt", use_cache=True)
            
            assert result == "Test response from API"
            mock_client.messages.create.assert_called_once()
    
    def test_clear_cache(self, temp_cache_file):
        """Test cache clearing functionality."""
        # Create cache file with content
        cache_data = {"test": "data"}
        with open(temp_cache_file, 'w') as f:
            json.dump(cache_data, f)
        
        assert os.path.exists(temp_cache_file)
        
        with patch('src.utils.call_llm.cache_file', temp_cache_file):
            clear_cache()
            
            assert not os.path.exists(temp_cache_file)
    
    def test_clear_cache_nonexistent_file(self, temp_cache_file):
        """Test clearing cache when file doesn't exist."""
        # Ensure file doesn't exist
        if os.path.exists(temp_cache_file):
            os.remove(temp_cache_file)
        
        # Should not raise exception
        with patch('src.utils.call_llm.cache_file', temp_cache_file):
            clear_cache()
    
    @patch.dict(os.environ, {'ANTHROPIC_REGION': 'us-west1', 'ANTHROPIC_PROJECT_ID': 'test-project'})
    @patch('src.utils.call_llm.AnthropicVertex')
    def test_environment_variables(self, mock_anthropic_class, mock_anthropic_response, temp_cache_file):
        """Test that environment variables are used correctly."""
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_anthropic_response
        mock_anthropic_class.return_value = mock_client
        
        with patch('src.utils.call_llm.cache_file', temp_cache_file):
            call_llm("test prompt", use_cache=False)
            
            mock_anthropic_class.assert_called_with(
                region="us-west1",
                project_id="test-project"
            )
    
    @patch('src.utils.call_llm.AnthropicVertex')
    def test_api_error_handling(self, mock_anthropic_class, temp_cache_file):
        """Test handling of API errors."""
        mock_client = Mock()
        mock_client.messages.create.side_effect = Exception("API Error")
        mock_anthropic_class.return_value = mock_client
        
        with patch('src.utils.call_llm.cache_file', temp_cache_file):
            with pytest.raises(Exception) as exc_info:
                call_llm("test prompt", use_cache=False)
            
            assert "API Error" in str(exc_info.value)
    
    @patch('src.utils.call_llm.AnthropicVertex')
    def test_cache_save_error_handling(self, mock_anthropic_class, mock_anthropic_response):
        """Test handling of cache save errors."""
        # Use an invalid cache file path to trigger save error
        invalid_cache_file = "/invalid/path/cache.json"
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_anthropic_response
        mock_anthropic_class.return_value = mock_client
        
        # Should not raise exception even if cache save fails
        with patch('src.utils.call_llm.cache_file', invalid_cache_file):
            result = call_llm("test prompt", use_cache=True)
            assert result == "Test response from API"
    
    @patch('src.utils.call_llm.logger')
    @patch('src.utils.call_llm.AnthropicVertex')
    def test_logging_functionality(self, mock_anthropic_class, mock_logger, mock_anthropic_response, temp_cache_file):
        """Test that logging works correctly."""
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_anthropic_response
        mock_anthropic_class.return_value = mock_client
        
        with patch('src.utils.call_llm.cache_file', temp_cache_file):
            call_llm("test prompt", use_cache=False)
            
            # Check that logging was called
            assert mock_logger.info.call_count >= 2  # At least prompt and response logging
            
            # Check log content
            log_calls = mock_logger.info.call_args_list
            prompt_logged = any("PROMPT: test prompt" in str(call) for call in log_calls)
            response_logged = any("RESPONSE: Test response from API" in str(call) for call in log_calls)
            
            assert prompt_logged
            assert response_logged