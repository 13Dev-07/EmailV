"""Enhanced validation metrics collection and tracking."""

from prometheus_client import Counter, Histogram, Gauge
from typing import Optional, Dict, Any
import logging
import json
import time

logger = logging.getLogger(__name__)

# Detailed validation step metrics
VALIDATION_STEP_DURATION = Histogram(
    'validation_step_duration_seconds',
    'Time spent in each validation step',
    ['step', 'status']
)

VALIDATION_STEP_ERRORS = Counter(
    'validation_step_errors_total',
    'Errors encountered during validation steps',
    ['step', 'error_type']
)

VALIDATION_STEP_RESULTS = Counter(
    'validation_step_results_total',
    'Results of each validation step',
    ['step', 'result']
)

# Detailed error tracking
ERROR_DETAILS = Counter(
    'validation_error_details_total',
    'Detailed breakdown of validation errors',
    ['step', 'error_type', 'error_detail']
)

# Resource utilization during validation
VALIDATION_RESOURCE_USAGE = Gauge(
    'validation_resource_usage',
    'Resource utilization during validation',
    ['resource_type']
)

class ValidationMetricsCollector:
    """Collects and manages detailed validation metrics."""
    
    def __init__(self):
        self.current_validation: Optional[Dict[str, Any]] = None
        self.start_time: float = 0
    
    def start_validation(self):
        """Start tracking a new validation operation."""
        self.current_validation = {
            'steps': [],
            'errors': [],
            'start_time': time.time()
        }
        self.start_time = time.time()
    
    def record_step(self, step_name: str, status: str, duration: float):
        """Record metrics for a validation step."""
        if self.current_validation is None:
            logger.warning("No validation context found when recording step")
            return
            
        VALIDATION_STEP_DURATION.labels(
            step=step_name,
            status=status
        ).observe(duration)
        
        VALIDATION_STEP_RESULTS.labels(
            step=step_name,
            result=status
        ).inc()
        
        self.current_validation['steps'].append({
            'name': step_name,
            'status': status,
            'duration': duration
        })
    
    def record_error(self, step_name: str, error_type: str, error_detail: str):
        """Record detailed error information."""
        if self.current_validation is None:
            logger.warning("No validation context found when recording error")
            return
            
        VALIDATION_STEP_ERRORS.labels(
            step=step_name,
            error_type=error_type
        ).inc()
        
        ERROR_DETAILS.labels(
            step=step_name,
            error_type=error_type,
            error_detail=error_detail
        ).inc()
        
        self.current_validation['errors'].append({
            'step': step_name,
            'type': error_type,
            'detail': error_detail,
            'timestamp': time.time()
        })
    
    def update_resource_usage(self, resource_type: str, value: float):
        """Update resource utilization metrics."""
        VALIDATION_RESOURCE_USAGE.labels(
            resource_type=resource_type
        ).set(value)
    
    def complete_validation(self) -> Dict[str, Any]:
        """Complete the current validation tracking and return results."""
        if self.current_validation is None:
            logger.warning("No validation context found when completing validation")
            return {}
            
        self.current_validation['total_duration'] = time.time() - self.start_time
        result = self.current_validation
        self.current_validation = None
        return result

# Global metrics collector instance
metrics_collector = ValidationMetricsCollector()

def get_metrics_collector() -> ValidationMetricsCollector:
    """Get the global metrics collector instance."""
    return metrics_collector