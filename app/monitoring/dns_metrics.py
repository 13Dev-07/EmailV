"""DNS resolution performance monitoring."""
import time
from typing import Dict, Optional
from dataclasses import dataclass, field
from statistics import mean, median

@dataclass
class DNSMetrics:
    """Collector for DNS resolution performance metrics."""
    
    resolution_times: Dict[str, float] = field(default_factory=dict)
    cache_hits: int = 0
    cache_misses: int = 0
    parallel_resolutions: int = 0
    failed_resolutions: int = 0
    
    def record_resolution(self, domain: str, duration: float, cached: bool = False,
                         parallel: bool = False, failed: bool = False) -> None:
        """Record metrics for a single resolution operation."""
        self.resolution_times[domain] = duration
        if cached:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        if parallel:
            self.parallel_resolutions += 1
        if failed:
            self.failed_resolutions += 1
            
    def get_stats(self) -> Dict[str, float]:
        """Get summary statistics for DNS resolution performance."""
        times = list(self.resolution_times.values())
        if not times:
            return {}
            
        return {
            "mean_resolution_time": mean(times),
            "median_resolution_time": median(times),
            "min_resolution_time": min(times),
            "max_resolution_time": max(times),
            "cache_hit_ratio": self.cache_hits / (self.cache_hits + self.cache_misses)
                if (self.cache_hits + self.cache_misses) > 0 else 0,
            "parallel_resolution_ratio": self.parallel_resolutions / len(times)
                if times else 0,
            "failure_rate": self.failed_resolutions / len(times)
                if times else 0
        }
        
    def reset(self) -> None:
        """Reset all metrics."""
        self.resolution_times.clear()
        self.cache_hits = 0
        self.cache_misses = 0
        self.parallel_resolutions = 0
        self.failed_resolutions = 0