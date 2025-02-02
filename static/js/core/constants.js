/**
 * /core/constants.js
 * Sacred Constants System
 * Version: 1.0.0
 */

const Constants = (function() {
    'use strict';

    /**
     * Mathematical Constants
     */
    const MATH = {
        // Golden Ratio Constants
        PHI: {
            VALUE: 1.618033988749895,              // Golden Ratio (φ)
            INVERSE: 0.618033988749895,            // Golden Ratio Inverse (1/φ)
            SQUARED: 2.618033988749895,            // φ²
            CUBED: 4.236067977499790,             // φ³
            SQRT: 1.272019649514069,              // √φ
            RECIPROCAL: 0.618033988749895         // 1/φ
        },

        // Sacred Angles (in degrees)
        ANGLES: {
            GOLDEN: 137.5077640500378,            // Golden Angle
            SACRED_CUT: 108.0,                    // Sacred Cut
            PENTAGON: 72.0,                       // 360/5
            HEXAGON: 60.0,                        // 360/6
            OCTAGON: 45.0,                        // 360/8
            DODECAGON: 30.0                       // 360/12
        },

        // Sacred Ratios
        RATIOS: {
            GOLDEN: 1.618033988749895,            // Golden Ratio
            SILVER: 2.414213562373095,            // Silver Ratio
            BRONZE: 3.302775637731995,            // Bronze Ratio
            PLATINUM: 1.324717957244746,          // Platinum Ratio
            SACRED_MEAN: 1.732050807568877,       // √3
            DIVINE_PROPORTION: 1.618033988749895  // Same as Golden Ratio
        },

        // Sacred Sequences
        SEQUENCES: {
            FIBONACCI: [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144],
            LUCAS: [2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123],
            TRIANGULAR: [1, 3, 6, 10, 15, 21, 28, 36, 45, 55],
            SQUARE: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
            PENTAGONAL: [1, 5, 12, 22, 35, 51, 70, 92, 117, 145]
        }
// Enhancing the MATH section in constants.js

const MATH = {
    // Previous constants remain...
    
    // Enhanced Sacred Geometry
    GEOMETRY: {
        // Platonic Solids
        PLATONIC: {
            TETRAHEDRON: {
                FACES: 4,
                EDGES: 6,
                VERTICES: 4,
                DIHEDRAL_ANGLE: 70.53,  // degrees
                SOLID_ANGLE: 0.551,     // steradians
                RATIO: Math.sqrt(6) / 4  // Height to edge ratio
            },
            CUBE: {
                FACES: 6,
                EDGES: 12,
                VERTICES: 8,
                DIHEDRAL_ANGLE: 90,
                SOLID_ANGLE: 0.524,
                RATIO: Math.sqrt(3) / 3
            },
            OCTAHEDRON: {
                FACES: 8,
                EDGES: 12,
                VERTICES: 6,
                DIHEDRAL_ANGLE: 109.47,
                SOLID_ANGLE: 0.785,
                RATIO: Math.sqrt(2) / 2
            },
            DODECAHEDRON: {
                FACES: 12,
                EDGES: 30,
                VERTICES: 20,
                DIHEDRAL_ANGLE: 116.57,
                SOLID_ANGLE: 0.471,
                RATIO: MATH.PHI.VALUE
            },
            ICOSAHEDRON: {
                FACES: 20,
                EDGES: 30,
                VERTICES: 12,
                DIHEDRAL_ANGLE: 138.19,
                SOLID_ANGLE: 0.616,
                RATIO: MATH.PHI.VALUE
            }
        },

        // Sacred Polygons
        POLYGONS: {
            TRIANGLE: {
                ANGLES: 60,
                SIDES: 3,
                RATIO: Math.sqrt(3) / 4,
                SACRED_RATIO: Math.sqrt(3) / 2
            },
            SQUARE: {
                ANGLES: 90,
                SIDES: 4,
                RATIO: 1,
                SACRED_RATIO: Math.sqrt(2)
            },
            PENTAGON: {
                ANGLES: 108,
                SIDES: 5,
                RATIO: MATH.PHI.VALUE,
                SACRED_RATIO: (1 + Math.sqrt(5)) / 2
            },
            HEXAGON: {
                ANGLES: 120,
                SIDES: 6,
                RATIO: Math.sqrt(3),
                SACRED_RATIO: 2
            },
            HEPTAGON: {
                ANGLES: 128.57,
                SIDES: 7,
                RATIO: 2 * Math.cos(Math.PI / 7),
                SACRED_RATIO: 2 * Math.cos(Math.PI / 7)
            },
            OCTAGON: {
                ANGLES: 135,
                SIDES: 8,
                RATIO: 2 + Math.sqrt(2),
                SACRED_RATIO: 1 + Math.sqrt(2)
            }
        },

        // Sacred Spirals
        SPIRALS: {
            GOLDEN: {
                GROWTH_FACTOR: MATH.PHI.VALUE,
                ANGLE: MATH.ANGLES.GOLDEN,
                RATIO: MATH.PHI.VALUE
            },
            FIBONACCI: {
                GROWTH_FACTOR: MATH.PHI.VALUE,
                ANGLE: 360 / MATH.PHI.VALUE,
                RATIO: MATH.PHI.VALUE
            },
            LOGARITHMIC: {
                GROWTH_FACTOR: Math.E,
                ANGLE: 360 / Math.E,
                RATIO: Math.E
            }
        },

        // Sacred Proportions
        PROPORTIONS: {
            VESICA_PISCIS: {
                RATIO: Math.sqrt(3),
                ANGLE: 60,
                SACRED_RATIO: Math.sqrt(3) / 2
            },
            FLOWER_OF_LIFE: {
                CIRCLES: 19,
                RATIO: 6,
                SACRED_RATIO: 2 * Math.PI
            },
            SEED_OF_LIFE: {
                CIRCLES: 7,
                RATIO: 2,
                SACRED_RATIO: Math.sqrt(3)
            },
            TREE_OF_LIFE: {
                SPHERES: 10,
                PATHS: 22,
                RATIO: MATH.PHI.VALUE,
                SACRED_RATIO: 1.732
            },
            METATRONS_CUBE: {
                VERTICES: 13,
                LINES: 78,
                RATIO: MATH.PHI.VALUE,
                SACRED_RATIO: Math.sqrt(3)
            }
        }
    }
};
    

    /**
     * System Constants
     */
    const SYSTEM = {
        // Version Information
        VERSION: {
            MAJOR: 1,
            MINOR: 0,
            PATCH: 0,
            FULL: '1.0.0',
            BUILD: '20240101'
        },

        // Environment Types
        ENVIRONMENT: {
            DEVELOPMENT: 'development',
            STAGING: 'staging',
            PRODUCTION: 'production',
            TEST: 'test'
        },

        // System Modes
        MODES: {
            NORMAL: 'normal',
            DEBUG: 'debug',
            STRICT: 'strict',
            SAFE: 'safe'
        },

        // Feature Flags
        FEATURES: {
            ADVANCED_VALIDATION: true,
            PERFORMANCE_MONITORING: true,
            ERROR_TRACKING: true,
            ANALYTICS: true
        }
    };

    /**
     * Validation Constants
     */
    const VALIDATION = {
        // Timing Constants (based on Golden Ratio)
        TIMING: {
            DEBOUNCE: Math.round(100 * MATH.PHI.INVERSE),    // ~62ms
            THROTTLE: Math.round(160 * MATH.PHI.INVERSE),    // ~99ms
            TIMEOUT: Math.round(1000 * MATH.PHI.VALUE),      // ~1618ms
            RETRY_DELAY: Math.round(500 * MATH.PHI.INVERSE)  // ~309ms
        },

        // Batch Sizes (based on Golden Ratio)
        BATCH: {
            SMALL: Math.round(10 * MATH.PHI.INVERSE),        // ~6
            MEDIUM: Math.round(10 * MATH.PHI.VALUE),         // ~16
            LARGE: Math.round(100 * MATH.PHI.INVERSE),       // ~62
            MAX: Math.round(100 * MATH.PHI.VALUE)           // ~162
        },

        // Validation Modes
        MODES: {
            SYNC: 'sync',
            ASYNC: 'async',
            BATCH: 'batch',
            STREAM: 'stream'
        }
    };

    /**
     * UI Constants
     */
    const UI = {
        // Animation Timings (based on Golden Ratio)
        ANIMATION: {
            FAST: Math.round(100 * MATH.PHI.INVERSE),       // ~62ms
            NORMAL: Math.round(200 * MATH.PHI.INVERSE),     // ~124ms
            SLOW: Math.round(300 * MATH.PHI.INVERSE),       // ~185ms
            VERY_SLOW: Math.round(500 * MATH.PHI.INVERSE)   // ~309ms
        },

        // Sacred Spacing Units
        SPACING: {
            UNIT: 8,
            GOLDEN: Math.round(8 * MATH.PHI.VALUE),         // ~13px
            DOUBLE_GOLDEN: Math.round(8 * MATH.PHI.SQUARED) // ~21px
        },

        // Sacred Grid
        GRID: {
            COLUMNS: Math.round(12 * MATH.PHI.INVERSE),     // ~7 columns
            GUTTER: Math.round(16 * MATH.PHI.INVERSE),      // ~10px
            MARGIN: Math.round(24 * MATH.PHI.INVERSE)       // ~15px
        }
    };

    /**
     * Utility Methods
     */
    const utils = {
        /**
         * Get constant by path
         * @param {string} path - Dot notation path to constant
         * @returns {*} Constant value
         */
        get(path) {
            return path.split('.').reduce((obj, key) => 
                obj && obj[key], 
                { MATH, SYSTEM, VALIDATION, UI }
            );
        },

        /**
         * Check if constant exists
         * @param {string} path - Dot notation path to constant
         * @returns {boolean} Constant exists
         */
        has(path) {
            return Boolean(this.get(path));
        },

        /**
         * Get golden ratio multiple of a number
         * @param {number} value - Base value
         * @returns {number} Golden ratio multiple
         */
        golden(value) {
            return value * MATH.PHI.VALUE;
        },

        /**
         * Get inverse golden ratio multiple of a number
         * @param {number} value - Base value
         * @returns {number} Inverse golden ratio multiple
         */
        goldenInverse(value) {
            return value * MATH.PHI.INVERSE;
        }
    };

    /**
     * Initialize constants system
     */
    async function initialize() {
        // Validate critical constants
        if (!MATH.PHI.VALUE || !MATH.PHI.INVERSE) {
            throw new Error('Critical mathematical constants are invalid');
        }

        // Freeze all constant objects to prevent modification
        Object.freeze(MATH);
        Object.freeze(SYSTEM);
        Object.freeze(VALIDATION);
        Object.freeze(UI);

        return true;
    }

    // Public API
    const api = {
        initialize,
        ...utils,
        MATH,
        SYSTEM,
        VALIDATION,
        UI
    };

    // Attach to SacredCore
    if (typeof SacredCore !== 'undefined') {
        SacredCore.constants = api;
    }

    return api;
})();

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Constants;
} else if (typeof define === 'function' && define.amd) {
    define([], () => Constants);
}
