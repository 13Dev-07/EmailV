"""Unit tests for rate limiting component."""

import pytest
from unittest.mock import patch
import time
from app.rate_limiter import RateLimiter

@pytest.fixture
def rate_limiter():
    return RateLimiter(max_requests=2, window_size=1)

def test_rate_limiter_allows_within_limit(rate_limiter):
    """Test requests within rate limit are allowed."""
    assert rate_limiter.is_allowed("test_user")
    assert rate_limiter.is_allowed("test_user")
    assert not rate_limiter.is_allowed("test_user")  # Third request blocked

def test_rate_limiter_window_reset(rate_limiter):
    """Test rate limit resets after window expires."""
    assert rate_limiter.is_allowed("test_user")
    assert rate_limiter.is_allowed("test_user")
    
    with patch('time.time') as mock_time:
        # Move time forward past window
        mock_time.return_value = time.time() + 2
        assert rate_limiter.is_allowed("test_user")  # Should be allowed again

def test_rate_limiter_multiple_users(rate_limiter):
    """Test rate limits are tracked separately per user."""
    assert rate_limiter.is_allowed("user1")
    assert rate_limiter.is_allowed("user2")
    assert rate_limiter.is_allowed("user1")
    assert rate_limiter.is_allowed("user2")
    assert not rate_limiter.is_allowed("user1")
    assert not rate_limiter.is_allowed("user2")

def test_rate_limiter_cleanup(rate_limiter):
    """Test old entries are cleaned up."""
    assert rate_limiter.is_allowed("test_user")
    
    with patch('time.time') as mock_time:
        # Move time forward
        mock_time.return_value = time.time() + 2
        
        # This should trigger cleanup of old entry
        assert rate_limiter.is_allowed("other_user")
        
        # Verify cleanup happened
        assert len(rate_limiter._counters) == 1
        assert "test_user" not in rate_limiter._counters

def test_get_remaining_fresh_user(rate_limiter):
    """Test remaining requests for new user."""
    info = rate_limiter.get_remaining("new_user")
    assert info['remaining'] == 2
    assert info['reset_in'] == 1

def test_get_remaining_active_user(rate_limiter):
    """Test remaining requests updates correctly."""
    rate_limiter.is_allowed("test_user")  # Use 1 request
    info = rate_limiter.get_remaining("test_user")
    assert info['remaining'] == 1
    assert 0 < info['reset_in'] <= 1