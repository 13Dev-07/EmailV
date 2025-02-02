/**
 * /validation/results-handler.js
 * Sacred Results Management System
 * Version: 1.0.0
 */

const ResultsHandler = (function() {
    'use strict';

    /**
     * Results Constants
     */
    const RESULTS_CONSTANTS = {
        // Result categories based on golden ratio thresholds
        CATEGORIES: {
            PERFECT: 100,
            EXCELLENT: Math.round(100 * SacredCore.constants.MATH.PHI.INVERSE),  // ~61.8
            GOOD: Math.round(100 * Math.pow(SacredCore.constants.MATH.PHI.INVERSE, 2)), // ~38.2
            FAIR: Math.round(100 * Math.pow(SacredCore.constants.MATH.PHI.INVERSE, 3)), // ~23.6
            POOR: Math.round(100 * Math.pow(SacredCore.constants.MATH.PHI.INVERSE, 4))  // ~14.6
        },

        // Export formats
        FORMATS: {
            JSON: 'json',
            CSV: 'csv',
            HTML: 'html',
            MARKDOWN: 'markdown'
        },

        // Analysis thresholds
        THRESHOLDS: {
            WARNING_RATIO: SacredCore.constants.MATH.PHI.INVERSE,    // ~0.618
            ERROR_RATIO: 1 - SacredCore.constants.MATH.PHI.INVERSE  // ~0.382
        }
    };

    /**
     * Results Collection Class
     */
    class ResultsCollection {
        constructor(results = []) {
            this.results = results;
            this.timestamp = Date.now();
            this.metadata = {
                total: results.length,
                valid: 0,
                invalid: 0,
                warnings: 0,
                errors: 0,
                score: 0
            };
            this.analyze();
        }

        /**
         * Analyze results and update metadata
         */
        analyze() {
            this.metadata.valid = this.results.filter(r => r.isValid).length;
            this.metadata.invalid = this.results.filter(r => !r.isValid).length;
            this.metadata.warnings = this.results.reduce((sum, r) => 
                sum + (r.warnings?.length || 0), 0);
            this.metadata.errors = this.results.reduce((sum, r) => 
                sum + (r.errors?.length || 0), 0);
            
            // Calculate overall score
            this.metadata.score = this.calculateOverallScore();

            // Add category based on score
            this.metadata.category = this.categorizeScore(this.metadata.score);

            // Add quality metrics
            this.metadata.quality = this.calculateQualityMetrics();
        }

        /**
         * Calculate overall score
         * @returns {number} Overall score
         */
        calculateOverallScore() {
            if (this.results.length === 0) return 0;

            const validWeight = SacredCore.constants.MATH.PHI.VALUE;
            const warningWeight = SacredCore.constants.MATH.PHI.INVERSE;

            const validScore = (this.metadata.valid / this.results.length) * 100 * validWeight;
            const warningScore = (1 - (this.metadata.warnings / (this.results.length * 3))) * 
                100 * warningWeight;

            return Math.round((validScore + warningScore) / (validWeight + warningWeight));
        }

        /**
         * Categorize score
         * @param {number} score - Score to categorize
         * @returns {string} Score category
         */
        categorizeScore(score) {
            const { CATEGORIES } = RESULTS_CONSTANTS;
            
            if (score >= CATEGORIES.PERFECT) return 'PERFECT';
            if (score >= CATEGORIES.EXCELLENT) return 'EXCELLENT';
            if (score >= CATEGORIES.GOOD) return 'GOOD';
            if (score >= CATEGORIES.FAIR) return 'FAIR';
            return 'POOR';
        }

        /**
         * Calculate quality metrics
         * @returns {Object} Quality metrics
         */
        calculateQualityMetrics() {
            return {
                validRatio: this.metadata.valid / this.metadata.total,
                errorRatio: this.metadata.errors / this.metadata.total,
                warningRatio: this.metadata.warnings / this.metadata.total,
                confidence: this.calculateConfidenceScore(),
                reliability: this.calculateReliabilityScore()
            };
        }

        /**
         * Calculate confidence score
         * @returns {number} Confidence score
         */
        calculateConfidenceScore() {
            const validRatio = this.metadata.valid / this.metadata.total;
            const warningImpact = (this.metadata.warnings / (this.metadata.total * 3)) * 
                SacredCore.constants.MATH.PHI.INVERSE;
            
            return Math.round((validRatio - warningImpact) * 100);
        }

        /**
         * Calculate reliability score
         * @returns {number} Reliability score
         */
        calculateReliabilityScore() {
            const errorImpact = (this.metadata.errors / this.metadata.total) * 
                SacredCore.constants.MATH.PHI.VALUE;
            const warningImpact = (this.metadata.warnings / (this.metadata.total * 3)) * 
                SacredCore.constants.MATH.PHI.INVERSE;
            
            return Math.round((1 - (errorImpact + warningImpact)) * 100);
        }

        /**
         * Get results summary
         * @returns {Object} Results summary
         */
        getSummary() {
            return {
                metadata: this.metadata,
                timestamp: this.timestamp,
                distribution: this.getDistribution(),
                patterns: this.analyzePatterns(),
                recommendations: this.generateRecommendations()
            };
        }

        /**
         * Get result distribution
         * @returns {Object} Result distribution
         */
        getDistribution() {
            const distribution = {
                categories: {},
                errorTypes: {},
                warningTypes: {},
                domains: {}
            };

            this.results.forEach(result => {
                // Category distribution
                const category = this.categorizeScore(result.score || 0);
                distribution.categories[category] = 
                    (distribution.categories[category] || 0) + 1;

                // Error types distribution
                result.errors?.forEach(error => {
                    distribution.errorTypes[error.code] = 
                        (distribution.errorTypes[error.code] || 0) + 1;
                });

                // Warning types distribution
                result.warnings?.forEach(warning => {
                    distribution.warningTypes[warning.code] = 
                        (distribution.warningTypes[warning.code] || 0) + 1;
                });

                // Domain distribution
                const domain = result.email.split('@')[1];
                distribution.domains[domain] = 
                    (distribution.domains[domain] || 0) + 1;
            });

            return distribution;
        }

        /**
         * Analyze result patterns
         * @returns {Object} Pattern analysis
         */
        analyzePatterns() {
            return {
                commonErrors: this.findCommonPatterns('errors'),
                commonWarnings: this.findCommonPatterns('warnings'),
                domainTrends: this.analyzeDomainTrends(),
                qualityTrends: this.analyzeQualityTrends()
            };
        }

        /**
         * Find common patterns
         * @param {string} type - Pattern type
         * @returns {Array} Common patterns
         */
        findCommonPatterns(type) {
            const patterns = {};
            
            this.results.forEach(result => {
                result[type]?.forEach(item => {
                    patterns[item.code] = patterns[item.code] || {
                        code: item.code,
                        count: 0,
                        messages: new Set()
                    };
                    patterns[item.code].count++;
                    patterns[item.code].messages.add(item.message);
                });
            });

            return Object.values(patterns)
                .sort((a, b) => b.count - a.count)
                .map(pattern => ({
                    ...pattern,
                    messages: Array.from(pattern.messages),
                    frequency: pattern.count / this.results.length
                }));
        }

        /**
         * Analyze domain trends
         * @returns {Object} Domain trends
         */
        analyzeDomainTrends() {
            const domains = {};
            
            this.results.forEach(result => {
                const domain = result.email.split('@')[1];
                domains[domain] = domains[domain] || {
                    domain,
                    total: 0,
                    valid: 0,
                    invalid: 0,
                    score: 0
                };

                domains[domain].total++;
                if (result.isValid) domains[domain].valid++;
                else domains[domain].invalid++;
                domains[domain].score += result.score || 0;
            });

            return Object.values(domains)
                .map(domain => ({
                    ...domain,
                    score: Math.round(domain.score / domain.total),
                    validRatio: domain.valid / domain.total
                }))
                .sort((a, b) => b.total - a.total);
        }

        /**
         * Generate recommendations
         * @returns {Array} Recommendations
         */
        generateRecommendations() {
            const recommendations = [];
            const { quality } = this.metadata;

            // Add recommendations based on analysis
            if (quality.errorRatio > RESULTS_CONSTANTS.THRESHOLDS.ERROR_RATIO) {
                recommendations.push({
                    priority: 'HIGH',
                    type: 'ERROR_RATE',
                    message: 'High error rate detected',
                    suggestion: 'Review validation rules and input quality'
                });
            }

            if (quality.warningRatio > RESULTS_CONSTANTS.THRESHOLDS.WARNING_RATIO) {
                recommendations.push({
                    priority: 'MEDIUM',
                    type: 'WARNING_RATE',
                    message: 'High warning rate detected',
                    suggestion: 'Consider implementing additional validation checks'
                });
            }

            // Add domain-specific recommendations
            const domainTrends = this.analyzeDomainTrends();
            const problematicDomains = domainTrends
                .filter(d => d.validRatio < RESULTS_CONSTANTS.THRESHOLDS.WARNING_RATIO);

            if (problematicDomains.length > 0) {
                recommendations.push({
                    priority: 'MEDIUM',
                    type: 'DOMAIN_QUALITY',
                    message: 'Problematic domains detected',
                    suggestion: 'Review email quality for specific domains',
                    domains: problematicDomains.map(d => d.domain)
                });
            }

            return recommendations.sort((a, b) => 
                b.priority.localeCompare(a.priority));
        }

        /**
         * Export results
         * @param {string} format - Export format
         * @returns {string} Exported results
         */
        export(format = RESULTS_CONSTANTS.FORMATS.JSON) {
            switch (format) {
                case RESULTS_CONSTANTS.FORMATS.JSON:
                    return this.exportJSON();
                case RESULTS_CONSTANTS.FORMATS.CSV:
                    return this.exportCSV();
                case RESULTS_CONSTANTS.FORMATS.HTML:
                    return this.exportHTML();
                case RESULTS_CONSTANTS.FORMATS.MARKDOWN:
                    return this.exportMarkdown();
                default:
                    throw new Error(`Unsupported export format: ${format}`);
            }
        }

        /**
         * Export results as JSON
         * @returns {string} JSON results
         */
        exportJSON() {
            return JSON.stringify({
                results: this.results,
                summary: this.getSummary()
            }, null, 2);
        }

        // Additional export methods would be implemented here...
    }

    /**
     * Results Handler Methods
     */
    const handlerMethods = {
        /**
         * Create results collection
         * @param {Array} results - Validation results
         * @returns {ResultsCollection} Results collection
         */
        createCollection(results) {
            return new ResultsCollection(results);
        },

        /**
         * Merge multiple result collections
         * @param {Array<ResultsCollection>} collections - Collections to merge
         * @returns {ResultsCollection} Merged collection
         */
        mergeCollections(collections) {
            const mergedResults = collections.reduce((all, collection) => 
                all.concat(collection.results), []);
            return new ResultsCollection(mergedResults);
        }
    };

    // Public API
    return {
        createCollection: handlerMethods.createCollection,
        mergeCollections: handlerMethods.mergeCollections,
        CONSTANTS: RESULTS_CONSTANTS
    };
})();

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ResultsHandler;
} else if (typeof define === 'function' && define.amd) {
    define(['SacredCore'], () => ResultsHandler);
} else {
    window.ResultsHandler = ResultsHandler;
}
