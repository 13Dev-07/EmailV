/**
 * DNS Cache Manager following sacred geometry principles
 * Implements caching with golden ratio-based expiration
 */
class DNSCacheManager {
    constructor() {
        this.cache = new Map();
        this.PHI = 1.618033988749895; // Golden ratio
        this.BASE_TTL = 3600000; // 1 hour in milliseconds
    }

    /**
     * Calculate cache TTL using golden ratio
     * @param {number} baseTTL - Base time to live in milliseconds
     * @param {number} priority - Priority level (1-5)
     * @returns {number} Calculated TTL
     */
    calculateTTL(baseTTL, priority = 3) {
        return Math.floor(baseTTL * Math.pow(this.PHI, priority - 3));
    }

    /**
     * Get cached DNS result
     * @param {string} domain 
     * @returns {Object|null} Cached result or null
     */
    get(domain) {
        const entry = this.cache.get(domain);
        if (!entry) return null;

        const now = Date.now();
        if (now > entry.expiresAt) {
            this.cache.delete(domain);
            return null;
        }

        return entry.data;
    }

    /**
     * Store DNS result in cache
     * @param {string} domain 
     * @param {Object} data 
     * @param {number} ttl 
     */
    set(domain, data, ttl) {
        const now = Date.now();
        const priority = this.calculatePriority(data);
        const adjustedTTL = this.calculateTTL(ttl || this.BASE_TTL, priority);

        this.cache.set(domain, {
            data,
            expiresAt: now + adjustedTTL,
            priority
        });

        // Maintain cache size using golden ratio sections
        this.maintain();
    }

    /**
     * Calculate priority based on DNS record characteristics
     * @param {Object} data 
     * @returns {number} Priority level (1-5)
     */
    calculatePriority(data) {
        if (!data) return 3;
        
        let priority = 3; // Default priority
        
        // Adjust priority based on record characteristics
        if (data.hasMX) priority++;
        if (data.mxRecords?.some(r => r.isPopular)) priority++;
        if (!data.hasDNS) priority--;
        
        return Math.max(1, Math.min(5, priority));
    }

    /**
     * Maintain cache size using golden ratio sections
     */
    maintain() {
        const maxSize = 1000;
        if (this.cache.size <= maxSize) return;

        // Calculate sections using golden ratio
        const phi = this.PHI;
        const section1 = Math.floor(maxSize / (phi * phi));
        const section2 = Math.floor(maxSize / phi);
        const section3 = maxSize - section1 - section2;

        // Sort entries by priority and expiration
        const entries = Array.from(this.cache.entries())
            .sort((a, b) => {
                const priorityDiff = b[1].priority - a[1].priority;
                if (priorityDiff !== 0) return priorityDiff;
                return b[1].expiresAt - a[1].expiresAt;
            });

        // Keep entries according to sectional distribution
        this.cache = new Map(entries.slice(0, section1 + section2 + section3));
    }

    /**
     * Clear expired entries
     */
    clearExpired() {
        const now = Date.now();
        for (const [domain, entry] of this.cache.entries()) {
            if (now > entry.expiresAt) {
                this.cache.delete(domain);
            }
        }
    }
}

// Export singleton instance
export const dnsCache = new DNSCacheManager();