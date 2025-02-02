"""Circuit breaker implementation for external service calls."""

import asyncio
import time
from enum import Enum
from typing import Callable, Any, Optional
import logging
from prometheus_client import Counter, Gauge, Histogram

logger = logging.getLogger(__name__)

# Circuit breaker metrics
CIRCUIT_STATE = Gauge(
    'circuit_breaker_state',
    'Current state of circuit breaker (0=open, 1=half-open, 2=closed)',
    ['service']
)

CIRCUIT_FAILURES = Counter(
    'circuit_breaker_failures_total',
    'Number of failures tracked by circuit breaker',
    ['service']
)

CIRCUIT_TRIPS = Counter(
    'circuit_breaker_trips_total',
    'Number of times circuit breaker has been tripped',
    ['service']
)

REQUEST_DURATION = Histogram(
    'circuit_breaker_request_duration_seconds',
    'Duration of requests through circuit breaker',
    ['service', 'status']
)

class CircuitState(Enum):
    OPEN = 0
    HALF_OPEN = 1
    CLOSED = 2

class CircuitBreaker:
    """Implementation of the circuit breaker pattern."""
    
    def __init__(
        self,
        service_name: str,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_max_requests: int = 3
    ):
        self.service_name = service_name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_requests = half_open_max_requests
        
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = 0
        self._half_open_requests = 0
        self._lock = asyncio.Lock()
        
        # Initialize metrics
        CIRCUIT_STATE.labels(service=service_name).set(CircuitState.CLOSED.value)
    
    @property
    def state(self) -> CircuitState:
        return self._state
    
    async def __call__(self, func: Callable, *args, **kwargs) -> Any:
        """Execute the wrapped function according to circuit breaker logic."""
        async with self._lock:
            if self._state == CircuitState.OPEN:
                if time.time() - self._last_failure_time >= self.recovery_timeout:
                    self._enter_half_open()
                else:
                    raise CircuitBreakerOpen(f"Circuit breaker for {self.service_name} is OPEN")
            
            if self._state == CircuitState.HALF_OPEN and self._half_open_requests >= self.half_open_max_requests:
                raise CircuitBreakerOpen(f"Circuit breaker for {self.service_name} is HALF-OPEN and at max requests")
            
            if self._state == CircuitState.HALF_OPEN:
                self._half_open_requests += 1
        
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            REQUEST_DURATION.labels(
                service=self.service_name,
                status="success"
            ).observe(time.time() - start_time)
            
            async with self._lock:
                if self._state == CircuitState.HALF_OPEN:
                    self._enter_closed()
                self._failure_count = 0
            return result
            
        except Exception as e:
            REQUEST_DURATION.labels(
                service=self.service_name,
                status="failure"
            ).observe(time.time() - start_time)
            
            async with self._lock:
                self._handle_failure()
            raise
    
    def _handle_failure(self):
        """Handle a failure by potentially opening the circuit."""
        self._failure_count += 1
        CIRCUIT_FAILURES.labels(service=self.service_name).inc()
        
        if self._state == CircuitState.HALF_OPEN or self._failure_count >= self.failure_threshold:
            self._enter_open()
    
    def _enter_open(self):
        """Transition to OPEN state."""
        if self._state != CircuitState.OPEN:
            self._state = CircuitState.OPEN
            self._last_failure_time = time.time()
            CIRCUIT_STATE.labels(service=self.service_name).set(CircuitState.OPEN.value)
            CIRCUIT_TRIPS.labels(service=self.service_name).inc()
            logger.warning(f"Circuit breaker for {self.service_name} is now OPEN")
    
    def _enter_half_open(self):
        """Transition to HALF-OPEN state."""
        self._state = CircuitState.HALF_OPEN
        self._half_open_requests = 0
        CIRCUIT_STATE.labels(service=self.service_name).set(CircuitState.HALF_OPEN.value)
        logger.info(f"Circuit breaker for {self.service_name} is now HALF-OPEN")
    
    def _enter_closed(self):
        """Transition to CLOSED state."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._half_open_requests = 0
        CIRCUIT_STATE.labels(service=self.service_name).set(CircuitState.CLOSED.value)
        logger.info(f"Circuit breaker for {self.service_name} is now CLOSED")

class CircuitBreakerOpen(Exception):
    """Exception raised when circuit breaker is open."""
    pass