/**
 * /core/config-manager.js
 * Sacred Configuration Management System
 * Version: 1.0.0
 */

const ConfigManager = (function() {
    'use strict';

    // Private storage
    const configStore = new Map();
    const configHistory = new Map();
    const configValidators = new Map();
    const configDefaults = new Map();

    /**
     * Configuration Schema
     */
    const CONFIG_SCHEMA = {
        core: {
            environment: {
                type: 'string',
                enum: Object.values(SacredCore.constants.SYSTEM.ENVIRONMENT),
                default: 'development'
            },
            mode: {
                type: 'string',
                enum: Object.values(SacredCore.constants.SYSTEM.MODES),
                default: 'normal'
            },
            debug: {
                type: 'boolean',
                default: false
            },
            version: {
                type: 'string',
                pattern: /^\d+\.\d+\.\d+$/,
                default: SacredCore.constants.SYSTEM.VERSION.FULL
            }
        },
        validation: {
            mode: {
                type: 'string',
                enum: Object.values(SacredCore.constants.VALIDATION.MODES),
                default: 'sync'
            },
            batchSize: {
                type: 'number',
                min: SacredCore.constants.VALIDATION.BATCH.SMALL,
                max: SacredCore.constants.VALIDATION.BATCH.MAX,
                default: SacredCore.constants.VALIDATION.BATCH.MEDIUM
            },
            timeout: {
                type: 'number',
                min: 0,
                default: SacredCore.constants.VALIDATION.TIMING.TIMEOUT
            }
        },
        performance: {
            monitoring: {
                type: 'boolean',
                default: true
            },
            sampleRate: {
                type: 'number',
                min: 0,
                max: 1,
                default: SacredCore.constants.MATH.PHI.INVERSE
            },
            throttle: {
                type: 'number',
                min: 0,
                default: SacredCore.constants.VALIDATION.TIMING.THROTTLE
            }
        },
        ui: {
            animations: {
                type: 'boolean',
                default: true
            },
            theme: {
                type: 'string',
                enum: ['light', 'dark', 'auto'],
                default: 'auto'
            },
            spacing: {
                type: 'number',
                min: 0,
                default: SacredCore.constants.UI.SPACING.UNIT
            }
        }
    };

    /**
     * Configuration Validation
     */
    class ConfigValidator {
        static validateType(value, type) {
            switch (type) {
                case 'string':
                    return typeof value === 'string';
                case 'number':
                    return typeof value === 'number' && !isNaN(value);
                case 'boolean':
                    return typeof value === 'boolean';
                case 'object':
                    return typeof value === 'object' && value !== null;
                case 'array':
                    return Array.isArray(value);
                default:
                    return false;
            }
        }

        static validateEnum(value, enumValues) {
            return enumValues.includes(value);
        }

        static validatePattern(value, pattern) {
            return pattern.test(value);
        }

        static validateRange(value, { min, max }) {
            if (min !== undefined && value < min) return false;
            if (max !== undefined && value > max) return false;
            return true;
        }

        static validate(value, schema) {
            // Type validation
            if (!this.validateType(value, schema.type)) {
                throw new Error(`Invalid type: expected ${schema.type}`);
            }

            // Enum validation
            if (schema.enum && !this.validateEnum(value, schema.enum)) {
                throw new Error(`Value must be one of: ${schema.enum.join(', ')}`);
            }

            // Pattern validation
            if (schema.pattern && !this.validatePattern(value, schema.pattern)) {
                throw new Error('Value does not match required pattern');
            }

            // Range validation
            if (schema.type === 'number' && 
                !this.validateRange(value, { min: schema.min, max: schema.max })) {
                throw new Error(`Value must be between ${schema.min} and ${schema.max}`);
            }

            return true;
        }
    }

    /**
     * Configuration Methods
     */
    const configMethods = {
        /**
         * Set configuration value
         * @param {string} path - Configuration path
         * @param {*} value - Configuration value
         * @returns {boolean} Success status
         */
        set(path, value) {
            try {
                // Get schema for path
                const schema = this.getSchema(path);
                if (!schema) {
                    throw new Error(`Invalid configuration path: ${path}`);
                }

                // Validate value
                ConfigValidator.validate(value, schema);

                // Store previous value in history
                this.storeHistory(path);

                // Update configuration
                const keys = path.split('.');
                let current = configStore;
                
                for (let i = 0; i < keys.length - 1; i++) {
                    if (!current.has(keys[i])) {
                        current.set(keys[i], new Map());
                    }
                    current = current.get(keys[i]);
                }
                
                current.set(keys[keys.length - 1], value);

                // Emit change event
                if (SacredCore.events) {
                    SacredCore.events.emit('config:changed', {
                        path,
                        value,
                        timestamp: Date.now()
                    });
                }

                return true;
            } catch (error) {
                if (SacredCore.errors) {
                    SacredCore.errors.handle(error);
                } else {
                    console.error('Configuration error:', error);
                }
                return false;
            }
        },

        /**
         * Get configuration value
         * @param {string} path - Configuration path
         * @returns {*} Configuration value
         */
        get(path) {
            const keys = path.split('.');
            let current = configStore;

            for (const key of keys) {
                if (!current.has(key)) {
                    return this.getDefault(path);
                }
                current = current.get(key);
            }

            return current;
        },

        /**
         * Get default configuration value
         * @param {string} path - Configuration path
         * @returns {*} Default value
         */
        getDefault(path) {
            const schema = this.getSchema(path);
            return schema ? schema.default : undefined;
        },

        /**
         * Get configuration schema
         * @param {string} path - Configuration path
         * @returns {Object} Configuration schema
         */
        getSchema(path) {
            return path.split('.').reduce((obj, key) => 
                obj && obj[key], CONFIG_SCHEMA);
        },

        /**
         * Store configuration history
         * @param {string} path - Configuration path
         */
        storeHistory(path) {
            if (!configHistory.has(path)) {
                configHistory.set(path, []);
            }

            const history = configHistory.get(path);
            history.push({
                value: this.get(path),
                timestamp: Date.now()
            });

            // Limit history size using golden ratio
            const maxHistory = Math.round(10 * SacredCore.constants.MATH.PHI.VALUE);
            if (history.length > maxHistory) {
                history.splice(0, history.length - maxHistory);
            }
        },

        /**
         * Reset configuration to defaults
         * @param {string} [path] - Optional path to reset
         * @returns {boolean} Success status
         */
        reset(path) {
            if (path) {
                return this.set(path, this.getDefault(path));
            }

            try {
                configStore.clear();
                this.initialize();
                return true;
            } catch (error) {
                if (SacredCore.errors) {
                    SacredCore.errors.handle(error);
                }
                return false;
            }
        },
// Adding to config-manager.js

/**
 * Configuration Error Classes
 */
class ConfigurationError extends Error {
    constructor(message, code, details = {}) {
        super(message);
        this.name = 'ConfigurationError';
        this.code = code;
        this.details = details;
        this.timestamp = Date.now();
    }
}

class ValidationError extends ConfigurationError {
    constructor(message, details) {
        super(message, 'VALIDATION_ERROR', details);
        this.name = 'ValidationError';
    }
}

class SchemaError extends ConfigurationError {
    constructor(message, details) {
        super(message, 'SCHEMA_ERROR', details);
        this.name = 'SchemaError';
    }
}

/**
 * Enhanced Error Handling Methods
 */
const errorHandlers = {
    handleValidationError(path, value, schema, details) {
        const error = new ValidationError(
            `Invalid configuration value for '${path}'`,
            {
                path,
                value,
                schema,
                details
            }
        );

        if (SacredCore.errors) {
            SacredCore.errors.handle(error);
        }

        // Emit error event
        if (SacredCore.events) {
            SacredCore.events.emit('config:error', error);
        }

        throw error;
    },

    handleSchemaError(path, details) {
        const error = new SchemaError(
            `Invalid configuration schema for '${path}'`,
            details
        );

        if (SacredCore.errors) {
            SacredCore.errors.handle(error);
        }

        // Emit error event
        if (SacredCore.events) {
            SacredCore.events.emit('config:schema:error', error);
        }

        throw error;
    },

    handleTypeError(path, expectedType, receivedType) {
        return this.handleValidationError(
            path,
            undefined,
            { type: expectedType },
            { receivedType }
        );
    },

    handleRangeError(path, value, min, max) {
        return this.handleValidationError(
            path,
            value,
            { min, max },
            { message: `Value must be between ${min} and ${max}` }
        );
    }
};

// Enhance ConfigValidator class with better error handling
class ConfigValidator {
    static validate(value, schema, path) {
        // Type validation
        if (!this.validateType(value, schema.type)) {
            errorHandlers.handleTypeError(
                path,
                schema.type,
                typeof value
            );
        }

        // Enum validation
        if (schema.enum && !this.validateEnum(value, schema.enum)) {
            errorHandlers.handleValidationError(
                path,
                value,
                schema,
                { message: `Value must be one of: ${schema.enum.join(', ')}` }
            );
        }

        // Pattern validation
        if (schema.pattern && !this.validatePattern(value, schema.pattern)) {
            errorHandlers.handleValidationError(
                path,
                value,
                schema,
                { message: 'Value does not match required pattern' }
            );
        }

        // Range validation
        if (schema.type === 'number' && 
            !this.validateRange(value, { min: schema.min, max: schema.max })) {
            errorHandlers.handleRangeError(
                path,
                value,
                schema.min,
                schema.max
            );
        }

        return true;
    }
}

        /**
         * Initialize configuration system
         * @param {Object} options - Initialization options
         */
        initialize(options = {}) {
            // Load default configuration
            Object.entries(CONFIG_SCHEMA).forEach(([section, config]) => {
                Object.entries(config).forEach(([key, schema]) => {
                    const path = `${section}.${key}`;
                    const value = options[section]?.[key] ?? schema.default;
                    this.set(path, value);
                });
            });

            return true;
        }
    };

    // Initialize configuration on creation
    configMethods.initialize();

    // Public API
    const api = {
        set: configMethods.set.bind(configMethods),
        get: configMethods.get.bind(configMethods),
        reset: configMethods.reset.bind(configMethods),
        initialize: configMethods.initialize.bind(configMethods),
        SCHEMA: CONFIG_SCHEMA
    };

    // Attach to SacredCore
    if (typeof SacredCore !== 'undefined') {
        SacredCore.config = api;
    }

    return api;
})();

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ConfigManager;
} else if (typeof define === 'function' && define.amd) {
    define(['SacredCore'], () => ConfigManager);
}
