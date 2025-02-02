/**
 * /components/sacred-animations.js
 * Divine animation system based on sacred geometry principles
 * Version: 1.0.0
 */

const SacredAnimations = (function() {
    'use strict';

    /**
     * Animation Constants
     * Aligned with CSS variables from sacred-animations.css
     */
    const ANIMATION_CONSTANTS = {
        // Timing Constants (Based on Fibonacci)
        DURATION: {
            INSTANT: 100,    // --time-instant
            QUICK: 200,      // --time-quick
            SWIFT: 300,      // --time-swift
            NATURAL: 500,    // --time-natural
            BALANCED: 800,   // --time-balanced
            HARMONIC: 1300,  // --time-harmonic
            FLOWING: 2100,   // --time-flowing
            COMPLETE: 3400   // --time-complete
        },

        // Sacred Easing Functions
        EASING: {
            GOLDEN: 'cubic-bezier(0.618, 0, 0.382, 1)',      // --ease-golden
            NATURAL: 'cubic-bezier(0.236, 0, 0.764, 1)',     // --ease-natural
            DIVINE: 'cubic-bezier(0.382, 0, 0.618, 1)',      // --ease-divine
            SPIRAL: 'cubic-bezier(0.618, -0.236, 0.382, 1.236)' // --ease-spiral
        },

        // Animation Types (Matching CSS classes)
        TYPES: {
            FADE: 'sacred-fade',
            SPIRAL: 'sacred-spiral',
            FLOW: 'sacred-flow',
            EXPAND: 'sacred-expand',
            VEIL: 'sacred-transition-veil',
            PORTAL: 'sacred-transition-portal',
            ORBIT: 'sacred-orbit',
            PULSE: 'sacred-pulse-pattern',
            MERKABA: 'sacred-merkaba-motion',
            WAVE: 'sacred-wave-pattern',
            VORTEX: 'sacred-vortex-pattern',
            BREATH: 'sacred-breath-pattern'
        },

        // Animation States
        STATES: {
            ENTERING: 'entering',
            ENTERED: 'entered',
            EXITING: 'exiting',
            EXITED: 'exited'
        }
    };
// Continuing sacred-animations.js...

/**
 * Animation Pattern Implementations
 */
const animationPatterns = {
    /**
     * Sacred Orbit Animation
     */
    orbit(element, options = {}) {
        const radius = options.radius || 
            `calc(var(--phi-space-6) * var(--phi))`;
        const duration = options.duration || 
            `calc(var(--transition-golden-slow) * 2)`;

        element.classList.add('sacred-orbit');
        element.style.setProperty('--orbit-radius', radius);
        element.style.setProperty('--orbit-duration', duration);

        return {
            start() {
                element.querySelectorAll('.sacred-orbit-element').forEach((el, i) => {
                    el.style.animationDelay = 
                        `calc(${duration} / ${-(i + 1)})`;
                });
            },
            stop() {
                element.classList.remove('sacred-orbit');
            }
        };
    },

    /**
     * Sacred Pulse Pattern
     */
    pulse(element, options = {}) {
        const duration = options.duration || 'var(--transition-golden-normal)';
        const color = options.color || 'var(--color-ethereal-blue)';

        element.classList.add('sacred-pulse-pattern');
        element.style.setProperty('--pulse-duration', duration);
        element.style.setProperty('--pulse-color', color);

        return {
            start() {
                element.style.animation = 
                    `sacredPulse ${duration} var(--ease-golden) infinite`;
            },
            stop() {
                element.classList.remove('sacred-pulse-pattern');
                element.style.animation = '';
            }
        };
    },

    /**
     * Sacred Flow Pattern
     */
    flow(element, options = {}) {
        const duration = options.duration || 'var(--transition-golden-slow)';
        
        element.classList.add('sacred-flow-pattern');
        element.style.setProperty('--flow-duration', duration);

        return {
            start() {
                element.style.animation = 
                    `divineFlow ${duration} linear infinite`;
            },
            stop() {
                element.classList.remove('sacred-flow-pattern');
                element.style.animation = '';
            }
        };
    },

    /**
     * Merkaba Motion Pattern
     */
    merkaba(element, options = {}) {
        const duration = options.duration || 'var(--transition-golden-slow)';
        
        element.classList.add('sacred-merkaba-motion');
        element.style.setProperty('--merkaba-duration', duration);

        return {
            start() {
                element.style.animation = 
                    `merkabaRotate ${duration} linear infinite`;
            },
            stop() {
                element.classList.remove('sacred-merkaba-motion');
                element.style.animation = '';
            }
        };
    },

    /**
     * Sacred Wave Pattern
     */
    wave(element, options = {}) {
        const duration = options.duration || 'var(--transition-golden-slow)';
        const height = options.height || 
            'calc(var(--phi-space-4) * var(--phi))';

        element.classList.add('sacred-wave-pattern');
        element.style.setProperty('--wave-duration', duration);
        element.style.setProperty('--wave-height', height);

        return {
            start() {
                element.style.animation = 
                    `sacredWave ${duration} linear infinite`;
            },
            stop() {
                element.classList.remove('sacred-wave-pattern');
                element.style.animation = '';
            }
        };
    },

    /**
     * Divine Vortex Pattern
     */
    vortex(element, options = {}) {
        const duration = options.duration || 'var(--transition-golden-slow)';
        
        element.classList.add('sacred-vortex-pattern');
        element.style.setProperty('--vortex-duration', duration);

        return {
            start() {
                element.style.animation = 
                    `vortexSpin ${duration} linear infinite`;
            },
            stop() {
                element.classList.remove('sacred-vortex-pattern');
                element.style.animation = '';
            }
        };
    },

    /**
     * Sacred Breath Pattern
     */
    breath(element, options = {}) {
        const duration = options.duration || 'var(--transition-golden-slow)';
        
        element.classList.add('sacred-breath-pattern');
        element.style.setProperty('--breath-duration', duration);

        return {
            start() {
                element.style.animation = 
                    `sacredBreath calc(${duration} * 2) var(--ease-golden) infinite`;
            },
            stop() {
                element.classList.remove('sacred-breath-pattern');
                element.style.animation = '';
            }
        };
    }
};

// Add patterns to public API
Object.assign(SacredAnimations, {
    patterns: animationPatterns
});
/**
 * Sacred Motion Patterns
 * Implements divine movement manifestations from sacred-animations.css
 */
const SacredMotionPatterns = {
    /**
     * Sacred Orbit Pattern
     */
    orbit(element, options = {}) {
        const config = {
            radius: options.radius || `calc(var(--phi-space-6) * var(--phi))`,
            duration: options.duration || `calc(var(--transition-golden-slow) * 2)`,
            elements: options.elements || 4
        };

        element.classList.add('sacred-orbit');
        element.style.setProperty('--orbit-radius', config.radius);
        element.style.setProperty('--orbit-duration', config.duration);

        // Create orbit elements
        for (let i = 0; i < config.elements; i++) {
            const orbitElement = document.createElement('div');
            orbitElement.className = 'sacred-orbit-element';
            element.appendChild(orbitElement);
        }

        return {
            start() {
                element.querySelectorAll('.sacred-orbit-element').forEach((el, i) => {
                    el.style.animationDelay = `calc(${config.duration} / ${-(i + 1)})`;
                });
            },
            stop() {
                element.classList.remove('sacred-orbit');
                element.querySelectorAll('.sacred-orbit-element').forEach(el => el.remove());
            }
        };
    },

    /**
     * Sacred Pulse Pattern
     */
    pulse(element, options = {}) {
        const config = {
            duration: options.duration || 'var(--transition-golden-normal)',
            color: options.color || 'var(--color-ethereal-blue)'
        };

        element.classList.add('sacred-pulse-pattern');
        element.style.setProperty('--pulse-duration', config.duration);
        element.style.setProperty('--pulse-color', config.color);

        return {
            start() {
                element.style.animation = `sacredPulse ${config.duration} var(--ease-golden) infinite`;
            },
            stop() {
                element.classList.remove('sacred-pulse-pattern');
                element.style.animation = '';
            }
        };
    },

    /**
     * Divine Flow Pattern
     */
    flow(element, options = {}) {
        const config = {
            duration: options.duration || 'var(--transition-golden-slow)'
        };

        element.classList.add('sacred-flow-pattern');
        element.style.setProperty('--flow-duration', config.duration);

        return {
            start() {
                element.style.animation = `divineFlow ${config.duration} linear infinite`;
            },
            stop() {
                element.classList.remove('sacred-flow-pattern');
                element.style.animation = '';
            }
        };
    },

    /**
     * Sacred Spiral Pattern
     */
    spiral(element, options = {}) {
        const config = {
            duration: options.duration || 'var(--transition-golden-slow)',
            scale: options.scale || 'var(--phi)'
        };

        element.classList.add('sacred-spiral-pattern');
        element.style.setProperty('--spiral-duration', config.duration);
        element.style.setProperty('--spiral-scale', config.scale);

        return {
            start() {
                element.style.animation = `sacredSpiral ${config.duration} var(--ease-golden) infinite alternate`;
            },
            stop() {
                element.classList.remove('sacred-spiral-pattern');
                element.style.animation = '';
            }
        };
    },

    /**
     * Merkaba Motion Pattern
     */
    merkaba(element, options = {}) {
        const config = {
            duration: options.duration || 'var(--transition-golden-slow)'
        };

        element.classList.add('sacred-merkaba-motion');
        element.style.setProperty('--merkaba-duration', config.duration);

        return {
            start() {
                element.style.animation = `merkabaRotate ${config.duration} linear infinite`;
            },
            stop() {
                element.classList.remove('sacred-merkaba-motion');
                element.style.animation = '';
            }
        };
    },

    /**
     * Sacred Wave Pattern
     */
    wave(element, options = {}) {
        const config = {
            duration: options.duration || 'var(--transition-golden-slow)',
            height: options.height || 'calc(var(--phi-space-4) * var(--phi))'
        };

        element.classList.add('sacred-wave-pattern');
        element.style.setProperty('--wave-duration', config.duration);
        element.style.setProperty('--wave-height', config.height);

        return {
            start() {
                element.style.animation = `sacredWave ${config.duration} linear infinite`;
            },
            stop() {
                element.classList.remove('sacred-wave-pattern');
                element.style.animation = '';
            }
        };
    }
};

// Add motion patterns to SacredAnimations
Object.assign(SacredAnimations, {
    motions: SacredMotionPatterns
});
// Adding to sacred-animations.js...

/**
 * Component Transition System
 * Implements sacred element transformations
 */
const ComponentTransitions = {
    /**
     * Sacred Reveal Component
     */
    reveal(element, options = {}) {
        const config = {
            duration: options.duration || 'var(--transition-golden-normal)',
            angle: options.angle || 'var(--transition-angle-sacred)',
            origin: options.origin || 'left'
        };

        element.classList.add('sacred-reveal');
        element.style.setProperty('--reveal-angle', config.angle);
        element.style.setProperty('--component-duration', config.duration);

        return {
            enter() {
                element.dataset.state = 'entering';
                requestAnimationFrame(() => {
                    element.dataset.state = 'entered';
                });
            },
            exit() {
                element.dataset.state = 'exiting';
            }
        };
    },

    /**
     * Sacred Flow Component
     */
    flow(element, options = {}) {
        const config = {
            duration: options.duration || 'var(--transition-golden-normal)',
            distance: options.distance || 'var(--transition-distance-md)',
            rotation: options.rotation || 'var(--transition-angle-golden)'
        };

        element.classList.add('sacred-flow');
        element.style.setProperty('--flow-distance', config.distance);
        element.style.setProperty('--flow-rotation', config.rotation);
        element.style.setProperty('--component-duration', config.duration);

        return {
            enter() {
                element.dataset.state = 'entering';
                requestAnimationFrame(() => {
                    element.dataset.state = 'entered';
                });
            },
            exit() {
                element.dataset.state = 'exiting';
            }
        };
    },

    /**
     * Sacred Scale Component
     */
    scale(element, options = {}) {
        const config = {
            duration: options.duration || 'var(--transition-golden-normal)',
            origin: options.origin || 'center'
        };

        element.classList.add('sacred-scale');
        element.style.setProperty('--scale-origin', config.origin);
        element.style.setProperty('--component-duration', config.duration);

        return {
            enter() {
                element.dataset.state = 'entering';
                requestAnimationFrame(() => {
                    element.dataset.state = 'entered';
                });
            },
            exit() {
                element.dataset.state = 'exiting';
            }
        };
    },

    /**
     * Divine Rotate Component
     */
    rotate(element, options = {}) {
        const config = {
            duration: options.duration || 'var(--transition-golden-normal)',
            angle: options.angle || 'var(--transition-angle-sacred)'
        };

        element.classList.add('sacred-rotate');
        element.style.setProperty('--rotate-angle', config.angle);
        element.style.setProperty('--component-duration', config.duration);

        return {
            enter() {
                element.dataset.state = 'entering';
                requestAnimationFrame(() => {
                    element.dataset.state = 'entered';
                });
            },
            exit() {
                element.dataset.state = 'exiting';
            }
        };
    },

    /**
     * Flip Component
     */
    flip(element, options = {}) {
        const config = {
            duration: options.duration || 'var(--transition-golden-normal)',
            perspective: options.perspective || '1000px'
        };

        element.classList.add('sacred-flip');
        element.style.setProperty('--flip-perspective', config.perspective);
        element.style.setProperty('--component-duration', config.duration);

        return {
            enter() {
                element.dataset.state = 'entering';
                requestAnimationFrame(() => {
                    element.dataset.state = 'entered';
                });
            },
            exit() {
                element.dataset.state = 'exiting';
            }
        };
    }
};

// Add component transitions to SacredAnimations
Object.assign(SacredAnimations, {
    components: ComponentTransitions
});
