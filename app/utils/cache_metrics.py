"""
Cache Metrics Module
Defines Prometheus metrics for cache monitoring.
"""

from prometheus_client import Counter, Histogram, Gauge

# Cache operation metrics
CACHE_HITS = Counter('email_validator_cache_hits_total',
                  'Number of cache hits',
                  ['cache_type'])

CACHE_MISSES = Counter('email_validator_cache_misses_total',
                    'Number of cache misses',
                    ['cache_type'])

CACHE_LATENCY = Histogram('email_validator_cache_latency_seconds',
                       'Cache operation latency in seconds',
                       ['operation'])

# Cache state metrics
CACHE_SIZE = Gauge('email_validator_cache_size_bytes',
                'Current cache size in bytes',
                ['cache_type'])

CACHE_ITEMS = Gauge('email_validator_cache_items_total',
                 'Number of items in cache',
                 ['cache_type'])

CACHE_MEMORY = Gauge('email_validator_cache_memory_bytes',
                  'Memory used by cache',
                  ['type'])  # resident, peak, etc.

# Cache operations metrics
CACHE_OPERATIONS = Counter('email_validator_cache_operations_total',
                       'Number of cache operations',
                       ['operation', 'status'])

CACHE_ERRORS = Counter('email_validator_cache_errors_total',
                    'Number of cache errors',
                    ['operation', 'error_type'])

# Invalidation metrics
CACHE_INVALIDATIONS = Counter('email_validator_cache_invalidations_total',
                          'Number of cache invalidations',
                          ['reason'])

CACHE_EVICTIONS = Counter('email_validator_cache_evictions_total',
                       'Number of cache evictions',
                       ['reason'])