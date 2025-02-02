"""
SMTP-related constants for email validation system.
"""

# SMTP connection settings
SMTP_PORT = 25
SMTP_TIMEOUT = 10  # seconds
MAX_RETRIES = 2
RETRY_DELAY = 2  # seconds
MAX_POOL_SIZE = 20
CONNECTION_TIMEOUT = 30  # seconds
POOL_TIMEOUT = 5  # seconds

# SMTP commands
SMTP_HELO = "HELO {}"
SMTP_EHLO = "EHLO {}"
SMTP_MAIL = "MAIL FROM:<{}>\\r\\n"
SMTP_RCPT = "RCPT TO:<{}>\\r\\n"
SMTP_RSET = "RSET\\r\\n"
SMTP_QUIT = "QUIT\\r\\n"

# SMTP response codes
SMTP_OK = 250
SMTP_READY = 220
SMTP_BYE = 221
SMTP_AUTH_SUCCESS = 235
SMTP_TEMP_ERROR = 421
SMTP_MAILBOX_FULL = 452
SMTP_AUTH_REQUIRED = 530
SMTP_MAILBOX_UNAVAILABLE = 550
SMTP_MAILBOX_NOT_FOUND = 551
SMTP_RELAY_DENIED = 554

# Error messages
ERR_CONNECTION_FAILED = "Failed to establish SMTP connection"
ERR_TIMEOUT = "SMTP operation timed out"
ERR_MAILBOX_NOT_FOUND = "Mailbox does not exist"
ERR_MAILBOX_FULL = "Mailbox is full"
ERR_DOMAIN_NOT_FOUND = "Domain not found"
ERR_RELAY_DENIED = "Relay denied"
ERR_POOL_TIMEOUT = "Connection pool timeout"
ERR_TOO_MANY_ERRORS = "Too many SMTP errors"