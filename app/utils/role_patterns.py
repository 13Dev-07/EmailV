"""Common patterns for detecting role-based email accounts."""

# Role-based email patterns that indicate non-personal accounts
ROLE_PATTERNS = {
    # Administrative roles
    r'^admin@',
    r'^administrator@', 
    r'^webmaster@',
    r'^postmaster@',
    r'^hostmaster@',
    r'^root@',
    r'^sysadmin@',

    # Support roles
    r'^support@',
    r'^help@',
    r'^helpdesk@',
    r'^servicedesk@',
    r'^techsupport@',
    r'^customerservice@',
    r'^feedback@',

    # Business functions
    r'^info@',
    r'^contact@',
    r'^enquiries?@',
    r'^sales@',
    r'^marketing@',
    r'^billing@',
    r'^accounts?@',
    r'^finance@',
    r'^orders?@',
    r'^purchasing@',
    
    # HR related
    r'^hr@',
    r'^jobs@',
    r'^careers@',
    r'^recruitment@',
    r'^hiring@',
    r'^personnel@',

    # Security roles
    r'^security@',
    r'^abuse@',
    r'^spam@',
    r'^phishing@',
    r'^privacy@',
    r'^compliance@',

    # Technical roles
    r'^noc@',
    r'^systems?@',
    r'^dev(eloper)?s?@',
    r'^it@',
    r'^hosting@',
    r'^domains?@',
    r'^dns@',

    # Generic roles
    r'^office@',
    r'^team@',
    r'^staff@',
    r'^general@',
    r'^mail@',
    r'^web@',
    r'^no-?reply@',
    r'^do-?not-?reply@',
    r'^automated@',
    r'^bot@',
    r'^mailer@'
}

# Optional role-based patterns that may be configurable
OPTIONAL_ROLE_PATTERNS = {
    r'^newsletter@',
    r'^subscribe@',
    r'^unsubscribe@',
    r'^list@',
    r'^alerts?@',
    r'^notifications?@',
    r'^news@',
    r'^press@',
    r'^media@',
    r'^events?@'
}