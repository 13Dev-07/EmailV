/**
 * /validation/batch-processor.js
 * Sacred Batch Processing System for Email Validation
 * Version: 1.0.0
 */

const BatchProcessor = (function() {
    'use strict';

    /**
     * Batch Processing Constants
     */
    const BATCH_CONSTANTS = {
        // Batch sizes based on golden ratio
        SIZES: {
            TINY: Math.round(5 * SacredCore.constants.MATH.PHI.INVERSE),    // ~3
            SMALL: Math.round(10 * SacredCore.constants.MATH.PHI.INVERSE),  // ~6
            MEDIUM: Math.round(25 * SacredCore.constants.MATH.PHI.INVERSE), // ~15
            LARGE: Math.round(50 * SacredCore.constants.MATH.PHI.INVERSE),  // ~31
            HUGE: Math.round(100 * SacredCore.constants.MATH.PHI.INVERSE)   // ~62
        },

        // Processing delays (ms)
        DELAYS: {
            BATCH: 100 * SacredCore.constants.MATH.PHI.INVERSE,     // ~62ms
            THROTTLE: 200 * SacredCore.constants.MATH.PHI.INVERSE,  // ~124ms
            TIMEOUT: 1000 * SacredCore.constants.MATH.PHI.VALUE     // ~1618ms
        },

        // Priority levels
        PRIORITY: {
            CRITICAL: SacredCore.constants.MATH.PHI.VALUE * 100,    // ~161.8
            HIGH: SacredCore.constants.MATH.PHI.VALUE * 50,         // ~80.9
            NORMAL: SacredCore.constants.MATH.PHI.VALUE * 10,       // ~16.18
            LOW: SacredCore.constants.MATH.PHI.VALUE                // ~1.618
        }
    };

    /**
     * Batch Processing Queue
     */
    class BatchQueue {
        constructor() {
            this.queues = new Map();
            this.processing = false;
            this.stats = {
                processed: 0,
                successful: 0,
                failed: 0,
                startTime: null,
                endTime: null
            };
        }

        /**
         * Add items to queue
         * @param {Array} items - Items to process
         * @param {string} priority - Priority level
         * @returns {Promise} Queue processing promise
         */
        add(items, priority = 'NORMAL') {
            const priorityLevel = BATCH_CONSTANTS.PRIORITY[priority] || 
                                BATCH_CONSTANTS.PRIORITY.NORMAL;

            if (!this.queues.has(priorityLevel)) {
                this.queues.set(priorityLevel, []);
            }

            const queue = this.queues.get(priorityLevel);
            queue.push(...items);

            // Start processing if not already running
            if (!this.processing) {
                this.startProcessing();
            }

            return this.createQueuePromise(items);
        }

        /**
         * Create promise for queued items
         * @param {Array} items - Queued items
         * @returns {Promise} Queue promise
         */
        createQueuePromise(items) {
            return new Promise((resolve, reject) => {
                const results = new Map();
                let completed = 0;

                items.forEach(item => {
                    item.callback = (result) => {
                        results.set(item.id, result);
                        completed++;

                        if (completed === items.length) {
                            resolve(Array.from(results.values()));
                        }
                    };
                    item.errorCallback = reject;
                });
            });
        }

        /**
         * Start queue processing
         */
        async startProcessing() {
            if (this.processing) return;

            this.processing = true;
            this.stats.startTime = performance.now();

            try {
                while (this.hasItems()) {
                    const batch = this.getNextBatch();
                    if (batch.length === 0) break;

                    await this.processBatch(batch);
                    await this.delay(BATCH_CONSTANTS.DELAYS.BATCH);
                }
            } finally {
                this.processing = false;
                this.stats.endTime = performance.now();
            }
        }

        /**
         * Check if queue has items
         * @returns {boolean} Has items
         */
        hasItems() {
            return Array.from(this.queues.values())
                .some(queue => queue.length > 0);
        }

        /**
         * Get next batch of items
         * @returns {Array} Batch items
         */
        getNextBatch() {
            const batch = [];
            const priorities = Array.from(this.queues.keys())
                .sort((a, b) => b - a);

            // Calculate optimal batch size based on queue size
            const totalItems = Array.from(this.queues.values())
                .reduce((sum, queue) => sum + queue.length, 0);
            const batchSize = this.calculateOptimalBatchSize(totalItems);

            // Fill batch with highest priority items first
            for (const priority of priorities) {
                const queue = this.queues.get(priority);
                while (queue.length > 0 && batch.length < batchSize) {
                    batch.push(queue.shift());
                }

                if (batch.length >= batchSize) break;
            }

            return batch;
        }

        /**
         * Calculate optimal batch size
         * @param {number} totalItems - Total items in queue
         * @returns {number} Optimal batch size
         */
        calculateOptimalBatchSize(totalItems) {
            const { SIZES } = BATCH_CONSTANTS;

            if (totalItems <= SIZES.TINY) return SIZES.TINY;
            if (totalItems <= SIZES.SMALL) return SIZES.SMALL;
            if (totalItems <= SIZES.MEDIUM) return SIZES.MEDIUM;
            if (totalItems <= SIZES.LARGE) return SIZES.LARGE;
            return SIZES.HUGE;
        }

        /**
         * Process batch of items
         * @param {Array} batch - Batch to process
         */
        async processBatch(batch) {
            const batchPromises = batch.map(async item => {
                try {
                    const result = await this.processItem(item);
                    this.stats.processed++;
                    this.stats.successful++;
                    item.callback(result);
                    return result;
                } catch (error) {
                    this.stats.processed++;
                    this.stats.failed++;
                    item.errorCallback(error);
                    throw error;
                }
            });

            return Promise.allSettled(batchPromises);
        }

        /**
         * Process single item
         * @param {Object} item - Item to process
         * @returns {Promise} Processing promise
         */
        async processItem(item) {
            // Add timeout protection
            return Promise.race([
                item.processor(item.data),
                new Promise((_, reject) => 
                    setTimeout(() => reject(new Error('Processing timeout')), 
                        BATCH_CONSTANTS.DELAYS.TIMEOUT)
                )
            ]);
        }

        /**
         * Delay execution
         * @param {number} ms - Milliseconds to delay
         * @returns {Promise} Delay promise
         */
        delay(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

        /**
         * Get processing statistics
         * @returns {Object} Processing stats
         */
        getStats() {
            return {
                ...this.stats,
                duration: this.stats.endTime - this.stats.startTime,
                successRate: (this.stats.successful / this.stats.processed) * 100,
                throughput: this.stats.processed / 
                    ((this.stats.endTime - this.stats.startTime) / 1000)
            };
        }
    }

    /**
     * Batch Processor Methods
     */
    const batchMethods = {
        /**
         * Process batch of emails
         * @param {Array} emails - Emails to validate
         * @param {Object} options - Processing options
         * @returns {Promise<Array>} Validation results
         */
        async processBatch(emails, options = {}) {
            const queue = new BatchQueue();
            const items = emails.map((email, index) => ({
                id: `${index}-${email}`,
                data: email,
                processor: async (email) => {
                    return options.dns ? 
                        EmailValidator.validateWithDNS(email, options) :
                        EmailValidator.validate(email, options);
                }
            }));

            return queue.add(items, options.priority);
        },

        /**
         * Process emails in parallel with domain grouping
         * @param {Array} emails - Emails to validate
         * @param {Object} options - Processing options
         * @returns {Promise<Array>} Validation results
         */
        async processParallel(emails, options = {}) {
            // Group emails by domain for efficient DNS lookups
            const domainGroups = new Map();
            emails.forEach(email => {
                const domain = email.split('@')[1];
                if (!domainGroups.has(domain)) {
                    domainGroups.set(domain, []);
                }
                domainGroups.get(domain).push(email);
            });

            // Process each domain group
            const results = await Promise.all(
                Array.from(domainGroups.entries()).map(async ([domain, groupEmails]) => {
                    const queue = new BatchQueue();
                    const items = groupEmails.map((email, index) => ({
                        id: `${domain}-${index}-${email}`,
                        data: email,
                        processor: async (email) => {
                            return options.dns ? 
                                EmailValidator.validateWithDNS(email, options) :
                                EmailValidator.validate(email, options);
                        }
                    }));

                    return queue.add(items, options.priority);
                })
            );

            // Flatten and sort results
            return results.flat().sort((a, b) => 
                emails.indexOf(a.email) - emails.indexOf(b.email));
        }
    };

    // Public API
    return {
        processBatch: batchMethods.processBatch,
        processParallel: batchMethods.processParallel,
        CONSTANTS: BATCH_CONSTANTS
    };
})();

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BatchProcessor;
} else if (typeof define === 'function' && define.amd) {
    define(['SacredCore', 'EmailValidator'], () => BatchProcessor);
} else {
    window.BatchProcessor = BatchProcessor;
}
