"""
Constants used throughout the email validation system.
"""

# RFC 5322 compliant regex patterns
ATEXT = r'[a-zA-Z0-9!#$%&\'*+\-/=?^_`{|}~]'
DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'
QUOTED_PAIR = r'\\[\x21-\x7E ]'
QTEXT = r'[\x21\x23-\x5B\x5D-\x7E]'
QCONTENT = f'(?:{QTEXT}|{QUOTED_PAIR})'
QUOTED_STRING = f'"(?:{QCONTENT})*"'
LOCAL_PART = f'(?:{DOT_ATOM_TEXT}|{QUOTED_STRING})'
DOMAIN = r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?'
EMAIL_REGEX = f'^{LOCAL_PART}@{DOMAIN}$'

# IDNA (Internationalized Domain Names) maximum length
DOMAIN_MAX_LENGTH = 255
LOCAL_PART_MAX_LENGTH = 64

# Error messages
ERR_INVALID_SYNTAX = "Invalid email syntax"
ERR_LOCAL_TOO_LONG = "Local part exceeds maximum length of 64 characters"
ERR_DOMAIN_TOO_LONG = "Domain exceeds maximum length of 255 characters"
ERR_INVALID_LOCAL_CHARS = "Local part contains invalid characters"
ERR_INVALID_DOMAIN_CHARS = "Domain contains invalid characters"
ERR_CONSECUTIVE_DOTS = "Consecutive dots are not allowed"
ERR_DOT_START_END = "Email cannot start or end with a dot"