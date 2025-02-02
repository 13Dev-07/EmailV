"""
Catch-All Detector Module
Determines if a domain has a catch-all email configuration.
"""

import random
import string
import smtplib
import dns.resolver
from app.utils.exceptions import SMTPVerificationError
from app.utils.logger import setup_logger

logger = setup_logger('CatchAllDetector')

class CatchAllDetector:
    def __init__(self, cache_manager: Optional[CacheManager] = None):
        """Initialize catch-all detector with caching and SMTP pool.
        
        Args:
            cache_manager: Optional cache manager for caching results
        """
        self.cache_manager = cache_manager
        self.smtp_pool = SMTPConnectionPool(
            max_connections=5,
            connection_timeout=10,
            max_lifetime=3600
        )
        self.dns_resolver = DNSResolver()
        """
        Initializes the CatchAllDetector.
        """
        pass

    def is_catch_all(self, domain: str) -> bool:
        """Check if a domain has catch-all email configuration.
        
        Args:
            domain: Domain to check
            
        Returns:
            bool: True if domain accepts all emails, False otherwise
        """
        # Check cache first
        if self.cache_manager:
            cached_result = self.cache_manager.get(f"catch_all:{domain}")
            if cached_result is not None:
                return cached_result

        try:
            # Get MX records
            mx_records = self.get_mx_records(domain)
            if not mx_records:
                self._cache_result(domain, False)
                return False
                
            # Generate test email
            test_email = self.generate_random_email(domain)
            
            # Test against primary MX
            primary_mx = mx_records[0]
            is_catch_all = self._test_mx_catch_all(primary_mx, test_email)
            
            # Cache result
            self._cache_result(domain, is_catch_all)
            return is_catch_all
            
        except Exception as e:
            logger.error(f"Error checking catch-all for {domain}: {str(e)}")
            return False
        """
        Determines if the given domain has a catch-all email configuration.
        
        Args:
            domain (str): The domain to check.
        
        Returns:
            bool: True if it's a catch-all, False otherwise.
        
        Raises:
            SMTPVerificationError: If SMTP verification fails.
        """
        random_email = self.generate_random_email(domain)
        try:
            mx_record = self.get_mx_record(domain)
            logger.debug(f"MX Record for {domain}: {mx_record}")
            server = smtplib.SMTP(timeout=10)
            server.connect(mx_record)
            server.helo(server.local_hostname)  # Can be customized
            server.mail('no-reply@example.com')  # Sender email can be customized
            code, message = server.rcpt(random_email)
            server.quit()
            
            if code == 250:
                logger.info(f"Domain {domain} is a catch-all.")
                return True
            elif code == 550:
                logger.info(f"Domain {domain} is not a catch-all.")
                return False
            else:
                logger.warning(f"Unexpected SMTP response {code} for domain {domain}. Assuming not catch-all.")
                return False
        except SMTPVerificationError as e:
            logger.error(f"SMTP Verification Error for domain {domain}: {e.message}")
            raise e
        except Exception as e:
            logger.exception(f"Unexpected error during catch-all detection for domain {domain}: {e}")
            raise SMTPVerificationError(f"Unexpected error: {e}")

    def generate_random_email(self, domain: str) -> str:
        """
        Generates a random email address for testing catch-all.
        
        Args:
            domain (str): The domain to use.
        
        Returns:
            str: A randomly generated email address.
        """
        local_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{local_part}@{domain}"

    def get_mx_records(self, domain: str) -> List[str]:
        """Get MX records for a domain sorted by priority.
        
        Args:
            domain: Domain to check
            
        Returns:
            List of MX records sorted by priority
        """
        try:
            if self.cache_manager:
                cached = self.cache_manager.get(f"mx:{domain}")
                if cached is not None:
                    return cached
                    
            mx_records = []
            answers = self.dns_resolver.resolve(domain, 'MX')
            
            # Sort by priority (lowest first)
            sorted_records = sorted(
                [(answer.preference, str(answer.exchange).rstrip('.'))
                 for answer in answers]
            )
            
            mx_records = [record[1] for record in sorted_records]
            
            if self.cache_manager:
                self.cache_manager.set(f"mx:{domain}", mx_records, expire=3600)
                
            return mx_records
            
        except DNSException as e:
            logger.error(f"DNS error getting MX records for {domain}: {str(e)}")
            return []
        """
        Retrieves the primary MX record for the domain.
        
        Args:
            domain (str): The domain to query.
        
        Returns:
            str: The MX server address.
        
        Raises:
            SMTPVerificationError: If no MX records are found.
        """
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            mx_records = sorted([(r.preference, r.exchange.to_text()) for r in answers], key=lambda x: x[0])
            primary_mx = mx_records[0][1]
            return primary_mx
        except dns.resolver.NoAnswer:
            logger.error(f"No MX records found for domain: {domain}")
            raise SMTPVerificationError("No MX records found for domain.")
        except dns.resolver.NXDOMAIN:
            logger.error(f"Domain does not exist: {domain}")
            raise SMTPVerificationError("Domain does not exist.")
        except Exception as e:
            logger.exception(f"Error retrieving MX records for domain {domain}: {e}")
            raise SMTPVerificationError(f"Error retrieving MX records: {e}")