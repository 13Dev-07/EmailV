"""
SMTP Verifier Module
Provides functionality for SMTP-based email validation.

This module implements SMTP verification with:
- Connection pooling for improved performance
- Retry mechanisms for reliability
- Proper timeout handling
- Comprehensive SMTP response handling
"""

import asyncio
import socket
import aiosmtplib
from typing import Optional, Dict, List
from contextlib import asynccontextmanager
from app.utils.smtp_constants import (
    SMTP_PORT, SMTP_TIMEOUT, MAX_RETRIES, RETRY_DELAY,
    MAX_POOL_SIZE, CONNECTION_TIMEOUT, POOL_TIMEOUT,
    SMTP_OK, SMTP_READY, SMTP_AUTH_SUCCESS, SMTP_TEMP_ERROR,
    SMTP_MAILBOX_FULL, SMTP_MAILBOX_NOT_FOUND, SMTP_RELAY_DENIED,
    ERR_CONNECTION_FAILED, ERR_TIMEOUT, ERR_MAILBOX_NOT_FOUND,
    ERR_MAILBOX_FULL, ERR_DOMAIN_NOT_FOUND, ERR_RELAY_DENIED,
    ERR_POOL_TIMEOUT, ERR_TOO_MANY_ERRORS
)
from app.utils.exceptions import SMTPError
from app.utils.validation_result import ValidationResult

class SMTPVerifier:
    """SMTP verification with connection pooling and retry logic."""
    
    def __init__(self):
        """Initialize the SMTP verifier with connection pool."""
        self.connection_pool: Dict[str, List[aiosmtplib.SMTP]] = {}
        self.pool_semaphore = asyncio.Semaphore(MAX_POOL_SIZE)
        self.local_hostname = socket.gethostname()

    async def verify_smtp(self, email: str, domain: str) -> ValidationResult:
        """
        Verifies email existence using SMTP with connection pooling and retries.
        
        Args:
            email (str): The email address to verify
            domain (str): The domain to connect to
            
        Returns:
            ValidationResult: Object containing validation results
            
        Raises:
            SMTPError: If verification fails with an unrecoverable error
        """
        result = ValidationResult(email)
        
        for attempt in range(MAX_RETRIES):
            try:
                async with self._get_connection(domain) as client:
                    # Send MAIL FROM command
                    response = await client.mail(f"verify@{self.local_hostname}")
                    if response[0] != SMTP_OK:
                        result.add_error(ERR_RELAY_DENIED)
                        return result
                        
                    # Send RCPT TO command
                    response = await client.rcpt(email)
                    if response[0] == SMTP_OK:
                        result.smtp_check = True
                        result.is_valid = True
                        return result
                    elif response[0] in [SMTP_MAILBOX_NOT_FOUND, SMTP_RELAY_DENIED]:
                        result.add_error(ERR_MAILBOX_NOT_FOUND)
                        return result
                    elif response[0] == SMTP_MAILBOX_FULL:
                        result.add_warning(ERR_MAILBOX_FULL)
                        result.smtp_check = True
                        result.is_valid = True
                        return result
                        
            except aiosmtplib.SMTPTimeoutError:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY)
                    continue
                result.add_error(ERR_TIMEOUT)
            except aiosmtplib.SMTPConnectError:
                result.add_error(ERR_CONNECTION_FAILED)
            except Exception as e:
                result.add_error(str(e))
                
        return result
    
    @asynccontextmanager
    async def _get_connection(self, domain: str):
        """Get a connection from the pool or create a new one."""
        async with self.pool_semaphore:
            if domain in self.connection_pool and self.connection_pool[domain]:
                client = self.connection_pool[domain].pop()
            else:
                client = aiosmtplib.SMTP(
                    hostname=domain,
                    port=SMTP_PORT,
                    timeout=SMTP_TIMEOUT,
                    use_tls=False
                )
                
            try:
                if not client.is_connected:
                    await client.connect()
                yield client
                
                # Reset the connection and return it to the pool
                try:
                    await client.rset()
                    if domain not in self.connection_pool:
                        self.connection_pool[domain] = []
                    self.connection_pool[domain].append(client)
                except Exception:
                    # If reset fails, close the connection
                    try:
                        await client.quit()
                    except Exception:
                        pass
                        
            except Exception as e:
                # Ensure connection is closed on error
                try:
                    await client.quit()
                except Exception:
                    pass
                raise SMTPError(str(e))
    
    async def cleanup(self):
        """Close all connections in the pool."""
        for domain, connections in self.connection_pool.items():
            for client in connections:
                try:
                    await client.quit()
                except Exception:
                    pass
            self.connection_pool[domain] = []