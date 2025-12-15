"""
Unit tests for retry logic with exponential backoff.

Tests decorator behavior, timing, max retries, and exception handling.
"""

import pytest
import time
from unittest.mock import Mock, patch
from src.utils.retry_logic import (
    exponential_backoff_retry,
    retry_with_backoff,
    MaxRetriesExceeded
)


class TestExponentialBackoffRetry:
    """Test exponential backoff retry decorator."""
    
    def test_successful_first_attempt(self):
        """Test function succeeds on first attempt without retry."""
        mock_func = Mock(return_value="success")
        mock_func.__name__ = "test_func"
        decorated = exponential_backoff_retry()(mock_func)
        
        result = decorated()
        
        assert result == "success"
        assert mock_func.call_count == 1
    
    def test_retry_on_exception(self):
        """Test function retries on specified exceptions."""
        mock_func = Mock(side_effect=[
            ValueError("First attempt"),
            ValueError("Second attempt"),
            "success"  # Third attempt succeeds
        ])
        mock_func.__name__ = "test_func"
        mock_func.__name__ = "test_func"
        
        decorated = exponential_backoff_retry(exceptions=(ValueError,))(mock_func)
        
        result = decorated()
        
        assert result == "success"
        assert mock_func.call_count == 3
    
    def test_max_retries_exhausted(self):
        """Test MaxRetriesExceeded raised after exhausting retries."""
        mock_func = Mock(side_effect=ValueError("Always fails"))
        mock_func.__name__ = "test_func"
        mock_func.__name__ = "test_func"
        decorated = exponential_backoff_retry(max_retries=3, exceptions=(ValueError,))(mock_func)
        
        with pytest.raises(MaxRetriesExceeded) as exc_info:
            decorated()
        
        # Check exception message contains failure info
        assert "Failed after" in str(exc_info.value)
        assert "3 attempts" in str(exc_info.value)
        assert mock_func.call_count == 3
    
    def test_exponential_delay_timing(self):
        """Test exponential backoff delay timing (1s, 2s, 4s)."""
        mock_func = Mock(side_effect=[ValueError(), ValueError(), "success"])
        mock_func.__name__ = "test_func"
        mock_func.__name__ = "test_func"
        
        with patch('time.sleep') as mock_sleep:
            decorated = exponential_backoff_retry(
                max_retries=3,
                base_delay=1.0,
                exceptions=(ValueError,)
            )(mock_func)
            
            decorated()
            
            # Verify sleep was called with correct delays
            assert mock_sleep.call_count == 2  # Sleep before 2nd and 3rd attempts
            calls = [call[0][0] for call in mock_sleep.call_args_list]
            assert calls[0] == 1.0  # First retry: 1s delay
            assert calls[1] == 2.0  # Second retry: 2s delay
    
    def test_max_delay_cap(self):
        """Test delay is capped at max_delay."""
        mock_func = Mock(side_effect=[ValueError()] * 10)
        mock_func.__name__ = "test_func"
        mock_func.__name__ = "test_func"
        
        with patch('time.sleep') as mock_sleep:
            decorated = exponential_backoff_retry(
                max_retries=10,
                base_delay=1.0,
                max_delay=5.0,  # Cap at 5 seconds
                exceptions=(ValueError,)
            )(mock_func)
            
            with pytest.raises(MaxRetriesExceeded):
                decorated()
            
            # Check that no delay exceeds max_delay
            for call in mock_sleep.call_args_list:
                delay = call[0][0]
                assert delay <= 5.0
    
    def test_exception_type_filtering(self):
        """Test only specified exception types trigger retry."""
        # ValueError should be retried
        mock_func1 = Mock(side_effect=[ValueError(), "success"])
        mock_func1.__name__ = "test_func1"
        mock_func1.__name__ = "test_func1"
        decorated1 = exponential_backoff_retry(exceptions=(ValueError,))(mock_func1)
        
        result1 = decorated1()
        assert result1 == "success"
        assert mock_func1.call_count == 2
        
        # TypeError should not be retried (immediate failure)
        mock_func2 = Mock(side_effect=TypeError("Not retryable"))
        mock_func2.__name__ = "test_func2"
        mock_func2.__name__ = "test_func2"
        decorated2 = exponential_backoff_retry(exceptions=(ValueError,))(mock_func2)
        
        with pytest.raises(TypeError):
            decorated2()
        
        assert mock_func2.call_count == 1  # No retry
    
    def test_original_exception_chained(self):
        """Test original exception is chained in MaxRetriesExceeded."""
        original_error = ValueError("Original error")
        mock_func = Mock(side_effect=original_error)
        mock_func.__name__ = "test_func"
        mock_func.__name__ = "test_func"
        decorated = exponential_backoff_retry(max_retries=2, exceptions=(ValueError,))(mock_func)
        
        with pytest.raises(MaxRetriesExceeded) as exc_info:
            decorated()
        
        # Check the exception chain
        assert exc_info.value.__cause__ == original_error
    
    def test_function_with_arguments(self):
        """Test decorator works with functions that have arguments."""
        def func_with_args(a, b, c=None):
            if a < 0:
                raise ValueError("Negative value")
            return a + b + (c or 0)
        
        decorated = exponential_backoff_retry(exceptions=(ValueError,))(func_with_args)
        
        # Should succeed without retry
        result = decorated(1, 2, c=3)
        assert result == 6
    
    def test_async_function_not_supported(self):
        """Test that async functions are not directly supported."""
        # Note: The current implementation doesn't support async functions
        # This test documents expected behavior
        
        @exponential_backoff_retry()
        async def async_func():
            return "async result"
        
        # Calling async function will return a coroutine, not the result
        result = async_func()
        assert hasattr(result, '__await__')  # It's a coroutine


class TestRetryWithBackoffFunction:
    """Test retry_with_backoff non-decorator function."""
    
    def test_retry_with_backoff_success(self):
        """Test retry_with_backoff function succeeds."""
        mock_func = Mock(side_effect=[ValueError(), ValueError(), "success"])
        mock_func.__name__ = "test_func"
        
        result = retry_with_backoff(
            func=mock_func,
            max_retries=3,
            base_delay=0.1,  # Small delay for test speed
            exceptions=(ValueError,)
        )
        
        assert result == "success"
        assert mock_func.call_count == 3
    
    def test_retry_with_backoff_failure(self):
        """Test retry_with_backoff raises MaxRetriesExceeded."""
        mock_func = Mock(side_effect=ValueError("Always fails"))
        mock_func.__name__ = "test_func"
        
        with pytest.raises(MaxRetriesExceeded):
            retry_with_backoff(
                func=mock_func,
                max_retries=2,
                base_delay=0.1,
                exceptions=(ValueError,)
            )
        
        assert mock_func.call_count == 2


class TestMaxRetriesExceededException:
    """Test MaxRetriesExceeded exception."""
    
    def test_exception_message(self):
        """Test exception contains useful message."""
        exc = MaxRetriesExceeded("Failed after 3 attempts: error")
        
        assert "Failed after" in str(exc)
        assert "3 attempts" in str(exc)
    
    def test_exception_attributes(self):
        """Test exception stores error message."""
        exc = MaxRetriesExceeded("Failed after 5 attempts: error message")
        
        assert "Failed after 5 attempts" in exc.args[0]
