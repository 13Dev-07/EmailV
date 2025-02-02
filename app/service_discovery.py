"""Service discovery implementation for high availability cluster."""

import asyncio
import json
from typing import Dict, List, Optional
import aiohttp
import consul
import consul.aio
from logging import getLogger

logger = getLogger(__name__)

class ServiceRegistry:
    """Service registry using Consul for service discovery."""
    
    def __init__(
        self,
        consul_host: str = "localhost",
        consul_port: int = 8500,
        service_name: str = "email-validator",
        check_interval: str = "10s",
        deregister_after: str = "1m"
    ):
        """Initialize service registry.
        
        Args:
            consul_host: Consul server hostname
            consul_port: Consul server port
            service_name: Name of the service to register
            check_interval: Health check interval
            deregister_after: Time after which to deregister failing service
        """
        self.consul_host = consul_host
        self.consul_port = consul_port
        self.service_name = service_name
        self.check_interval = check_interval
        self.deregister_after = deregister_after
        self._consul: Optional[consul.aio.Consul] = None
        self._service_id: Optional[str] = None
        
    async def start(self):
        """Start the service registry client."""
        self._consul = consul.aio.Consul(
            host=self.consul_host,
            port=self.consul_port
        )
        
    async def stop(self):
        """Stop the service registry client."""
        if self._consul:
            await self._consul.agent.service.deregister(self._service_id)
            await self._consul.close()
            
    async def register_service(self, host: str, port: int, tags: List[str] = None):
        """Register service with Consul.
        
        Args:
            host: Service hostname
            port: Service port
            tags: Service tags for metadata
        """
        self._service_id = f"{self.service_name}-{host}-{port}"
        
        service_def = {
            "name": self.service_name,
            "service_id": self._service_id,
            "address": host,
            "port": port,
            "tags": tags or [],
            "check": {
                "http": f"http://{host}:{port}/health",
                "interval": self.check_interval,
                "deregister_critical_service_after": self.deregister_after
            }
        }
        
        await self._consul.agent.service.register(**service_def)
        logger.info(f"Registered service {self._service_id} with Consul")
        
    async def discover_services(self) -> List[Dict]:
        """Discover all healthy instances of the service.
        
        Returns:
            List of service instances with their metadata
        """
        index, services = await self._consul.health.service(
            self.service_name,
            passing=True
        )
        
        instances = []
        for service in services:
            service_data = service["Service"]
            instances.append({
                "url": f"http://{service_data['Address']}:{service_data['Port']}",
                "weight": 100,  # Default weight
                "tags": service_data.get("Tags", [])
            })
            
        return instances
        
    async def watch_services(self, callback):
        """Watch for service changes and notify callback.
        
        Args:
            callback: Async function to call when services change
        """
        index = None
        while True:
            try:
                index, services = await self._consul.health.service(
                    self.service_name,
                    index=index,
                    passing=True,
                    wait="30s"
                )
                instances = []
                for service in services:
                    service_data = service["Service"]
                    instances.append({
                        "url": f"http://{service_data['Address']}:{service_data['Port']}",
                        "weight": 100,
                        "tags": service_data.get("Tags", [])
                    })
                    
                await callback(instances)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error watching services: {e}")
                await asyncio.sleep(5)  # Backoff before retry