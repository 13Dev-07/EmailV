/**
 * /core/module-registry.js
 * Sacred Module Registry System
 * Version: 1.0.0
 */

const ModuleRegistry = (function() {
    'use strict';

    // Private storage
    const moduleStore = new Map();
    const instanceStore = new Map();
    const dependencyGraph = new Map();
    const lifecycleHooks = new Map();

    /**
     * Module Status Enum
     */
    const MODULE_STATUS = {
        REGISTERED: 'registered',
        INITIALIZING: 'initializing',
        ACTIVE: 'active',
        ERROR: 'error',
        DISABLED: 'disabled',
        DESTROYED: 'destroyed'
    };

    /**
     * Sacred Module Class
     */
    class SacredModule {
        constructor(id, config) {
            this.id = id;
            this.name = config.name || id;
            this.version = config.version || '1.0.0';
            this.dependencies = new Set(config.dependencies || []);
            this.exports = config.exports || {};
            this.status = MODULE_STATUS.REGISTERED;
            this.priority = this.calculatePriority(config.priority);
            this.instance = null;
            this.metadata = {
                registeredAt: Date.now(),
                lastInitialized: null,
                initCount: 0,
                errorCount: 0,
                author: config.author || 'unknown',
                description: config.description || ''
            };
        }

        calculatePriority(priority) {
            if (typeof priority === 'number') return priority;
            
            // Default priorities based on golden ratio
            const PRIORITIES = {
                CRITICAL: SacredCore.constants.MATH.PHI.VALUE * 100,  // ~161.8
                HIGH: SacredCore.constants.MATH.PHI.VALUE * 50,       // ~80.9
                NORMAL: SacredCore.constants.MATH.PHI.VALUE * 10,     // ~16.18
                LOW: SacredCore.constants.MATH.PHI.VALUE              // ~1.618
            };

            return PRIORITIES[priority] || PRIORITIES.NORMAL;
        }

        async initialize(context) {
            try {
                this.status = MODULE_STATUS.INITIALIZING;
                
                // Execute pre-init hooks
                await executeLifecycleHooks(this.id, 'preInit', context);

                // Initialize module
                if (typeof this.exports.initialize === 'function') {
                    this.instance = await this.exports.initialize(context);
                } else {
                    this.instance = this.exports;
                }

                this.status = MODULE_STATUS.ACTIVE;
                this.metadata.lastInitialized = Date.now();
                this.metadata.initCount++;

                // Execute post-init hooks
                await executeLifecycleHooks(this.id, 'postInit', context);

                return true;
            } catch (error) {
                this.status = MODULE_STATUS.ERROR;
                this.metadata.errorCount++;
                throw error;
            }
        }

        async destroy() {
            try {
                // Execute pre-destroy hooks
                await executeLifecycleHooks(this.id, 'preDestroy');

                // Cleanup module
                if (typeof this.exports.destroy === 'function') {
                    await this.exports.destroy();
                }

                this.instance = null;
                this.status = MODULE_STATUS.DESTROYED;

                // Execute post-destroy hooks
                await executeLifecycleHooks(this.id, 'postDestroy');

                return true;
            } catch (error) {
                this.status = MODULE_STATUS.ERROR;
                throw error;
            }
        }
    }

    /**
     * Dependency Resolution
     */
    function buildDependencyGraph() {
        dependencyGraph.clear();

        // Build graph
        for (const [id, module] of moduleStore) {
            dependencyGraph.set(id, new Set(module.dependencies));
        }

        // Validate graph (check for circular dependencies)
        const visited = new Set();
        const recursionStack = new Set();

        function detectCycle(moduleId) {
            if (recursionStack.has(moduleId)) {
                throw new Error(`Circular dependency detected involving module: ${moduleId}`);
            }

            if (visited.has(moduleId)) return;

            visited.add(moduleId);
            recursionStack.add(moduleId);

            const dependencies = dependencyGraph.get(moduleId) || new Set();
            for (const depId of dependencies) {
                detectCycle(depId);
            }

            recursionStack.delete(moduleId);
        }

        for (const moduleId of moduleStore.keys()) {
            detectCycle(moduleId);
        }
    }

    /**
     * Lifecycle Hook Management
     */
    function registerLifecycleHook(moduleId, phase, hook) {
        if (!lifecycleHooks.has(moduleId)) {
            lifecycleHooks.set(moduleId, new Map());
        }

        const moduleHooks = lifecycleHooks.get(moduleId);
        if (!moduleHooks.has(phase)) {
            moduleHooks.set(phase, []);
        }

        moduleHooks.get(phase).push(hook);
    }

    async function executeLifecycleHooks(moduleId, phase, context) {
        const moduleHooks = lifecycleHooks.get(moduleId);
        if (!moduleHooks) return;

        const hooks = moduleHooks.get(phase) || [];
        for (const hook of hooks) {
            await hook(context);
        }
    }

    /**
     * Module Registry Methods
     */
    const registryMethods = {
        /**
         * Register a new module
         * @param {string} id - Module ID
         * @param {Object} config - Module configuration
         * @returns {SacredModule} Registered module
         */
        register(id, config) {
            if (moduleStore.has(id)) {
                throw new Error(`Module "${id}" is already registered`);
            }

            const module = new SacredModule(id, config);
            moduleStore.set(id, module);

            // Rebuild dependency graph
            buildDependencyGraph();

            // Emit registration event
            if (SacredCore.events) {
                SacredCore.events.emit('module:registered', {
                    id,
                    module: module.metadata
                });
            }

            return module;
        },

        /**
         * Initialize modules in dependency order
         * @param {Object} context - Initialization context
         * @returns {Promise<boolean>} Initialization success
         */
        async initialize(context = {}) {
            try {
                // Sort modules by dependencies and priority
                const sortedModules = this.getInitializationOrder();

                // Initialize modules in order
                for (const moduleId of sortedModules) {
                    const module = moduleStore.get(moduleId);
                    await module.initialize(context);
                    instanceStore.set(moduleId, module.instance);
                }

                return true;
            } catch (error) {
                if (SacredCore.errors) {
                    SacredCore.errors.handle(error);
                }
                return false;
            }
        },

        /**
         * Get module initialization order
         * @returns {Array<string>} Ordered module IDs
         */
        getInitializationOrder() {
            const visited = new Set();
            const order = [];

            function visit(moduleId) {
                if (visited.has(moduleId)) return;

                visited.add(moduleId);

                const dependencies = dependencyGraph.get(moduleId) || new Set();
                for (const depId of dependencies) {
                    visit(depId);
                }

                order.push(moduleId);
            }

            // Sort modules by priority first
            const modulesByPriority = Array.from(moduleStore.entries())
                .sort(([, a], [, b]) => b.priority - a.priority);

            // Visit modules in priority order
            for (const [moduleId] of modulesByPriority) {
                visit(moduleId);
            }

            return order;
        },

        /**
         * Get module instance
         * @param {string} id - Module ID
         * @returns {*} Module instance
         */
        getInstance(id) {
            return instanceStore.get(id);
        },

        /**
         * Register lifecycle hook
         * @param {string} moduleId - Module ID
         * @param {string} phase - Lifecycle phase
         * @param {Function} hook - Hook function
         */
        registerHook(moduleId, phase, hook) {
            registerLifecycleHook(moduleId, phase, hook);
        },

        /**
         * Get module statistics
         * @returns {Object} Module statistics
         */
        getStats() {
            return {
                totalModules: moduleStore.size,
                activeModules: Array.from(moduleStore.values())
                    .filter(m => m.status === MODULE_STATUS.ACTIVE).length,
                errorModules: Array.from(moduleStore.values())
                    .filter(m => m.status === MODULE_STATUS.ERROR).length,
                initializationCount: Array.from(moduleStore.values())
                    .reduce((sum, m) => sum + m.metadata.initCount, 0)
            };
        }
    };

    // Public API
    const api = {
        register: registryMethods.register.bind(registryMethods),
        initialize: registryMethods.initialize.bind(registryMethods),
        getInstance: registryMethods.getInstance.bind(registryMethods),
        registerHook: registryMethods.registerHook.bind(registryMethods),
        getStats: registryMethods.getStats.bind(registryMethods),
        STATUS: MODULE_STATUS
    };

    // Attach to SacredCore
    if (typeof SacredCore !== 'undefined') {
        SacredCore.modules = api;
    }

    return api;
})();

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ModuleRegistry;
} else if (typeof define === 'function' && define.amd) {
    define(['SacredCore'], () => ModuleRegistry);
}
