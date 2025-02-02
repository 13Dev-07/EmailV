"""
Cache Manager Module
Manages caching mechanisms to optimize performance.
"""

import redis
import json
import os
from typing import Optional
from app.utils.logger import setup_logger

logger = setup_logger('CacheManager')

class CacheManager:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """
        Initializes the CacheManager with Redis connection.
        
        Args:
            host (str): Redis server host.
            port (int): Redis server port.
            db (int): Redis database number.
        """
        redis_host = os.getenv("REDIS_HOST", host)
        redis_port = int(os.getenv("REDIS_PORT", port))
        redis_db = int(os.getenv("REDIS_DB", db))
        
        try:
            self.client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
            # Test the connection
            self.client.ping()
            logger.info(f"Connected to Redis at {redis_host}:{redis_port}, DB: {redis_db}")
        except redis.exceptions.ConnectionError as e:
            logger.error(f"Redis connection failed: {e}")
            raise e
    
    def set_cache(self, key: str, value: dict, expire: int = 3600) -> bool:
        """
        Stores data in the cache.
        
        Args:
            key (str): Cache key.
            value (dict): Data to cache.
            expire (int): Expiration time in seconds.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            serialized_value = json.dumps(value)
            self.client.setex(key, expire, serialized_value)
            logger.debug(f"Set cache for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to set cache for key {key}: {e}")
            return False
    
    def get_cache(self, key: str) -> Optional[dict]:
        """
        Retrieves data from the cache.
        
        Args:
            key (str): Cache key.
        
        Returns:
            Optional[dict]: Cached data if available, else None.
        """
        try:
            serialized_value = self.client.get(key)
            if serialized_value:
                logger.debug(f"Cache hit for key: {key}")
                return json.loads(serialized_value)
            else:
                logger.debug(f"Cache miss for key: {key}")
                return None
        except Exception as e:
            logger.error(f"Failed to get cache for key {key}: {e}")
            return None
    
    def delete_cache(self, key: str) -> bool:
        """
        Deletes a cached key.
        
        Args:
            key (str): Cache key to delete.
        
        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            result = self.client.delete(key)
            if result:
                logger.debug(f"Deleted cache for key: {key}")
                return True
            else:
                logger.debug(f"No cache to delete for key: {key}")
                return False
        except Exception as e:
            logger.error(f"Failed to delete cache for key {key}: {e}")
            return False