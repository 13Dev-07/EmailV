/**
 * /validation/email-validator.js
 * Sacred Email Validation System
 * Version: 1.0.0
 */

const EmailValidator = (function() {
    'use strict';

    /**
     * Email Validation Constants
     */
    const EMAIL_CONSTANTS = {
        // Maximum lengths based on standards
        MAX_LENGTHS: {
            TOTAL: 254,        // RFC 5321
            LOCAL_PART: 64,    // RFC 5321
            DOMAIN: 255,       // RFC 1035
            LABEL: 63         // RFC 1035
        },

        // Minimum lengths based on practical usage
        MIN_LENGTHS: {
            TOTAL: 3,         // a@b
            LOCAL_PART: 1,
            DOMAIN: 1,
            TLD: 2
        },

        // Regular expressions for different parts
        REGEX: {
            // RFC 5322 Official Standard
            RFC_5322: new RegExp([
                '^',
                '(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*',  // Local part
                '|"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]',      // Quoted local part
                '|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*")',                              // Escaped characters
                '@',
                '(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?',  // Domain
                '|\\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}',            // IPv4
                '(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])',                           // IPv4 continuation
                '|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]',  // IPv6
                '|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])',                             // IPv6 continuation
                '$'
            ].join(''), 'i'),

            // Simplified pattern for quick checks
            QUICK: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,

            // International email (IDN support)
            INTERNATIONAL: new RegExp([
                '^',
                '[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+',
                '@',
                '[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?',
                '(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*',
                '$'
            ].join(''))
        },

        // Common disposable email domains
        DISPOSABLE_DOMAINS: new Set([
            'tempmail.com',
            'throwawaymail.com'
            // ... more domains would be loaded from a maintained list
        ]),

        // Role-based email prefixes to flag
        ROLE_ADDRESSES: new Set([
            'admin',
            'administrator',
            'webmaster',
            'info',
            'support',
            'noreply',
            'no-reply'
            // ... more role-based prefixes
        ])
    };

    /**
     * Validation Result Class
     */
    class EmailValidationResult {
        constructor(email) {
            this.email = email;
            this.isValid = false;
            this.normalizedEmail = '';
            this.errors = [];
            this.warnings = [];
            this.details = {};
        }

        addError(code, message) {
            this.errors.push({ code, message });
            this.isValid = false;
        }

        addWarning(code, message) {
            this.warnings.push({ code, message });
        }

        setDetails(details) {
            this.details = { ...this.details, ...details };
        }
    }

    /**
     * Email Parts Analysis
     */
    class EmailAnalyzer {
        constructor(email) {
            this.email = email;
            this.parts = this.parseEmail(email);
        }

        parseEmail(email) {
            const [localPart, domain] = email.split('@');
            return {
                localPart,
                domain,
                tld: domain?.split('.').pop(),
                labels: domain?.split('.') || []
            };
        }

        analyzeLocalPart() {
            const { localPart } = this.parts;
            
            return {
                length: localPart.length,
                hasQuotes: localPart.startsWith('"') && localPart.endsWith('"'),
                containsUnicode: /[^\x00-\x7F]/.test(localPart),
                isRoleBased: EMAIL_CONSTANTS.ROLE_ADDRESSES.has(localPart.toLowerCase()),
                specialChars: (localPart.match(/[^a-zA-Z0-9]/g) || []).join('')
            };
        }

        analyzeDomain() {
            const { domain, labels } = this.parts;
            
            return {
                length: domain.length,
                labelCount: labels.length,
                isIp: this.isIpAddress(domain),
                isPunycode: domain.startsWith('xn--'),
                containsUnicode: /[^\x00-\x7F]/.test(domain),
                isDisposable: EMAIL_CONSTANTS.DISPOSABLE_DOMAINS.has(domain.toLowerCase())
            };
        }

        isIpAddress(domain) {
            return /^\[.*\]$/.test(domain) || // IPv6
                   /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/.test(domain); // IPv4
        }
    }

    /**
     * Validation Methods
     */
    const validationMethods = {
        /**
         * Comprehensive email validation
         * @param {string} email - Email to validate
         * @param {Object} options - Validation options
         * @returns {EmailValidationResult} Validation result
         */
        validate(email, options = {}) {
            const result = new EmailValidationResult(email);
            
            try {
                // Quick format check
                if (!this.quickFormatCheck(email)) {
                    result.addError('FORMAT', 'Invalid email format');
                    return result;
                }

                // Normalize email
                const normalizedEmail = this.normalizeEmail(email);
                result.normalizedEmail = normalizedEmail;

                // Analyze email parts
                const analyzer = new EmailAnalyzer(normalizedEmail);
                const localPartAnalysis = analyzer.analyzeLocalPart();
                const domainAnalysis = analyzer.analyzeDomain();

                // Store analysis details
                result.setDetails({
                    localPart: localPartAnalysis,
                    domain: domainAnalysis
                });

                // Perform comprehensive validation
                this.validateLength(normalizedEmail, result);
                this.validateLocalPart(localPartAnalysis, result);
                this.validateDomain(domainAnalysis, result);
                this.validateSyntax(normalizedEmail, result);

                // Additional checks based on options
                if (options.checkDisposable && domainAnalysis.isDisposable) {
                    result.addWarning('DISPOSABLE', 'Disposable email address detected');
                }

                if (options.checkRoleBased && localPartAnalysis.isRoleBased) {
                    result.addWarning('ROLE_BASED', 'Role-based email address detected');
                }

                // Set valid if no errors
                result.isValid = result.errors.length === 0;

            } catch (error) {
                result.addError('SYSTEM', 'Validation system error');
                if (SacredCore.errors) {
                    SacredCore.errors.handle(error);
                }
            }

            return result;
        },

        /**
         * Quick format check
         * @param {string} email - Email to check
         * @returns {boolean} Is valid format
         */
        quickFormatCheck(email) {
            return typeof email === 'string' && 
                   EMAIL_CONSTANTS.REGEX.QUICK.test(email);
        },

        /**
         * Normalize email address
         * @param {string} email - Email to normalize
         * @returns {string} Normalized email
         */
        normalizeEmail(email) {
            return email.trim().toLowerCase();
        },

        /**
         * Validate email length
         * @param {string} email - Email to validate
         * @param {EmailValidationResult} result - Validation result
         */
        validateLength(email, result) {
            const { MAX_LENGTHS, MIN_LENGTHS } = EMAIL_CONSTANTS;
            const [localPart, domain] = email.split('@');

            if (email.length > MAX_LENGTHS.TOTAL) {
                result.addError('LENGTH', 'Email exceeds maximum length');
            }

            if (localPart.length > MAX_LENGTHS.LOCAL_PART) {
                result.addError('LOCAL_LENGTH', 'Local part exceeds maximum length');
            }

            if (domain.length > MAX_LENGTHS.DOMAIN) {
                result.addError('DOMAIN_LENGTH', 'Domain exceeds maximum length');
            }

            if (email.length < MIN_LENGTHS.TOTAL) {
                result.addError('MIN_LENGTH', 'Email is too short');
            }
        },

        /**
         * Validate local part
         * @param {Object} analysis - Local part analysis
         * @param {EmailValidationResult} result - Validation result
         */
        validateLocalPart(analysis, result) {
            if (analysis.containsUnicode) {
                result.addWarning('UNICODE_LOCAL', 'Local part contains Unicode characters');
            }

            if (analysis.specialChars.includes('..')) {
                result.addError('CONSECUTIVE_DOTS', 'Consecutive dots not allowed');
            }

            if (analysis.hasQuotes) {
                result.addWarning('QUOTED_LOCAL', 'Quoted local part detected');
            }
        },

        /**
         * Validate domain
         * @param {Object} analysis - Domain analysis
         * @param {EmailValidationResult} result - Validation result
         */
        validateDomain(analysis, result) {
            if (analysis.isIp) {
                result.addWarning('IP_DOMAIN', 'IP address used as domain');
            }

            if (analysis.containsUnicode && !analysis.isPunycode) {
                result.addWarning('UNICODE_DOMAIN', 'Domain contains Unicode characters');
            }

            if (analysis.labelCount < 2) {
                result.addError('DOMAIN_PARTS', 'Invalid domain structure');
            }

            analysis.labels.forEach(label => {
                if (label.length > EMAIL_CONSTANTS.MAX_LENGTHS.LABEL) {
                    result.addError('LABEL_LENGTH', 'Domain label exceeds maximum length');
                }
            });
        },

        /**
         * Validate email syntax
         * @param {string} email - Email to validate
         * @param {EmailValidationResult} result - Validation result
         */
        validateSyntax(email, result) {
            if (!EMAIL_CONSTANTS.REGEX.RFC_5322.test(email)) {
                result.addError('SYNTAX', 'Email does not comply with RFC 5322');
            }
        }
    };
// Adding to email-validator.js...

/**
 * DNS Validation System
 */
const DNSValidator = {
    // Cache for DNS results to prevent redundant lookups
    cache: new Map(),
    
    // Cache TTL in milliseconds (1 hour)
    cacheTTL: 3600000,

    /**
     * DNS Record Types
     */
    RECORD_TYPES: {
        A: 'A',
        MX: 'MX',
        CNAME: 'CNAME',
        TXT: 'TXT',
        NS: 'NS'
    },

    /**
     * Validate domain's DNS records
     * @param {string} domain - Domain to validate
     * @returns {Promise<Object>} DNS validation results
     */
    async validateDomain(domain) {
        try {
            // Check cache first
            const cached = this.getCachedResult(domain);
            if (cached) return cached;

            // Initialize result object
            const result = {
                hasDNS: false,
                hasMX: false,
                hasValidA: false,
                mxRecords: [],
                aRecords: [],
                timestamp: Date.now(),
                responseTime: 0
            };

            const startTime = performance.now();

            // Perform DNS lookups in parallel
            const [mxRecords, aRecords] = await Promise.all([
                this.resolveMX(domain),
                this.resolveA(domain)
            ]);

            result.responseTime = performance.now() - startTime;

            // Process MX records
            if (mxRecords && mxRecords.length > 0) {
                result.hasMX = true;
                result.mxRecords = this.normalizeMXRecords(mxRecords);
            }

            // Process A records
            if (aRecords && aRecords.length > 0) {
                result.hasValidA = true;
                result.aRecords = aRecords;
            }

            // Domain has valid DNS if it has either MX or A records
            result.hasDNS = result.hasMX || result.hasValidA;

            // Cache the result
            this.cacheResult(domain, result);

            return result;

        } catch (error) {
            // Handle specific DNS errors
            return this.handleDNSError(error, domain);
        }
    },

    /**
     * Resolve MX records
     * @param {string} domain - Domain to check
     * @returns {Promise<Array>} MX records
     */
    async resolveMX(domain) {
        return new Promise((resolve, reject) => {
            if (typeof window !== 'undefined') {
                // Browser environment - Use DNS over HTTPS
                this.resolveMXBrowser(domain)
                    .then(resolve)
                    .catch(reject);
            } else {
                // Node.js environment - Use dns module
                const dns = require('dns').promises;
                dns.resolveMx(domain)
                    .then(resolve)
                    .catch(reject);
            }
        });
    },

    /**
     * Resolve MX records in browser using DNS over HTTPS
     * @param {string} domain - Domain to check
     * @returns {Promise<Array>} MX records
     */
    async resolveMXBrowser(domain) {
        const response = await fetch(
            `https://dns.google/resolve?name=${domain}&type=MX`
        );
        const data = await response.json();

        if (!data.Answer) return [];

        return data.Answer
            .filter(record => record.type === 15) // MX record type
            .map(record => {
                const [priority, exchange] = record.data.split(' ');
                return { priority: parseInt(priority), exchange };
            });
    },

    /**
     * Resolve A records
     * @param {string} domain - Domain to check
     * @returns {Promise<Array>} A records
     */
    async resolveA(domain) {
        return new Promise((resolve, reject) => {
            if (typeof window !== 'undefined') {
                // Browser environment - Use DNS over HTTPS
                this.resolveABrowser(domain)
                    .then(resolve)
                    .catch(reject);
            } else {
                // Node.js environment - Use dns module
                const dns = require('dns').promises;
                dns.resolve4(domain)
                    .then(resolve)
                    .catch(reject);
            }
        });
    },

    /**
     * Resolve A records in browser using DNS over HTTPS
     * @param {string} domain - Domain to check
     * @returns {Promise<Array>} A records
     */
    async resolveABrowser(domain) {
        const response = await fetch(
            `https://dns.google/resolve?name=${domain}&type=A`
        );
        const data = await response.json();

        if (!data.Answer) return [];

        return data.Answer
            .filter(record => record.type === 1) // A record type
            .map(record => record.data);
    },

    /**
     * Normalize MX records
     * @param {Array} records - Raw MX records
     * @returns {Array} Normalized MX records
     */
    normalizeMXRecords(records) {
        return records
            .sort((a, b) => a.priority - b.priority)
            .map(record => ({
                priority: record.priority,
                exchange: record.exchange.toLowerCase(),
                isGoogleWorkspace: this.isGoogleWorkspace(record.exchange),
                isMicrosoft365: this.isMicrosoft365(record.exchange),
                isPopular: this.isPopularEmailProvider(record.exchange)
            }));
    },

    /**
     * Check if MX record belongs to Google Workspace
     * @param {string} exchange - MX exchange
     * @returns {boolean} Is Google Workspace
     */
    isGoogleWorkspace(exchange) {
        return /aspmx\.l\.google\.com$/i.test(exchange) ||
               /googlemail\.com$/i.test(exchange);
    },

    /**
     * Check if MX record belongs to Microsoft 365
     * @param {string} exchange - MX exchange
     * @returns {boolean} Is Microsoft 365
     */
    isMicrosoft365(exchange) {
        return /protection\.outlook\.com$/i.test(exchange);
    },

    /**
     * Check if MX record belongs to popular email provider
     * @param {string} exchange - MX exchange
     * @returns {boolean} Is popular provider
     */
    isPopularEmailProvider(exchange) {
        const popularProviders = [
            'google.com',
            'outlook.com',
            'yahoo.com',
            'protonmail.com',
            'zoho.com'
        ];
        return popularProviders.some(provider => 
            exchange.toLowerCase().includes(provider));
    },

    /**
     * Handle DNS errors
     * @param {Error} error - DNS error
     * @param {string} domain - Domain being checked
     * @returns {Object} Error result
     */
    handleDNSError(error, domain) {
        const result = {
            hasDNS: false,
            hasMX: false,
            hasValidA: false,
            error: true,
            errorCode: 'DNS_ERROR',
            errorMessage: error.message,
            timestamp: Date.now()
        };

        // Specific error handling
        if (error.code === 'ENOTFOUND') {
            result.errorCode = 'DOMAIN_NOT_FOUND';
            result.errorMessage = `Domain ${domain} does not exist`;
        } else if (error.code === 'ETIMEDOUT') {
            result.errorCode = 'DNS_TIMEOUT';
            result.errorMessage = `DNS lookup timeout for ${domain}`;
        }

        return result;
    },

    /**
     * Cache management methods
     */
    getCachedResult(domain) {
        const cached = this.cache.get(domain);
        if (cached && (Date.now() - cached.timestamp) < this.cacheTTL) {
            return cached;
        }
        this.cache.delete(domain);
        return null;
    },

    cacheResult(domain, result) {
        this.cache.set(domain, result);
        
        // Clean old cache entries
        if (this.cache.size > 1000) {
            const oldestAllowed = Date.now() - this.cacheTTL;
            for (const [key, value] of this.cache) {
                if (value.timestamp < oldestAllowed) {
                    this.cache.delete(key);
                }
            }
        }
    }
};

// Enhance EmailValidator with DNS validation
Object.assign(validationMethods, {
    /**
     * Validate email with DNS checks
     * @param {string} email - Email to validate
     * @param {Object} options - Validation options
     * @returns {Promise<EmailValidationResult>} Validation result
     */
    async validateWithDNS(email, options = {}) {
        // First perform standard validation
        const result = this.validate(email, options);
        
        // If basic validation failed, no need for DNS checks
        if (!result.isValid) {
            return result;
        }

        try {
            // Extract domain and perform DNS validation
            const domain = email.split('@')[1];
            const dnsResult = await DNSValidator.validateDomain(domain);

            // Add DNS validation details
            result.setDetails({
                dns: dnsResult
            });

            // Update validation status based on DNS results
            if (!dnsResult.hasDNS) {
                result.addError('DNS', 'Domain has no valid DNS records');
                result.isValid = false;
            } else if (!dnsResult.hasMX && !options.allowNoMX) {
                result.addError('MX', 'Domain has no MX records');
                result.isValid = false;
            }

            // Add warnings for specific cases
            if (dnsResult.hasMX) {
                const primaryMX = dnsResult.mxRecords[0];
                if (primaryMX.isPopular) {
                    result.addWarning('POPULAR_PROVIDER', 
                        'Email uses popular provider');
                }
                if (primaryMX.isGoogleWorkspace) {
                    result.addWarning('GOOGLE_WORKSPACE', 
                        'Email uses Google Workspace');
                }
                if (primaryMX.isMicrosoft365) {
                    result.addWarning('MICROSOFT_365', 
                        'Email uses Microsoft 365');
                }
            }

        } catch (error) {
            result.addError('DNS_CHECK', 'DNS validation failed');
            result.isValid = false;
            
            if (SacredCore.errors) {
                SacredCore.errors.handle(error);
            }
        }

        return result;
    }
});

// Update public API
Object.assign(EmailValidator, {
    validateWithDNS: validationMethods.validateWithDNS.bind(validationMethods)
});

    // Public API
    return {
        validate: validationMethods.validate.bind(validationMethods),
        quickCheck: validationMethods.quickFormatCheck.bind(validationMethods),
        normalize: validationMethods.normalizeEmail.bind(validationMethods),
        CONSTANTS: EMAIL_CONSTANTS
    };
})();

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EmailValidator;
} else if (typeof define === 'function' && define.amd) {
    define(['SacredCore'], () => EmailValidator);
} else {
    window.EmailValidator = EmailValidator;
}
