"""SMTP verification module for email validation."""

import smtplib
import socket
import logging
import asyncio
from prometheus_client import Summary
from app.monitoring.prometheus_metrics import (
    email_validation_duration_seconds,
    validation_errors_total,
    dns_resolution_duration_seconds
)
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import dns.resolver
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
from app.dns_resolver import DNSResolver, DNSRecord

logger = logging.getLogger(__name__)

@dataclass
class SMTPValidationResult:
    """Results of SMTP validation."""
    is_valid: bool
    error_message: Optional[str] = None
    smtp_response: Optional[str] = None
    mx_used: Optional[str] = None

from app.smtp_connection_pool import smtp_pool

class SMTPConnectionPool:
    """Deprecated: Use smtp_pool from smtp_connection_pool instead."""
    def __init__(self, *args, **kwargs):
        import warnings
        warnings.warn(
            "This SMTPConnectionPool is deprecated. Use smtp_pool from smtp_connection_pool instead.",
            DeprecationWarning
        )

    @asynccontextmanager
    async def get_connection(self, host: str, port: int = 25) -> smtplib.SMTP:
        """
        Get an SMTP connection from the pool.
        
        Args:
            host: SMTP server hostname.
            port: SMTP server port.
            
        Returns:
            SMTP connection.
        """
        async with self._semaphore:
            try:
                connection = await self._get_or_create_connection(host, port)
                yield connection
            finally:
                # Return connection to pool instead of closing
                if host in self._pool:
                    self._pool[host].append(connection)
                else:
                    self._pool[host] = [connection]

    async def _get_or_create_connection(self, host: str, port: int) -> smtplib.SMTP:
        """Get existing connection or create new one."""
        if host in self._pool and self._pool[host]:
            return self._pool[host].pop()
            
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor,
            self._create_connection,
            host,
            port
        )

    def _create_connection(self, host: str, port: int) -> smtplib.SMTP:
        """Create new SMTP connection."""
        smtp = smtplib.SMTP(timeout=self._timeout)
        smtp.set_debuglevel(0)
        smtp.connect(host, port)
        return smtp

    async def close_all(self):
        """Close all connections in the pool."""
        for host, connections in self._pool.items():
            for conn in connections:
                try:
                    conn.quit()
                except Exception as e:
                    logger.warning(f"Error closing SMTP connection to {host}: {str(e)}")
        self._pool.clear()
        self._executor.shutdown(wait=True)

class SMTPValidator:
    """Validates email addresses through SMTP verification with connection pooling and caching."""

    def __init__(
        self,
        dns_resolver: DNSResolver,
        redis_client: RedisClient,
        connection_timeout: float = 10.0,
        max_connections: int = 50,
        max_retries: int = 3,
        retry_delay: float = 2.0,
        cache_ttl: int = 86400  # Cache results for 24 hours
    ):
        """
        Initialize SMTP validator.
        
        Args:
            dns_resolver: DNS resolver for MX lookups.
            connection_timeout: Timeout for SMTP connections.
            max_connections: Maximum number of concurrent SMTP connections.
            max_retries: Maximum number of retry attempts.
            retry_delay: Delay between retries in seconds.
        """
        self.dns_resolver = dns_resolver
        self.redis_client = redis_client
        self.connection_timeout = connection_timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.cache_ttl = cache_ttl
        # Use the global connection pool
        self.connection_pool = smtp_pool  # Global instance from smtp_connection_pool

    async def verify_email(
        self,
        email: str,
        sender: str = "verify@example.com",
        use_cache: bool = True
    ) -> SMTPValidationResult:
        """
        Verify email address using SMTP with caching support.
        
        Args:
            email: Email address to verify.
            sender: Email address to use as MAIL FROM.
            use_cache: Whether to use cached results if available.
            
        Returns:
            SMTPValidationResult with verification details.
        """
        if use_cache:
            # Check cache first
            cache_key = f"email_validation:{email}"
            cached_result = await self.redis_client.get_cache(cache_key)
            if cached_result:
                return SMTPValidationResult(**cached_result)
        
        # Perform verification if not cached or cache disabled
        result = await self._verify_with_smtp(email, sender)
        
        if use_cache and result.is_valid:
            # Cache successful validations
            await self.redis_client.set_cache(
                cache_key,
                result.__dict__,
                expire_in=self.cache_ttl
            )
        
        return result
        """
        Verify email address through SMTP.
        
        Args:
            email: Email address to verify.
            sender: Email address to use as MAIL FROM.
            
        Returns:
            SMTPValidationResult with validation status.
        """
        domain = email.split('@')[1]
        
        try:
            # Get MX records
            mx_records = await self.dns_resolver.resolve_mx(domain)
            if not mx_records:
                return SMTPValidationResult(
                    is_valid=False,
                    error_message="No MX records found for domain"
                )

            # Sort MX records by priority
            mx_records.sort(key=lambda x: x.priority if x.priority is not None else 999)
            
            # Try each MX record in order
            last_error = None
            for mx in mx_records:
                try:
                    result = await self._verify_with_smtp(
                        mx.value,
                        email,
                        sender,
                        retries=self.max_retries
                    )
                    result.mx_used = mx.value
                    return result
                except Exception as e:
                    last_error = str(e)
                    logger.warning(f"SMTP verification failed for {email} using {mx.value}: {str(e)}")
                    continue

            return SMTPValidationResult(
                is_valid=False,
                error_message=f"All MX servers failed: {last_error}"
            )

        except Exception as e:
            return SMTPValidationResult(
                is_valid=False,
                error_message=f"SMTP verification failed: {str(e)}"
            )

    async def _verify_with_smtp(
        self,
        mx_host: str,
        email: str,
        sender: str,
        retries: int
    ) -> SMTPValidationResult:
        """
        Verify email with specific MX server.
        
        Args:
            mx_host: MX server hostname.
            email: Email to verify.
            sender: Sender email address.
            retries: Number of retry attempts.
            
        Returns:
            SMTPValidationResult with validation status.
        """
        last_error = None
        
        for attempt in range(retries):
            try:
                async with self.connection_pool.get_connection(mx_host) as smtp:
                    # Send HELO
                    smtp.ehlo_or_helo_if_needed()
                    
                    # Send MAIL FROM
                    code, message = smtp.mail(sender)
                    if code != 250:
                        return SMTPValidationResult(
                            is_valid=False,
                            error_message=f"MAIL FROM failed: {message.decode()}",
                            smtp_response=message.decode()
                        )
                    
                    # Send RCPT TO
                    code, message = smtp.rcpt(email)
                    message_str = message.decode()
                    
                    if code == 250:
                        return SMTPValidationResult(
                            is_valid=True,
                            smtp_response=message_str
                        )
                    elif code == 550:
                        return SMTPValidationResult(
                            is_valid=False,
                            error_message="Email address does not exist",
                            smtp_response=message_str
                        )
                    else:
                        return SMTPValidationResult(
                            is_valid=False,
                            error_message=f"RCPT TO failed with code {code}",
                            smtp_response=message_str
                        )
                        
            except Exception as e:
                last_error = str(e)
                if attempt < retries - 1:
                    await asyncio.sleep(self.retry_delay)
                continue

        return SMTPValidationResult(
            is_valid=False,
            error_message=f"Max retries exceeded: {last_error}"
        )

    async def close(self):
        """Close the validator and its connection pool."""
        await self.connection_pool.close_all()