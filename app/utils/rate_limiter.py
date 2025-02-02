"""
Rate Limiter Module
Implements rate limiting for the application.
"""

import time
from collections import defaultdict
from threading import Lock

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initializes the RateLimiter.

        Args:
            max_requests (int): Maximum number of allowed requests within the window.
            window_seconds (int): Time window for rate limiting in seconds.
        """
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(list)
        self.lock = Lock()

    def is_allowed(self, user_id: str) -> bool:
        """
        Determines if a request from the given user is allowed.

        Args:
            user_id (str): Identifier for the user.

        Returns:
            bool: True if the request is allowed, False otherwise.
        """
        current_time = time.time()
        with self.lock:
            request_times = self.requests[user_id]

            # Remove outdated requests
            while request_times and request_times[0] <= current_time - self.window:
                request_times.pop(0)

            if len(request_times) < self.max_requests:
                request_times.append(current_time)
                return True
            else:
                return False