"""
Domain Reputation Module
Evaluates the reputation of an email's domain.
"""

import requests
import os
from app.utils.cache_manager import CacheManager
from app.utils.logger import setup_logger

logger = setup_logger('DomainReputation')

DOMAIN_REPUTATION_API_URL = os.getenv("DOMAIN_REPUTATION_API_URL", "https://api.domain-reputation.com/check")

def get_domain_reputation(domain: str) -> int:
    """
    Retrieves the reputation score of the given domain.

    Args:
        domain (str): The domain to assess.

    Returns:
        int: Reputation score (0-100, where higher is better).
    """
    cache = CacheManager()
    cache_key = f"domain_reputation:{domain}"
    cached_score = cache.get_cache(cache_key)
    
    if cached_score is not None:
        logger.debug(f"Cache hit for domain reputation: {domain} -> {cached_score['reputation_score']}")
        return cached_score["reputation_score"]
    
    try:
        response = requests.get(f"{DOMAIN_REPUTATION_API_URL}?domain={domain}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            score = data.get("reputation_score", 50)  # Default to neutral score
            cache.set_cache(cache_key, {"reputation_score": score}, expire=3600)
            logger.info(f"Retrieved domain reputation for {domain}: {score}")
            return score
        else:
            logger.warning(f"Domain reputation API returned status {response.status_code} for domain: {domain}")
            return 50  # Neutral score on API failure
    except requests.RequestException as e:
        logger.error(f"Error fetching domain reputation for {domain}: {e}")
        return 50  # Neutral score on exception