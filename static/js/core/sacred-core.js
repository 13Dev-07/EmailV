/**
 * /core/sacred-core.js
 * Sacred Core System - Main Entry Point
 * Version: 1.0.0
 */

const SacredCore = (function() {
    'use strict';

    // Private core state
    let isInitialized = false;
    let initializationPromise = null;

    /**
     * Core initialization and bootstrapping
     */
    async function initialize(options = {}) {
        if (isInitialized) {
            return true;
        }

        if (initializationPromise) {
            return initializationPromise;
        }

        initializationPromise = (async () => {
            try {
                // Initialize core dependencies in order
                await Constants.initialize();
                await ConfigManager.initialize(options.config);
                await ModuleRegistry.initialize();

                // Initialize systems
                await Promise.all([
                    EventSystem.initialize(),
                    StateSystem.initialize(),
                    ErrorSystem.initialize(),
                    LoggingSystem.initialize(),
                    SecuritySystem.initialize(),
                    PerformanceSystem.initialize()
                ]);

                isInitialized = true;
                return true;

            } catch (error) {
                console.error('Sacred Core initialization failed:', error);
                throw error;
            }
        })();

        return initializationPromise;
    }

    /**
     * Core API
     */
    return {
        /**
         * Initialize the Sacred Core system
         * @param {Object} options - Initialization options
         * @returns {Promise<boolean>} Initialization success
         */
        async initialize(options = {}) {
            return initialize(options);
        },

        /**
         * Check if system is initialized
         * @returns {boolean} Initialization status
         */
        isInitialized() {
            return isInitialized;
        },

        /**
         * Get system version
         * @returns {string} System version
         */
        getVersion() {
            return '1.0.0';
        },

        /**
         * Export core modules
         * These will be populated by their respective modules
         */
        constants: null,    // Will be set by constants.js
        config: null,       // Will be set by config-manager.js
        modules: null,      // Will be set by module-registry.js
        events: null,       // Will be set by event-system.js
        state: null,        // Will be set by state-system.js
        errors: null,       // Will be set by error-system.js
        logging: null,      // Will be set by logging-system.js
        security: null,     // Will be set by security-system.js
        performance: null   // Will be set by performance-system.js
    };
})();

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SacredCore;
} else if (typeof define === 'function' && define.amd) {
    define([], () => SacredCore);
} else {
    window.SacredCore = SacredCore;
}
