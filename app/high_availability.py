"""High availability configuration for email validator service."""

import aiohttp
import asyncio
from typing import List, Dict, Optional, Any
import random
import time
import logging
from prometheus_client import Counter, Gauge

logger = logging.getLogger(__name__)

# Metrics
node_health_status = Gauge(
    'node_health_status',
    'Health status of service nodes',
    ['node']
)

failover_events = Counter(
    'failover_events_total',
    'Number of failover events',
    ['source_node', 'target_node']
)

class ServiceNode:
    """Represents a service node in the HA cluster."""
    
    def __init__(self, url: str, weight: int = 100):
        self.url = url
        self.weight = weight
        self.healthy = True
        self.last_check = time.time()
        self.consecutive_failures = 0
        
    def __str__(self) -> str:
        return f"ServiceNode(url={self.url}, healthy={self.healthy})"

class LoadBalancer:
    """Load balancer with health checking, failover, and circuit breaker pattern."""
    
    def __init__(
        self,
        nodes: List[Dict[str, Any]],
        health_check_interval: float = 5.0,
        max_failures: int = 3,
        circuit_breaker_timeout: float = 60.0,
        half_open_max_requests: int = 3,
        consul_host: str = "localhost",
        consul_port: int = 8500,
        service_name: str = "email-validator"
    ):
        """
        Initialize load balancer.
        
        Args:
            nodes: List of node configurations with URLs and weights
            health_check_interval: Time between health checks in seconds
            max_failures: Maximum consecutive failures before marking node unhealthy
            circuit_breaker_timeout: Time before attempting recovery in seconds
            half_open_max_requests: Maximum requests in half-open state
        """
        self.nodes = [ServiceNode(**node) for node in nodes]
        self.health_check_interval = health_check_interval
        self.max_failures = max_failures
        self._session: Optional[aiohttp.ClientSession] = None
        self._health_check_task: Optional[asyncio.Task] = None
        self._service_discovery_task: Optional[asyncio.Task] = None
        
        # Initialize service registry
        self.service_registry = ServiceRegistry(
            consul_host=consul_host,
            consul_port=consul_port,
            service_name=service_name
        )
        
        # Create circuit breakers for each node
        self.circuit_breakers = {
            node.url: CircuitBreaker(
                service_name=node.url,
                failure_threshold=max_failures,
                recovery_timeout=circuit_breaker_timeout,
                half_open_max_requests=half_open_max_requests
            )
            for node in self.nodes
        }
        
    async def start(self):
        """Start the load balancer and health checks."""
        self._session = aiohttp.ClientSession()
        await self.service_registry.start()
        self._health_check_task = asyncio.create_task(self._health_check_loop())
        self._service_discovery_task = asyncio.create_task(
            self.service_registry.watch_services(self._update_nodes)
        )
        
    async def stop(self):
        """Stop the load balancer and cleanup."""
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass
                
        if self._service_discovery_task:
            self._service_discovery_task.cancel()
            try:
                await self._service_discovery_task
            except asyncio.CancelledError:
                pass
        
        if self._session:
            await self._session.close()
            
        await self.service_registry.stop()
            
    async def _health_check_loop(self):
        """Continuous health checking of nodes."""
        while True:
            try:
                await self._check_all_nodes()
                await asyncio.sleep(self.health_check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health check error: {e}")
                await asyncio.sleep(1)
                
    async def _check_all_nodes(self):
        """Check health of all nodes."""
        tasks = [self._check_node(node) for node in self.nodes]
        await asyncio.gather(*tasks)
        
    async def _check_node(self, node: ServiceNode):
        """Check health of a single node using circuit breaker pattern."""
        circuit_breaker = self.circuit_breakers[node.url]
        
        try:
            # Use circuit breaker to make the health check request
            async def health_check():
                async with self._session.get(f"{node.url}/health") as response:
                    if response.status != 200:
                        raise ValueError(f"Unhealthy response: {response.status}")
                    return True
            
            await circuit_breaker(health_check)
            node.consecutive_failures = 0
            healthy = True
            
        except CircuitBreakerOpen as e:
            logger.error(f"Circuit breaker open for {node.url}: {e}")
            healthy = False
            node.consecutive_failures = self.max_failures  # Force unhealthy state
            
        except Exception as e:
            logger.warning(f"Health check failed for {node.url}: {e}")
            node.consecutive_failures += 1
            healthy = False
        
        # Update node health status
        was_healthy = node.healthy
        node.healthy = healthy
        node.last_check = time.time()
        
        # Update metrics
        node_health_status.labels(node=node.url).set(1 if node.healthy else 0)
        
        # Log state changes
        if was_healthy and not node.healthy:
            logger.error(f"Node {node.url} is now unhealthy")
            self._handle_node_failure(node)
        elif not was_healthy and node.healthy:
            logger.info(f"Node {node.url} recovered")
            
    def _handle_node_failure(self, failed_node: ServiceNode):
        """Handle node failure by updating routing."""
        healthy_nodes = [n for n in self.nodes if n.healthy and n != failed_node]
        if healthy_nodes:
            target_node = random.choice(healthy_nodes)
            failover_events.labels(
                source_node=failed_node.url,
                target_node=target_node.url
            ).inc()
            
            # Schedule recovery check
            asyncio.create_task(self._attempt_node_recovery(failed_node))
            
    async def _attempt_node_recovery(self, node: ServiceNode, max_attempts: int = 3):
        """Attempt to recover a failed node.
        
        Args:
            node: The node to attempt recovery for
            max_attempts: Maximum number of recovery attempts
        """
        for attempt in range(max_attempts):
            await asyncio.sleep(5 * (attempt + 1))  # Exponential backoff
            
            try:
                async with self._session.get(f"{node.url}/health") as response:
                    if response.status == 200:
                        # Node is responding again
                        node.healthy = True
                        node.consecutive_failures = 0
                        circuit_breaker = self.circuit_breakers[node.url]
                        await circuit_breaker._enter_half_open()
                        logger.info(f"Node {node.url} recovered after {attempt + 1} attempts")
                        return
                        
            except Exception as e:
                logger.warning(f"Recovery attempt {attempt + 1} failed for {node.url}: {e}")
                
        logger.error(f"Node {node.url} failed to recover after {max_attempts} attempts")
        
    async def _update_nodes(self, discovered_nodes: List[Dict]):
        """Update nodes based on service discovery results.
        
        Args:
            discovered_nodes: List of node configurations from service discovery
        """
        # Track existing nodes by URL
        existing_urls = {node.url for node in self.nodes}
        discovered_urls = {node["url"] for node in discovered_nodes}
        
        # Add new nodes
        for node_config in discovered_nodes:
            if node_config["url"] not in existing_urls:
                new_node = ServiceNode(**node_config)
                self.nodes.append(new_node)
                self.circuit_breakers[new_node.url] = CircuitBreaker(
                    service_name=new_node.url,
                    failure_threshold=self.max_failures,
                    recovery_timeout=60.0,
                    half_open_max_requests=3
                )
                logger.info(f"Added new node: {new_node.url}")
                
        # Remove nodes that no longer exist
        self.nodes = [node for node in self.nodes if node.url in discovered_urls]
        # Clean up circuit breakers for removed nodes
        self.circuit_breakers = {
            url: cb for url, cb in self.circuit_breakers.items() 
            if url in discovered_urls
        }
            
    def get_next_node(self) -> Optional[ServiceNode]:
        """Get next available node using weighted round-robin."""
        healthy_nodes = [n for n in self.nodes if n.healthy]
        if not healthy_nodes:
            return None
            
        # Weighted random selection
        total_weight = sum(node.weight for node in healthy_nodes)
        r = random.uniform(0, total_weight)
        upto = 0
        
        for node in healthy_nodes:
            upto += node.weight
            if upto > r:
                return node
                
        return healthy_nodes[-1] if healthy_nodes else None

# High Availability Configuration
HA_CONFIG = {
    "nodes": [
        {"url": "http://validator1:8000", "weight": 100},
        {"url": "http://validator2:8000", "weight": 100},
        {"url": "http://validator3:8000", "weight": 100}
    ],
    "health_check": {
        "interval": 5.0,
        "max_failures": 3,
        "timeout": 2.0
    },
    "failover": {
        "enabled": True,
        "auto_recover": True
    }
}

# Global load balancer instance
load_balancer = LoadBalancer(
    nodes=HA_CONFIG["nodes"],
    health_check_interval=HA_CONFIG["health_check"]["interval"],
    max_failures=HA_CONFIG["health_check"]["max_failures"]
)