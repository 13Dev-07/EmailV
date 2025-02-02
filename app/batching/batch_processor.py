"""Async batch processing implementation."""
import asyncio
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from app.smtp_validator import SMTPValidator
from app.caching.redis_client import RedisClient

logger = logging.getLogger(__name__)

class BatchProcessor:
    """Handles async batch processing of email validations."""
    
    def __init__(
        self,
        smtp_validator: SMTPValidator,
        redis_client: RedisClient,
        max_batch_size: int = 100,
        batch_timeout: float = 30.0
    ):
        """
        Initialize batch processor.
        
        Args:
            smtp_validator: SMTP validator instance.
            redis_client: Redis client for caching results.
            max_batch_size: Maximum size of a batch.
            batch_timeout: Maximum time to wait for batch completion in seconds.
        """
        self.smtp_validator = smtp_validator
        self.redis = redis_client
        self.max_batch_size = max_batch_size
        self.batch_timeout = batch_timeout
        self._current_batch: List[str] = []
        self._batch_results: Dict[str, Any] = {}
        self._batch_lock = asyncio.Lock()
        self._processing = False
        
    async def add_to_batch(self, email: str) -> str:
        """
        Add email to current batch and return batch ID.
        
        Args:
            email: Email address to validate.
            
        Returns:
            Batch ID for tracking results.
        """
        batch_id = f"batch:{datetime.now().timestamp()}:{email}"
        
        async with self._batch_lock:
            self._current_batch.append(email)
            self._batch_results[batch_id] = None
            
            if len(self._current_batch) >= self.max_batch_size:
                await self._process_batch()
                
        return batch_id
        
    async def get_result(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """
        Get result for a batch item.
        
        Args:
            batch_id: Batch ID to look up.
            
        Returns:
            Validation result if available, None if still processing.
        """
        return self._batch_results.get(batch_id)
        
    async def start(self):
        """Start the batch processor."""
        self._processing = True
        asyncio.create_task(self._batch_monitor())
        
    async def stop(self):
        """Stop the batch processor."""
        self._processing = False
        if self._current_batch:
            await self._process_batch()
            
    async def _batch_monitor(self):
        """Monitor batch processing and trigger processing on timeout."""
        while self._processing:
            await asyncio.sleep(self.batch_timeout)
            if self._current_batch:
                await self._process_batch()
                
    async def _process_batch(self):
        """Process current batch of emails."""
        async with self._batch_lock:
            if not self._current_batch:
                return
                
            batch = self._current_batch.copy()
            self._current_batch.clear()
            
        try:
            tasks = [
                self.smtp_validator.verify_email(email)
                for email in batch
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for email, result in zip(batch, results):
                batch_id = f"batch:{datetime.now().timestamp()}:{email}"
                if isinstance(result, Exception):
                    self._batch_results[batch_id] = {
                        "error": str(result),
                        "status": "error"
                    }
                else:
                    self._batch_results[batch_id] = {
                        "result": result.__dict__,
                        "status": "completed"
                    }
                    
        except Exception as e:
            logger.error(f"Batch processing error: {str(e)}")
            for email in batch:
                batch_id = f"batch:{datetime.now().timestamp()}:{email}"
                self._batch_results[batch_id] = {
                    "error": str(e),
                    "status": "error"
                }