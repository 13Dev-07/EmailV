"""
Constants related to domain analysis and categorization.
"""

# Lists of known providers
DISPOSABLE_DOMAINS_FILE = "data/disposable_domains.txt"
FREE_EMAIL_DOMAINS_FILE = "data/free_email_domains.txt"
ROLE_ACCOUNTS = {
    "admin", "administrator", "webmaster", "hostmaster", "postmaster",
    "abuse", "support", "sales", "info", "contact", "help", "no-reply",
    "noreply", "marketing", "office", "hr", "jobs", "billing"
}

# Reputation thresholds
REPUTATION_THRESHOLD_HIGH = 80
REPUTATION_THRESHOLD_MEDIUM = 50
REPUTATION_THRESHOLD_LOW = 30

# Cache TTLs (in seconds)
DISPOSABLE_CACHE_TTL = 86400  # 24 hours
REPUTATION_CACHE_TTL = 3600   # 1 hour
TYPO_CACHE_TTL = 86400       # 24 hours

# Error messages
ERR_DISPOSABLE_EMAIL = "Email domain is from a disposable provider"
ERR_LOW_REPUTATION = "Domain has low reputation score"
ERR_ROLE_ACCOUNT = "Email appears to be a role account"
ERR_TYPO_DETECTED = "Possible typo detected in domain"

# Reputation factors
REPUTATION_FACTORS = {
    "has_mx": 20,
    "has_spf": 10,
    "has_dmarc": 10,
    "has_website": 10,
    "is_free_provider": -5,
    "recent_spam": -30,
    "blacklisted": -50
}

# Common typos
COMMON_TYPOS = {
    "gmail.com": ["gmal.com", "gmial.com", "gmai.com", "gamil.com"],
    "yahoo.com": ["yaho.com", "yahooo.com", "yaaho.com", "yhoo.com"],
    "hotmail.com": ["hotnail.com", "hotmal.com", "hotmai.com", "hotmial.com"],
    "outlook.com": ["outlok.com", "outloot.com", "outlock.com", "outlool.com"]
}