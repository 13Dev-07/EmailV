"""Common patterns for detecting disposable email domains."""

# Patterns indicating temporary/disposable domains
DISPOSABLE_DOMAIN_PATTERNS = [
    r'temp',
    r'fake',
    r'disposable',
    r'trash',
    r'throw?away',
    r'tempmail',
    r'guerrilla',
    r'10minutemail',
    r'mailinator',
    r'tempinbox',
    r'yopmail',
    r'spam',
    r'junk',
]

# Common disposable email domain keywords
SUSPICIOUS_KEYWORDS = {
    'temp', 'fake', 'junk', 'spam', 'trash', 'throw', 'away', 
    'temporary', 'dump', 'random', 'burner', 'delete', 'disposable'
}

# Time-based patterns indicating temporary emails
TIME_BASED_PATTERNS = [
    r'\d+min(ute)?s?',  # e.g., 10minute, 15min
    r'\d+hour',
    r'\d+sec(ond)?s?',
    r'temp\d+',
]

# Domain generation patterns
GENERATED_PATTERNS = [
    r'[a-z0-9]{8,}\.com',  # Long random strings
    r'[0-9]{6,}mail',      # Number-based mail domains
    r'mail[0-9]{4,}',      # mail followed by numbers
]

# Commonly used free email providers (not disposable)
LEGITIMATE_EMAIL_PROVIDERS = {
    'gmail.com',
    'yahoo.com',
    'outlook.com',
    'hotmail.com',
    'aol.com',
    'protonmail.com',
    'icloud.com',
    'mail.com',
    'zoho.com',
    'live.com'
}