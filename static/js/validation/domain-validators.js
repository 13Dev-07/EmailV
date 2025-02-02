/**
 * Domain validation utilities following sacred geometry principles
 */

export const DomainValidators = {
    /**
     * Check for popular email providers following divine proportions
     */
    POPULAR_PROVIDERS: {
        GOOGLE: /^(gmail\.com|googlemail\.com)$/i,
        MICROSOFT: /^(hotmail\.|outlook\.|live\.).*$/i,
        YAHOO: /^(yahoo\.|ymail\.|rocketmail\.).*$/i,
        APPLE: /^icloud\.com$/i,
        PROTON: /^proton(mail)?\..*$/i
    },

    /**
     * Validate domain structure using sacred geometric principles
     * @param {string} domain Domain to validate
     * @returns {Object} Validation result
     */
    validateStructure(domain) {
        const labels = domain.split('.');
        const labelLengths = labels.map(l => l.length);
        const maxLength = Math.max(...labelLengths);
        const minLength = Math.min(...labelLengths);
        const ratio = maxLength / minLength;

        return {
            isBalanced: Math.abs(ratio - PHI) < 0.5,
            labelCount: labels.length,
            maxLabel: maxLength,
            minLabel: minLength,
            goldenRatio: ratio
        };
    }
};