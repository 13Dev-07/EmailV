/**
 * Sacred Loader System
 * Divine loading manifestations based on sacred geometry
 * Version: 1.0.0
 */

const SacredLoader = (function() {
    'use strict';

    // Core Constants aligned with CSS variables
    const LOADER_CONSTANTS = {
        TYPES: {
            MERKABA: 'sacred-loader-merkaba',
            FLOWER: 'sacred-loader-flower',
            WAVE: 'sacred-loader-wave',
            VESICA: 'sacred-loader-vesica',
            METATRON: 'sacred-loader-metatron',
            SPIRAL: 'sacred-loader-spiral',
            SRI_YANTRA: 'sacred-loader-sri-yantra',
            SEED_OF_LIFE: 'sacred-loader-seed-of-life',
            PLATONIC: 'sacred-loader-platonic',
            TORUS: 'sacred-loader-torus',
            MERKABA_STAR: 'sacred-loader-merkaba-star'
        },
        
        STATES: {
            LOADING: 'loading',
            ACTIVE: 'active',
            COMPLETE: 'complete',
            ERROR: 'error'
        },

        TRANSITIONS: {
            FADE: 'sacred-loading-fade',
            SHIMMER: 'sacred-loading-shimmer',
            SKELETON: 'sacred-loading-skeleton',
            PROGRESSIVE: 'sacred-loading-progressive',
            PULSE: 'sacred-loading-pulse'
        }
    };

/**
 * Sacred Base Loader Class
 * Foundation for all sacred loader types
 */
class SacredBaseLoader {
    constructor(options = {}) {
        this.options = this.mergeOptions(options);
        this.element = null;
        this.state = LOADER_CONSTANTS.STATES.LOADING;
        this.initialize();
    }

    /**
     * Merge default options with user options
     */
    mergeOptions(options) {
        return {
            container: options.container || document.body,
            type: options.type || LOADER_CONSTANTS.TYPES.MERKABA,
            size: options.size || 'var(--phi-space-6)',
            color: options.color || 'var(--color-ethereal-blue)',
            background: options.background || 'var(--color-cosmic-background)',
            message: options.message || '',
            overlay: options.overlay !== false,
            animated: options.animated !== false,
            duration: options.duration || 'var(--transition-golden-normal)',
            easing: options.easing || 'var(--ease-golden)'
        };
    }

    /**
     * Initialize loader
     */
    initialize() {
        this.createLoader();
        if (this.options.animated) {
            this.setupAnimations();
        }
        this.setupEventListeners();
    }

    /**
     * Create loader element
     */
    createLoader() {
        // Create container
        this.element = document.createElement('div');
        this.element.className = `sacred-loader ${this.options.type}`;
        
        // Apply styles
        Object.assign(this.element.style, {
            width: this.options.size,
            height: this.options.size,
            '--loader-color': this.options.color,
            '--loader-duration': this.options.duration,
            '--loader-easing': this.options.easing
        });

        // Create overlay if needed
        if (this.options.overlay) {
            this.createOverlay();
        }

        // Add message if provided
        if (this.options.message) {
            this.addMessage();
        }

        // Add to container
        this.options.container.appendChild(this.element);
    }

    /**
     * Create overlay
     */
    createOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'sacred-loader-overlay';
        
        Object.assign(overlay.style, {
            position: 'fixed',
            inset: '0',
            background: this.options.background,
            backdropFilter: 'blur(var(--transition-overlay-blur))',
            opacity: 'var(--transition-overlay-opacity)',
            transition: `opacity ${this.options.duration} ${this.options.easing}`
        });

        this.element.appendChild(overlay);
    }

    /**
     * Add message
     */
    addMessage() {
        const message = document.createElement('div');
        message.className = 'sacred-loader-message';
        message.textContent = this.options.message;
        
        Object.assign(message.style, {
            marginTop: 'calc(var(--phi-space-4) * var(--phi))',
            color: this.options.color,
            fontSize: 'var(--font-size-sm)'
        });

        this.element.appendChild(message);
    }

    /**
     * Setup animations
     */
    setupAnimations() {
        this.element.style.animation = `${this.getAnimationName()} var(--loader-duration) var(--loader-easing) infinite`;
    }

    /**
     * Get animation name based on loader type
     */
    getAnimationName() {
        switch (this.options.type) {
            case LOADER_CONSTANTS.TYPES.MERKABA:
                return 'merkabaRotate';
            case LOADER_CONSTANTS.TYPES.FLOWER:
                return 'flowerOfLife';
            case LOADER_CONSTANTS.TYPES.WAVE:
                return 'divineWave';
            default:
                return 'sacredSpin';
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Handle reduced motion preference
        const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
        mediaQuery.addEventListener('change', () => this.handleReducedMotion(mediaQuery));
        this.handleReducedMotion(mediaQuery);
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        if (mediaQuery.matches) {
            this.element.style.animation = 'none';
        } else if (this.options.animated) {
            this.setupAnimations();
        }
    }

    /**
     * Show loader
     */
    show() {
        this.element.style.display = 'flex';
        requestAnimationFrame(() => {
            this.element.style.opacity = '1';
        });
    }

    /**
     * Hide loader
     */
    hide() {
        this.element.style.opacity = '0';
        this.element.addEventListener('transitionend', () => {
            this.element.style.display = 'none';
        }, { once: true });
    }

    /**
     * Update loader state
     */
    setState(state) {
        this.state = state;
        this.element.dataset.state = state;
    }

    /**
     * Destroy loader
     */
    destroy() {
        if (this.element && this.element.parentNode) {
            this.element.parentNode.removeChild(this.element);
        }
        this.element = null;
    }
}
/**
 * Sacred Loading State Management
 * Manages divine loading states and transitions
 */
class SacredLoadingState {
    constructor(loader) {
        this.loader = loader;
        this.currentState = LOADER_CONSTANTS.STATES.LOADING;
        this.progress = 0;
        this.transitions = new Map();
        this.initialize();
    }

    /**
     * Initialize state management
     */
    initialize() {
        this.setupTransitions();
        this.updateState(this.currentState);
    }

    /**
     * Setup state transitions
     */
    setupTransitions() {
        this.transitions.set(LOADER_CONSTANTS.STATES.LOADING, {
            enter: () => {
                this.loader.element.classList.add('sacred-loading');
                this.loader.element.style.animation = `${this.getLoadingAnimation()} var(--loader-duration) var(--loader-easing) infinite`;
            },
            exit: () => {
                this.loader.element.classList.remove('sacred-loading');
                this.loader.element.style.animation = 'none';
            }
        });

        this.transitions.set(LOADER_CONSTANTS.STATES.ACTIVE, {
            enter: () => {
                this.loader.element.classList.add('sacred-active');
                this.updateProgress(this.progress);
            },
            exit: () => {
                this.loader.element.classList.remove('sacred-active');
            }
        });

        this.transitions.set(LOADER_CONSTANTS.STATES.COMPLETE, {
            enter: () => {
                this.loader.element.classList.add('sacred-complete');
                this.updateProgress(100);
                this.triggerCompleteAnimation();
            },
            exit: () => {
                this.loader.element.classList.remove('sacred-complete');
            }
        });

        this.transitions.set(LOADER_CONSTANTS.STATES.ERROR, {
            enter: () => {
                this.loader.element.classList.add('sacred-error');
                this.triggerErrorAnimation();
            },
            exit: () => {
                this.loader.element.classList.remove('sacred-error');
            }
        });
    }

    /**
     * Update loader state
     */
    updateState(newState) {
        if (this.currentState === newState) return;

        const prevTransition = this.transitions.get(this.currentState);
        const nextTransition = this.transitions.get(newState);

        if (prevTransition?.exit) {
            prevTransition.exit();
        }

        if (nextTransition?.enter) {
            nextTransition.enter();
        }

        this.currentState = newState;
        this.loader.element.dataset.state = newState;
    }

    /**
     * Update progress value
     */
    updateProgress(value) {
        this.progress = Math.min(100, Math.max(0, value));
        this.loader.element.style.setProperty('--loader-progress', `${this.progress}%`);
        
        if (this.progress === 100) {
            this.updateState(LOADER_CONSTANTS.STATES.COMPLETE);
        } else if (this.progress > 0) {
            this.updateState(LOADER_CONSTANTS.STATES.ACTIVE);
        }
    }

    /**
     * Get loading animation based on loader type
     */
    getLoadingAnimation() {
        switch (this.loader.options.type) {
            case LOADER_CONSTANTS.TYPES.MERKABA:
                return 'sacredMerkaba';
            case LOADER_CONSTANTS.TYPES.FLOWER:
                return 'sacredFlower';
            case LOADER_CONSTANTS.TYPES.WAVE:
                return 'sacredWave';
            default:
                return 'sacredSpin';
        }
    }

    /**
     * Trigger complete animation
     */
    triggerCompleteAnimation() {
        this.loader.element.style.animation = 'sacredComplete var(--loader-duration) var(--loader-easing) forwards';
        
        this.loader.element.addEventListener('animationend', () => {
            if (this.loader.options.autoHide) {
                this.loader.hide();
            }
        }, { once: true });
    }

    /**
     * Trigger error animation
     */
    triggerErrorAnimation() {
        this.loader.element.style.animation = 'sacredError var(--loader-duration) var(--loader-easing) forwards';
    }

    /**
     * Reset state
     */
    reset() {
        this.progress = 0;
        this.updateState(LOADER_CONSTANTS.STATES.LOADING);
        this.loader.element.style.removeProperty('--loader-progress');
    }
}

/**
 * Sacred Transition System
 * Manages divine transitions between loader states
 */
class SacredTransitionSystem {
    constructor(loader) {
        this.loader = loader;
        this.currentTransition = null;
        this.transitionQueue = [];
        this.initialize();
    }

    /**
     * Initialize transition system
     */
    initialize() {
        this.setupTransitionStates();
        this.setupTransitionEffects();
    }

    /**
     * Setup transition states
     */
    setupTransitionStates() {
        this.transitions = {
            fade: {
                enter: (element) => {
                    element.style.animation = 'fadeEnter var(--transition-golden-normal) var(--ease-golden) forwards';
                },
                exit: (element) => {
                    element.style.animation = 'fadeExit var(--transition-golden-normal) var(--ease-golden) forwards';
                }
            },
            spiral: {
                enter: (element) => {
                    element.style.animation = 'spiralEnter var(--transition-golden-slow) var(--ease-golden) forwards';
                },
                exit: (element) => {
                    element.style.animation = 'spiralExit var(--transition-golden-slow) var(--ease-golden) forwards';
                }
            },
            flow: {
                enter: (element) => {
                    element.style.animation = 'flowEnter var(--transition-golden-normal) var(--ease-golden) forwards';
                },
                exit: (element) => {
                    element.style.animation = 'flowExit var(--transition-golden-normal) var(--ease-golden) forwards';
                }
            },
            expand: {
                enter: (element) => {
                    element.style.animation = 'expandEnter var(--transition-golden-normal) var(--ease-golden) forwards';
                },
                exit: (element) => {
                    element.style.animation = 'expandExit var(--transition-golden-normal) var(--ease-golden) forwards';
                }
            }
        };
    }

    /**
     * Setup transition effects
     */
    setupTransitionEffects() {
        this.effects = {
            veil: (element) => {
                const veil = document.createElement('div');
                veil.className = 'sacred-transition-veil';
                element.appendChild(veil);
                return veil;
            },
            portal: (element) => {
                element.style.perspective = '1000px';
                element.style.transformStyle = 'preserve-3d';
            }
        };
    }

    /**
     * Transition to new state
     */
    async transition(from, to, type = 'fade') {
        if (this.currentTransition) {
            this.transitionQueue.push({ from, to, type });
            return;
        }

        this.currentTransition = { from, to, type };

        try {
            await this.executeTransition(from, to, type);
        } finally {
            this.currentTransition = null;
            this.processQueue();
        }
    }

    /**
     * Execute transition
     */
    async executeTransition(from, to, type) {
        const transition = this.transitions[type];
        if (!transition) return;

        return new Promise((resolve) => {
            // Exit phase
            transition.exit(from);
            from.addEventListener('animationend', () => {
                // Enter phase
                transition.enter(to);
                to.addEventListener('animationend', resolve, { once: true });
            }, { once: true });
        });
    }

    /**
     * Process transition queue
     */
    processQueue() {
        if (this.transitionQueue.length > 0) {
            const next = this.transitionQueue.shift();
            this.transition(next.from, next.to, next.type);
        }
    }

    /**
     * Add custom transition
     */
    addTransition(name, handlers) {
        this.transitions[name] = handlers;
    }

    /**
     * Add transition effect
     */
    addEffect(name, handler) {
        this.effects[name] = handler;
    }

    /**
     * Apply effect to element
     */
    applyEffect(element, effect) {
        const effectHandler = this.effects[effect];
        if (effectHandler) {
            return effectHandler(element);
        }
    }
}

/**
 * Sacred Merkaba Loader
 * Based on sacred geometry principles
 */
class MerkabaLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.MERKABA
        });
    }

    createLoader() {
        super.createLoader();
        
        // Create Merkaba structure
        const merkaba = document.createElement('div');
        merkaba.className = 'sacred-merkaba';

        // Create tetrahedrons
        const upTetra = document.createElement('div');
        upTetra.className = 'merkaba-tetrahedron merkaba-up';
        
        const downTetra = document.createElement('div');
        downTetra.className = 'merkaba-tetrahedron merkaba-down';

        merkaba.appendChild(upTetra);
        merkaba.appendChild(downTetra);
        this.element.appendChild(merkaba);
    }

    setupAnimations() {
        this.element.style.animation = 'merkabaRotate var(--loader-duration) var(--loader-easing) infinite';
    }
}

/**
 * Sacred Flower of Life Loader
 * Based on sacred geometry patterns
 */
class FlowerLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.FLOWER
        });
    }

    createLoader() {
        super.createLoader();
        
        const flower = document.createElement('div');
        flower.className = 'sacred-flower';

        // Create circles based on Flower of Life pattern
        for (let i = 0; i < 7; i++) {
            const circle = document.createElement('div');
            circle.className = 'flower-circle';
            circle.style.setProperty('--circle-index', i);
            flower.appendChild(circle);
        }

        this.element.appendChild(flower);
    }

    setupAnimations() {
        this.element.style.animation = 'flowerOfLife var(--loader-duration) var(--loader-easing) infinite';
    }
}

/**
 * Sacred Wave Loader
 * Based on divine flow patterns
 */
class WaveLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.WAVE
        });
    }

    createLoader() {
        super.createLoader();
        
        const wave = document.createElement('div');
        wave.className = 'sacred-wave';

        // Create wave particles
        for (let i = 0; i < 5; i++) {
            const particle = document.createElement('div');
            particle.className = 'wave-particle';
            particle.style.setProperty('--particle-index', i);
            wave.appendChild(particle);
        }

        this.element.appendChild(wave);
    }

    setupAnimations() {
        this.element.style.animation = 'divineWave var(--loader-duration) var(--loader-easing) infinite';
    }
}

/**
 * Sacred Vesica Loader
 * Based on vesica piscis geometry
 */
class VesicaLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.VESICA
        });
    }

    createLoader() {
        super.createLoader();
        
        const vesica = document.createElement('div');
        vesica.className = 'sacred-vesica';

        // Create overlapping circles
        const circle1 = document.createElement('div');
        circle1.className = 'vesica-circle circle-1';
        
        const circle2 = document.createElement('div');
        circle2.className = 'vesica-circle circle-2';

        vesica.appendChild(circle1);
        vesica.appendChild(circle2);
        this.element.appendChild(vesica);
    }

    setupAnimations() {
        this.element.style.animation = 'vesicaPiscis var(--loader-duration) var(--loader-easing) infinite';
    }
}

/**
 * Sacred Metatron Loader
 * Based on Metatron's Cube sacred geometry
 */
class MetatronLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.METATRON
        });
    }

    createLoader() {
        super.createLoader();
        
        const metatron = document.createElement('div');
        metatron.className = 'sacred-metatron';

        // Create center circle
        const centerCircle = document.createElement('div');
        centerCircle.className = 'metatron-center';
        metatron.appendChild(centerCircle);

        // Create first ring of circles
        for (let i = 0; i < 6; i++) {
            const circle = document.createElement('div');
            circle.className = 'metatron-circle first-ring';
            circle.style.setProperty('--circle-index', i);
            metatron.appendChild(circle);
        }

        // Create second ring of circles
        for (let i = 0; i < 6; i++) {
            const circle = document.createElement('div');
            circle.className = 'metatron-circle second-ring';
            circle.style.setProperty('--circle-index', i);
            metatron.appendChild(circle);
        }

        // Create connecting lines
        const lines = document.createElement('div');
        lines.className = 'metatron-lines';
        
        // Create 13 lines for complete Metatron's Cube
        for (let i = 0; i < 13; i++) {
            const line = document.createElement('div');
            line.className = 'metatron-line';
            line.style.setProperty('--line-index', i);
            lines.appendChild(line);
        }

        metatron.appendChild(lines);
        this.element.appendChild(metatron);
    }

    setupAnimations() {
        const duration = 'var(--transition-golden-slow)';
        const circles = this.element.querySelectorAll('.metatron-circle');
        const lines = this.element.querySelectorAll('.metatron-line');

        // Animate circles
        circles.forEach((circle, index) => {
            circle.style.animation = `metatronCircle ${duration} var(--ease-golden) infinite`;
            circle.style.animationDelay = `calc(${index} * var(--transition-delay-minimal))`;
        });

        // Animate lines
        lines.forEach((line, index) => {
            line.style.animation = `metatronLine ${duration} var(--ease-divine) infinite`;
            line.style.animationDelay = `calc(${index} * var(--transition-delay-short))`;
        });

        // Animate center
        const center = this.element.querySelector('.metatron-center');
        center.style.animation = `metatronCenter ${duration} var(--ease-spiral) infinite`;
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        const elements = this.element.querySelectorAll('.metatron-circle, .metatron-line, .metatron-center');
        
        elements.forEach(element => {
            if (mediaQuery.matches) {
                element.style.animation = 'none';
            } else {
                this.setupAnimations();
            }
        });
    }

    /**
     * Update loader state
     */
    setState(state) {
        super.setState(state);
        
        if (state === LOADER_CONSTANTS.STATES.COMPLETE) {
            this.element.classList.add('metatron-complete');
        } else if (state === LOADER_CONSTANTS.STATES.ERROR) {
            this.element.classList.add('metatron-error');
        }
    }
}
/**
 * Sacred Flower of Life Loader
 * Based on sacred geometry principles and divine proportions
 */
class FlowerOfLifeLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.FLOWER_OF_LIFE
        });
    }

    /**
     * Create loader structure
     */
    createLoader() {
        super.createLoader();
        
        const flowerContainer = document.createElement('div');
        flowerContainer.className = 'sacred-flower-container';

        // Create center circle
        const centerCircle = document.createElement('div');
        centerCircle.className = 'flower-circle center';
        flowerContainer.appendChild(centerCircle);

        // Create first ring of circles
        for (let i = 0; i < 6; i++) {
            const circle = document.createElement('div');
            circle.className = 'flower-circle first-ring';
            circle.style.setProperty('--circle-index', i);
            circle.style.setProperty('--circle-angle', `${i * 60}deg`);
            flowerContainer.appendChild(circle);
        }

        // Create second ring of circles
        for (let i = 0; i < 12; i++) {
            const circle = document.createElement('div');
            circle.className = 'flower-circle second-ring';
            circle.style.setProperty('--circle-index', i);
            circle.style.setProperty('--circle-angle', `${i * 30}deg`);
            flowerContainer.appendChild(circle);
        }

        this.element.appendChild(flowerContainer);
    }

    /**
     * Setup animations
     */
    setupAnimations() {
        const circles = this.element.querySelectorAll('.flower-circle');
        
        circles.forEach((circle, index) => {
            circle.style.animation = `
                flowerOfLife var(--time-harmonic) var(--ease-golden) infinite ${index * 100}ms,
                sacredPulse var(--time-flowing) var(--ease-divine) infinite ${index * 200}ms
            `;
        });
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        const circles = this.element.querySelectorAll('.flower-circle');
        
        circles.forEach(circle => {
            if (mediaQuery.matches) {
                circle.style.animation = 'none';
            } else {
                this.setupAnimations();
            }
        });
    }

    /**
     * Update loader state
     */
    setState(state) {
        super.setState(state);
        
        if (state === LOADER_CONSTANTS.STATES.COMPLETE) {
            this.element.classList.add('flower-complete');
        } else if (state === LOADER_CONSTANTS.STATES.ERROR) {
            this.element.classList.add('flower-error');
        }
    }
}

/**
 * Sacred Wave Loader
 * Based on divine flow patterns and sacred geometry
 */
class SacredWaveLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.WAVE
        });
    }

    /**
     * Create loader structure
     */
    createLoader() {
        super.createLoader();
        
        const waveContainer = document.createElement('div');
        waveContainer.className = 'sacred-wave-container';

        // Create wave particles based on golden ratio
        const particleCount = Math.round(SACRED_CONSTANTS.MATH.PHI.VALUE * 5);
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'wave-particle';
            particle.style.setProperty('--particle-index', i);
            particle.style.setProperty('--particle-delay', 
                `calc(${i} * var(--time-swift) / ${particleCount})`);
            waveContainer.appendChild(particle);
        }

        // Create wave path
        const wavePath = document.createElement('div');
        wavePath.className = 'wave-path';
        waveContainer.appendChild(wavePath);

        this.element.appendChild(waveContainer);
    }

    /**
     * Setup animations
     */
    setupAnimations() {
        const particles = this.element.querySelectorAll('.wave-particle');
        const wavePath = this.element.querySelector('.wave-path');

        // Animate particles
        particles.forEach((particle, index) => {
            particle.style.animation = `
                waveFloat var(--time-flowing) var(--ease-divine) infinite,
                waveOpacity var(--time-harmonic) var(--ease-golden) infinite
            `;
            particle.style.animationDelay = `calc(
                var(--particle-delay) + 
                ${index * SACRED_CONSTANTS.MATH.PHI_INVERSE}s
            )`;
        });

        // Animate wave path
        wavePath.style.animation = `
            wavePath var(--time-flowing) var(--ease-spiral) infinite,
            waveGlow var(--time-harmonic) var(--ease-divine) infinite
        `;
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        const elements = this.element.querySelectorAll('.wave-particle, .wave-path');
        
        elements.forEach(element => {
            if (mediaQuery.matches) {
                element.style.animation = 'none';
            } else {
                this.setupAnimations();
            }
        });
    }

    /**
     * Update loader state
     */
    setState(state) {
        super.setState(state);
        
        if (state === LOADER_CONSTANTS.STATES.COMPLETE) {
            this.element.classList.add('wave-complete');
        } else if (state === LOADER_CONSTANTS.STATES.ERROR) {
            this.element.classList.add('wave-error');
        }
    }
}

/**
 * Sacred Vesica Piscis Loader
 * Based on sacred geometry intersection principles
 */
class VesicaPiscisLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.VESICA
        });
    }

    /**
     * Create loader structure
     */
    createLoader() {
        super.createLoader();
        
        const vesicaContainer = document.createElement('div');
        vesicaContainer.className = 'sacred-vesica-container';

        // Create overlapping circles
        const circle1 = document.createElement('div');
        circle1.className = 'vesica-circle circle-left';
        
        const circle2 = document.createElement('div');
        circle2.className = 'vesica-circle circle-right';

        // Create sacred intersection
        const intersection = document.createElement('div');
        intersection.className = 'vesica-intersection';

        // Create sacred mandorla (almond shape)
        const mandorla = document.createElement('div');
        mandorla.className = 'vesica-mandorla';

        vesicaContainer.appendChild(circle1);
        vesicaContainer.appendChild(circle2);
        vesicaContainer.appendChild(intersection);
        vesicaContainer.appendChild(mandorla);

        this.element.appendChild(vesicaContainer);
    }

    /**
     * Setup animations
     */
    setupAnimations() {
        const circles = this.element.querySelectorAll('.vesica-circle');
        const intersection = this.element.querySelector('.vesica-intersection');
        const mandorla = this.element.querySelector('.vesica-mandorla');

        // Animate circles
        circles.forEach((circle, index) => {
            circle.style.animation = `
                vesicaPiscis var(--time-harmonic) var(--ease-divine) infinite alternate,
                sacredPulse var(--time-flowing) var(--ease-golden) infinite ${index * 200}ms
            `;
        });

        // Animate intersection
        intersection.style.animation = `
            vesicaGlow var(--time-flowing) var(--ease-spiral) infinite
        `;

        // Animate mandorla
        mandorla.style.animation = `
            vesicaBreath var(--time-harmonic) var(--ease-natural) infinite
        `;
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        const elements = this.element.querySelectorAll('.vesica-circle, .vesica-intersection, .vesica-mandorla');
        
        elements.forEach(element => {
            if (mediaQuery.matches) {
                element.style.animation = 'none';
            } else {
                this.setupAnimations();
            }
        });
    }

    /**
     * Update loader state
     */
    setState(state) {
        super.setState(state);
        
        if (state === LOADER_CONSTANTS.STATES.COMPLETE) {
            this.element.classList.add('vesica-complete');
        } else if (state === LOADER_CONSTANTS.STATES.ERROR) {
            this.element.classList.add('vesica-error');
        }
    }
}

/**
 * Sacred Fibonacci Spiral Loader
 * Based on divine proportions and sacred geometry
 */
class FibonacciSpiralLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.SPIRAL
        });
    }

    /**
     * Create loader structure
     */
    createLoader() {
        super.createLoader();
        
        const spiralContainer = document.createElement('div');
        spiralContainer.className = 'sacred-spiral-container';

        // Create spiral segments based on Fibonacci sequence
        const segments = this.createSpiralSegments();
        segments.forEach(segment => spiralContainer.appendChild(segment));

        // Create center point
        const centerPoint = document.createElement('div');
        centerPoint.className = 'spiral-center';
        spiralContainer.appendChild(centerPoint);

        this.element.appendChild(spiralContainer);
    }

    /**
     * Create spiral segments
     */
    createSpiralSegments() {
        const segments = [];
        const fibSequence = [1, 1, 2, 3, 5, 8, 13];
        
        fibSequence.forEach((num, index) => {
            const segment = document.createElement('div');
            segment.className = 'spiral-segment';
            segment.style.setProperty('--segment-index', index);
            segment.style.setProperty('--segment-size', `${num * SACRED_CONSTANTS.MATH.PHI.VALUE}rem`);
            segment.style.setProperty('--segment-angle', `${index * SACRED_CONSTANTS.MATH.ANGLES.GOLDEN}deg`);
            
            segments.push(segment);
        });

        return segments;
    }

    /**
     * Setup animations
     */
    setupAnimations() {
        const segments = this.element.querySelectorAll('.spiral-segment');
        const center = this.element.querySelector('.spiral-center');

        // Animate spiral segments
        segments.forEach((segment, index) => {
            segment.style.animation = `
                spiralGrow var(--time-flowing) var(--ease-spiral) infinite ${index * 100}ms,
                spiralRotate var(--time-harmonic) var(--ease-golden) infinite ${index * 200}ms
            `;
        });

        // Animate center point
        center.style.animation = `
            sacredPulse var(--time-harmonic) var(--ease-divine) infinite
        `;
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        const elements = this.element.querySelectorAll('.spiral-segment, .spiral-center');
        
        elements.forEach(element => {
            if (mediaQuery.matches) {
                element.style.animation = 'none';
            } else {
                this.setupAnimations();
            }
        });
    }

    /**
     * Update loader state
     */
    setState(state) {
        super.setState(state);
        
        if (state === LOADER_CONSTANTS.STATES.COMPLETE) {
            this.element.classList.add('spiral-complete');
        } else if (state === LOADER_CONSTANTS.STATES.ERROR) {
            this.element.classList.add('spiral-error');
        }
    }
}

/**
 * Sacred Sri Yantra Loader
 * Based on sacred geometry and divine proportions
 */
class SriYantraLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.SRI_YANTRA
        });
    }

    /**
     * Create loader structure
     */
    createLoader() {
        super.createLoader();
        
        const sriContainer = document.createElement('div');
        sriContainer.className = 'sacred-sri-yantra-container';

        // Create central bindu (point)
        const bindu = document.createElement('div');
        bindu.className = 'sri-yantra-bindu';
        sriContainer.appendChild(bindu);

        // Create nine interlocking triangles
        for (let i = 0; i < 9; i++) {
            const triangle = document.createElement('div');
            triangle.className = 'sri-yantra-triangle';
            triangle.style.setProperty('--triangle-index', i);
            triangle.style.setProperty('--triangle-angle', 
                `${i * SACRED_CONSTANTS.MATH.ANGLES.GOLDEN}deg`);
            sriContainer.appendChild(triangle);
        }

        // Create outer circles
        for (let i = 0; i < 3; i++) {
            const circle = document.createElement('div');
            circle.className = 'sri-yantra-circle';
            circle.style.setProperty('--circle-index', i);
            sriContainer.appendChild(circle);
        }

        // Create lotus petals
        for (let i = 0; i < 8; i++) {
            const petal = document.createElement('div');
            petal.className = 'sri-yantra-petal';
            petal.style.setProperty('--petal-index', i);
            petal.style.setProperty('--petal-angle', `${i * 45}deg`);
            sriContainer.appendChild(petal);
        }

        this.element.appendChild(sriContainer);
    }

    /**
     * Setup animations
     */
    setupAnimations() {
        const triangles = this.element.querySelectorAll('.sri-yantra-triangle');
        const circles = this.element.querySelectorAll('.sri-yantra-circle');
        const petals = this.element.querySelectorAll('.sri-yantra-petal');
        const bindu = this.element.querySelector('.sri-yantra-bindu');

        // Animate triangles
        triangles.forEach((triangle, index) => {
            triangle.style.animation = `
                sriYantraRotate var(--time-flowing) var(--ease-divine) infinite ${index * 200}ms,
                sacredPulse var(--time-harmonic) var(--ease-golden) infinite ${index * 100}ms
            `;
        });

        // Animate circles
        circles.forEach((circle, index) => {
            circle.style.animation = `
                sriYantraExpand var(--time-harmonic) var(--ease-spiral) infinite ${index * 300}ms,
                sacredPulse var(--time-flowing) var(--ease-divine) infinite ${index * 200}ms
            `;
        });

        // Animate petals
        petals.forEach((petal, index) => {
            petal.style.animation = `
                sriYantraBloom var(--time-flowing) var(--ease-golden) infinite ${index * 100}ms
            `;
        });

        // Animate bindu
        bindu.style.animation = `
            sacredPulse var(--time-harmonic) var(--ease-divine) infinite
        `;
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        const elements = this.element.querySelectorAll(
            '.sri-yantra-triangle, .sri-yantra-circle, .sri-yantra-petal, .sri-yantra-bindu'
        );
        
        elements.forEach(element => {
            if (mediaQuery.matches) {
                element.style.animation = 'none';
            } else {
                this.setupAnimations();
            }
        });
    }

    /**
     * Update loader state
     */
    setState(state) {
        super.setState(state);
        
        if (state === LOADER_CONSTANTS.STATES.COMPLETE) {
            this.element.classList.add('sri-yantra-complete');
        } else if (state === LOADER_CONSTANTS.STATES.ERROR) {
            this.element.classList.add('sri-yantra-error');
        }
    }
}

/**
 * Sacred Seed of Life Loader
 * Based on sacred geometry principles and divine proportions
 */
class SeedOfLifeLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.SEED_OF_LIFE
        });
    }

    /**
     * Create loader structure
     */
    createLoader() {
        super.createLoader();
        
        const seedContainer = document.createElement('div');
        seedContainer.className = 'sacred-seed-container';

        // Create center circle
        const centerCircle = document.createElement('div');
        centerCircle.className = 'seed-circle center';
        seedContainer.appendChild(centerCircle);

        // Create six surrounding circles
        for (let i = 0; i < 6; i++) {
            const circle = document.createElement('div');
            circle.className = 'seed-circle';
            circle.style.setProperty('--circle-index', i);
            circle.style.setProperty('--circle-angle', `${i * 60}deg`);
            seedContainer.appendChild(circle);
        }

        // Create outer ring
        const outerRing = document.createElement('div');
        outerRing.className = 'seed-outer-ring';
        seedContainer.appendChild(outerRing);

        this.element.appendChild(seedContainer);
    }

    /**
     * Setup animations
     */
    setupAnimations() {
        const circles = this.element.querySelectorAll('.seed-circle');
        const outerRing = this.element.querySelector('.seed-outer-ring');

        // Animate circles
        circles.forEach((circle, index) => {
            circle.style.animation = `
                seedOfLife var(--time-harmonic) var(--ease-divine) infinite ${index * 100}ms,
                sacredPulse var(--time-flowing) var(--ease-golden) infinite ${index * 200}ms
            `;
        });

        // Animate outer ring
        outerRing.style.animation = `
            seedRing var(--time-flowing) var(--ease-spiral) infinite
        `;
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        const elements = this.element.querySelectorAll('.seed-circle, .seed-outer-ring');
        
        elements.forEach(element => {
            if (mediaQuery.matches) {
                element.style.animation = 'none';
            } else {
                this.setupAnimations();
            }
        });
    }

    /**
     * Update loader state
     */
    setState(state) {
        super.setState(state);
        
        if (state === LOADER_CONSTANTS.STATES.COMPLETE) {
            this.element.classList.add('seed-complete');
        } else if (state === LOADER_CONSTANTS.STATES.ERROR) {
            this.element.classList.add('seed-error');
        }
    }
}

/**
 * Sacred Platonic Solids Loader
 * Based on sacred geometry principles and divine proportions
 */
class PlatonicSolidsLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.PLATONIC
        });
    }

    /**
     * Create loader structure
     */
    createLoader() {
        super.createLoader();
        
        const platonicContainer = document.createElement('div');
        platonicContainer.className = 'sacred-platonic-container';

        // Create tetrahedron
        const tetrahedron = this.createTetrahedron();
        platonicContainer.appendChild(tetrahedron);

        // Create cube
        const cube = this.createCube();
        platonicContainer.appendChild(cube);

        // Create octahedron
        const octahedron = this.createOctahedron();
        platonicContainer.appendChild(octahedron);

        // Create icosahedron
        const icosahedron = this.createIcosahedron();
        platonicContainer.appendChild(icosahedron);

        // Create dodecahedron
        const dodecahedron = this.createDodecahedron();
        platonicContainer.appendChild(dodecahedron);

        this.element.appendChild(platonicContainer);
    }

    /**
     * Create tetrahedron element
     */
    createTetrahedron() {
        const tetrahedron = document.createElement('div');
        tetrahedron.className = 'platonic-solid tetrahedron';
        
        for (let i = 0; i < 4; i++) {
            const face = document.createElement('div');
            face.className = 'tetrahedron-face';
            face.style.setProperty('--face-index', i);
            tetrahedron.appendChild(face);
        }

        return tetrahedron;
    }

    /**
     * Create cube element
     */
    createCube() {
        const cube = document.createElement('div');
        cube.className = 'platonic-solid cube';
        
        for (let i = 0; i < 6; i++) {
            const face = document.createElement('div');
            face.className = 'cube-face';
            face.style.setProperty('--face-index', i);
            cube.appendChild(face);
        }

        return cube;
    }

    /**
     * Create octahedron element
     */
    createOctahedron() {
        const octahedron = document.createElement('div');
        octahedron.className = 'platonic-solid octahedron';
        
        for (let i = 0; i < 8; i++) {
            const face = document.createElement('div');
            face.className = 'octahedron-face';
            face.style.setProperty('--face-index', i);
            octahedron.appendChild(face);
        }

        return octahedron;
    }

    /**
     * Create icosahedron element
     */
    createIcosahedron() {
        const icosahedron = document.createElement('div');
        icosahedron.className = 'platonic-solid icosahedron';
        
        for (let i = 0; i < 20; i++) {
            const face = document.createElement('div');
            face.className = 'icosahedron-face';
            face.style.setProperty('--face-index', i);
            icosahedron.appendChild(face);
        }

        return icosahedron;
    }

    /**
     * Create dodecahedron element
     */
    createDodecahedron() {
        const dodecahedron = document.createElement('div');
        dodecahedron.className = 'platonic-solid dodecahedron';
        
        for (let i = 0; i < 12; i++) {
            const face = document.createElement('div');
            face.className = 'dodecahedron-face';
            face.style.setProperty('--face-index', i);
            dodecahedron.appendChild(face);
        }

        return dodecahedron;
    }

    /**
     * Setup animations
     */
    setupAnimations() {
        const solids = this.element.querySelectorAll('.platonic-solid');
        
        solids.forEach((solid, index) => {
            solid.style.animation = `
                platonicRotate var(--time-flowing) var(--ease-divine) infinite ${index * 200}ms,
                platonicTransform var(--time-harmonic) var(--ease-golden) infinite ${index * 300}ms
            `;
        });
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        const elements = this.element.querySelectorAll('.platonic-solid');
        
        elements.forEach(element => {
            if (mediaQuery.matches) {
                element.style.animation = 'none';
            } else {
                this.setupAnimations();
            }
        });
    }

    /**
     * Update loader state
     */
    setState(state) {
        super.setState(state);
        
        if (state === LOADER_CONSTANTS.STATES.COMPLETE) {
            this.element.classList.add('platonic-complete');
        } else if (state === LOADER_CONSTANTS.STATES.ERROR) {
            this.element.classList.add('platonic-error');
        }
    }
}

/**
 * Sacred Torus Loader
 * Based on sacred geometry principles and divine proportions
 */
class TorusLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.TORUS
        });
    }

    /**
     * Create loader structure
     */
    createLoader() {
        super.createLoader();
        
        const torusContainer = document.createElement('div');
        torusContainer.className = 'sacred-torus-container';

        // Create outer ring
        const outerRing = document.createElement('div');
        outerRing.className = 'torus-outer-ring';

        // Create inner rings
        for (let i = 0; i < 7; i++) {
            const ring = document.createElement('div');
            ring.className = 'torus-ring';
            ring.style.setProperty('--ring-index', i);
            ring.style.setProperty('--ring-angle', `${i * SACRED_CONSTANTS.MATH.ANGLES.GOLDEN}deg`);
            outerRing.appendChild(ring);
        }

        // Create center point
        const centerPoint = document.createElement('div');
        centerPoint.className = 'torus-center';
        
        torusContainer.appendChild(outerRing);
        torusContainer.appendChild(centerPoint);
        this.element.appendChild(torusContainer);
    }

    /**
     * Setup animations
     */
    setupAnimations() {
        const rings = this.element.querySelectorAll('.torus-ring');
        const outerRing = this.element.querySelector('.torus-outer-ring');
        const center = this.element.querySelector('.torus-center');

        // Animate rings
        rings.forEach((ring, index) => {
            ring.style.animation = `
                torusRotate var(--time-flowing) var(--ease-divine) infinite ${index * 100}ms,
                torusPulse var(--time-harmonic) var(--ease-golden) infinite ${index * 200}ms
            `;
        });

        // Animate outer ring
        outerRing.style.animation = `
            torusExpand var(--time-flowing) var(--ease-spiral) infinite
        `;

        // Animate center
        center.style.animation = `
            sacredPulse var(--time-harmonic) var(--ease-divine) infinite
        `;
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        const elements = this.element.querySelectorAll('.torus-ring, .torus-outer-ring, .torus-center');
        
        elements.forEach(element => {
            if (mediaQuery.matches) {
                element.style.animation = 'none';
            } else {
                this.setupAnimations();
            }
        });
    }

    /**
     * Update loader state
     */
    setState(state) {
        super.setState(state);
        
        if (state === LOADER_CONSTANTS.STATES.COMPLETE) {
            this.element.classList.add('torus-complete');
        } else if (state === LOADER_CONSTANTS.STATES.ERROR) {
            this.element.classList.add('torus-error');
        }
    }
}

/**
 * Sacred Merkaba Star Loader
 * Based on sacred geometry principles and divine proportions
 */
class MerkabaStarLoader extends SacredBaseLoader {
    constructor(options) {
        super({
            ...options,
            type: LOADER_CONSTANTS.TYPES.MERKABA_STAR
        });
    }

    /**
     * Create loader structure
     */
    createLoader() {
        super.createLoader();
        
        const merkabaContainer = document.createElement('div');
        merkabaContainer.className = 'sacred-merkaba-star-container';

        // Create upper tetrahedron
        const upperTetrahedron = this.createTetrahedron('upper');
        merkabaContainer.appendChild(upperTetrahedron);

        // Create lower tetrahedron
        const lowerTetrahedron = this.createTetrahedron('lower');
        merkabaContainer.appendChild(lowerTetrahedron);

        // Create center sphere
        const centerSphere = document.createElement('div');
        centerSphere.className = 'merkaba-star-center';
        merkabaContainer.appendChild(centerSphere);

        // Create energy field
        const energyField = document.createElement('div');
        energyField.className = 'merkaba-star-field';
        merkabaContainer.appendChild(energyField);

        this.element.appendChild(merkabaContainer);
    }

    /**
     * Create tetrahedron element
     */
    createTetrahedron(position) {
        const tetrahedron = document.createElement('div');
        tetrahedron.className = `merkaba-star-tetrahedron ${position}`;

        // Create faces
        for (let i = 0; i < 4; i++) {
            const face = document.createElement('div');
            face.className = 'merkaba-star-face';
            face.style.setProperty('--face-index', i);
            tetrahedron.appendChild(face);
        }

        // Create edges
        for (let i = 0; i < 6; i++) {
            const edge = document.createElement('div');
            edge.className = 'merkaba-star-edge';
            edge.style.setProperty('--edge-index', i);
            tetrahedron.appendChild(edge);
        }

        return tetrahedron;
    }

    /**
     * Setup animations
     */
    setupAnimations() {
        const tetrahedrons = this.element.querySelectorAll('.merkaba-star-tetrahedron');
        const center = this.element.querySelector('.merkaba-star-center');
        const field = this.element.querySelector('.merkaba-star-field');

        // Animate tetrahedrons
        tetrahedrons.forEach((tetra, index) => {
            tetra.style.animation = `
                merkabaStarRotate var(--time-flowing) var(--ease-divine) infinite ${index * 200}ms,
                merkabaStarPulse var(--time-harmonic) var(--ease-golden) infinite ${index * 300}ms
            `;
        });

        // Animate center
        center.style.animation = `
            sacredPulse var(--time-harmonic) var(--ease-spiral) infinite
        `;

        // Animate energy field
        field.style.animation = `
            merkabaStarField var(--time-flowing) var(--ease-divine) infinite
        `;
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        const elements = this.element.querySelectorAll(
            '.merkaba-star-tetrahedron, .merkaba-star-center, .merkaba-star-field'
        );
        
        elements.forEach(element => {
            if (mediaQuery.matches) {
                element.style.animation = 'none';
            } else {
                this.setupAnimations();
            }
        });
    }

    /**
     * Update loader state
     */
    setState(state) {
        super.setState(state);
        
        if (state === LOADER_CONSTANTS.STATES.COMPLETE) {
            this.element.classList.add('merkaba-star-complete');
        } else if (state === LOADER_CONSTANTS.STATES.ERROR) {
            this.element.classList.add('merkaba-star-error');
        }
    }
}

/**
 * Sacred Progress Tracking System
 * Based on divine proportions and sacred geometry
 */
class SacredProgressTracker {
    constructor(loader) {
        this.loader = loader;
        this.progress = 0;
        this.total = 100;
        this.initialize();
    }

    /**
     * Initialize progress tracking
     */
    initialize() {
        const progressContainer = document.createElement('div');
        progressContainer.className = 'sacred-progress-container';

        // Create progress circle
        const progressCircle = document.createElement('div');
        progressCircle.className = 'sacred-progress-circle';

        // Create progress path
        const progressPath = document.createElement('svg');
        progressPath.className = 'sacred-progress-path';
        progressPath.setAttribute('viewBox', '0 0 100 100');

        const circle = document.createElement('circle');
        circle.setAttribute('cx', '50');
        circle.setAttribute('cy', '50');
        circle.setAttribute('r', '45');
        progressPath.appendChild(circle);

        // Create progress text
        const progressText = document.createElement('div');
        progressText.className = 'sacred-progress-text';

        progressContainer.appendChild(progressPath);
        progressContainer.appendChild(progressCircle);
        progressContainer.appendChild(progressText);
        this.loader.element.appendChild(progressContainer);

        this.elements = {
            container: progressContainer,
            circle: progressCircle,
            path: progressPath,
            text: progressText
        };
    }

    /**
     * Update progress value
     */
    update(value) {
        this.progress = Math.min(100, Math.max(0, value));
        
        // Calculate circle circumference
        const radius = 45;
        const circumference = 2 * Math.PI * radius;
        
        // Calculate stroke dash offset using golden ratio
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;
        const offset = circumference - (this.progress / 100) * circumference * phi;

        // Update progress path
        const circle = this.elements.path.querySelector('circle');
        circle.style.strokeDasharray = `${circumference} ${circumference}`;
        circle.style.strokeDashoffset = offset;

        // Update progress text
        this.elements.text.textContent = `${Math.round(this.progress)}%`;

        // Update loader state based on progress
        if (this.progress === 100) {
            this.loader.setState(LOADER_CONSTANTS.STATES.COMPLETE);
        } else if (this.progress > 0) {
            this.loader.setState(LOADER_CONSTANTS.STATES.ACTIVE);
        }
    }

    /**
     * Set total progress steps
     */
    setTotal(total) {
        this.total = total;
    }

    /**
     * Increment progress by step
     */
    increment(step = 1) {
        const increment = (step / this.total) * 100;
        this.update(this.progress + increment);
    }

    /**
     * Reset progress
     */
    reset() {
        this.progress = 0;
        this.update(0);
        this.loader.setState(LOADER_CONSTANTS.STATES.LOADING);
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        const elements = this.elements.container.querySelectorAll('.sacred-progress-circle, .sacred-progress-path');
        
        elements.forEach(element => {
            if (mediaQuery.matches) {
                element.style.transition = 'none';
            } else {
                element.style.transition = 'all var(--time-harmonic) var(--ease-divine)';
            }
        });
    }
}

/**
 * Sacred Event System
 * Based on divine event patterns and sacred timing
 */
class SacredEventSystem {
    constructor(loader) {
        this.loader = loader;
        this.handlers = new Map();
        this.initialize();
    }

    /**
     * Initialize event system
     */
    initialize() {
        // Setup core events
        this.setupCoreEvents();
        this.setupStateEvents();
        this.setupProgressEvents();
    }

    /**
     * Setup core loader events
     */
    setupCoreEvents() {
        const events = {
            start: [],
            complete: [],
            error: [],
            reset: [],
            update: []
        };

        events.forEach((event) => {
            this.handlers.set(event, new Set());
        });

        this.loader.element.addEventListener('transitionend', (event) => {
            if (event.target === this.loader.element) {
                this.emit('transitionComplete', event);
            }
        });
    }

    /**
     * Setup state transition events
     */
    setupStateEvents() {
        const states = Object.values(LOADER_CONSTANTS.STATES);
        
        states.forEach(state => {
            this.handlers.set(`state:${state}`, new Set());
            this.handlers.set(`state:${state}:enter`, new Set());
            this.handlers.set(`state:${state}:exit`, new Set());
        });
    }

    /**
     * Setup progress tracking events
     */
    setupProgressEvents() {
        const progressEvents = [
            'progressStart',
            'progressUpdate',
            'progressComplete',
            'progressPause',
            'progressResume'
        ];

        progressEvents.forEach(event => {
            this.handlers.set(event, new Set());
        });
    }

    /**
     * Add event listener
     */
    on(event, handler) {
        if (!this.handlers.has(event)) {
            this.handlers.set(event, new Set());
        }
        this.handlers.get(event).add(handler);
    }

    /**
     * Remove event listener
     */
    off(event, handler) {
        if (this.handlers.has(event)) {
            this.handlers.get(event).delete(handler);
        }
    }

    /**
     * Emit event
     */
    emit(event, data) {
        if (this.handlers.has(event)) {
            this.handlers.get(event).forEach(handler => {
                setTimeout(() => {
                    handler({
                        type: event,
                        timestamp: Date.now(),
                        loader: this.loader,
                        data
                    });
                }, 0);
            });
        }
    }

    /**
     * Handle state changes
     */
    handleStateChange(prevState, newState) {
        // Emit exit event for previous state
        if (prevState) {
            this.emit(`state:${prevState}:exit`, { prevState, newState });
        }

        // Emit enter event for new state
        this.emit(`state:${newState}:enter`, { prevState, newState });
        
        // Emit general state change event
        this.emit(`state:${newState}`, { prevState, newState });
    }

    /**
     * Handle progress updates
     */
    handleProgress(progress) {
        this.emit('progressUpdate', {
            progress,
            timestamp: Date.now()
        });

        if (progress === 100) {
            this.emit('progressComplete');
        }
    }

    /**
     * Cleanup event system
     */
    destroy() {
        this.handlers.clear();
        this.loader.element.removeEventListener('transitionend', this.handleTransitionEnd);
    }
}

/**
 * Sacred Animation Controller
 * Based on sacred geometry principles and divine timing
 */
class SacredAnimationController {
    constructor(loader) {
        this.loader = loader;
        this.animations = new Map();
        this.currentAnimation = null;
        this.initialize();
    }

    /**
     * Initialize animation controller
     */
    initialize() {
        this.setupBaseAnimations();
        this.setupEventListeners();
    }

    /**
     * Setup base animations
     */
    setupBaseAnimations() {
        this.animations.set('sacredSpiral', {
            duration: 'var(--time-flowing)',
            easing: 'var(--ease-spiral)',
            keyframes: [
                { transform: 'scale(0) rotate(0deg)', opacity: 0 },
                { transform: 'scale(1) rotate(var(--rotate-phi))', opacity: 1 }
            ]
        });

        this.animations.set('flowerOfLife', {
            duration: 'var(--time-harmonic)',
            easing: 'var(--ease-golden)',
            keyframes: [
                { transform: 'scale(0)', opacity: 0 },
                { transform: 'scale(0.382)', opacity: 0.4 },
                { transform: 'scale(0.618)', opacity: 0.6 },
                { transform: 'scale(1)', opacity: 1 }
            ]
        });

        this.animations.set('divineWave', {
            duration: 'var(--time-flowing)',
            easing: 'var(--ease-divine)',
            keyframes: [
                { transform: 'translateY(0)' },
                { transform: 'translateY(calc(var(--scale-phi-inverse) * -1rem))' },
                { transform: 'translateY(calc(var(--scale-phi-inverse) * 1rem))' },
                { transform: 'translateY(0)' }
            ]
        });
    }

    /**
     * Play animation
     */
    play(animationName, options = {}) {
        const animation = this.animations.get(animationName);
        if (!animation) return;

        const element = options.element || this.loader.element;
        
        this.currentAnimation = element.animate(
            animation.keyframes,
            {
                duration: this.getComputedDuration(animation.duration),
                easing: animation.easing,
                iterations: options.iterations || 1,
                direction: options.direction || 'normal',
                fill: options.fill || 'forwards'
            }
        );

        return this.currentAnimation.finished;
    }

    /**
     * Get computed duration from CSS variable
     */
    getComputedDuration(duration) {
        const computed = getComputedStyle(this.loader.element)
            .getPropertyValue(duration.replace('var(', '').replace(')', ''));
        return parseFloat(computed) * 1000;
    }

    /**
     * Pause current animation
     */
    pause() {
        if (this.currentAnimation) {
            this.currentAnimation.pause();
        }
    }

    /**
     * Resume current animation
     */
    resume() {
        if (this.currentAnimation) {
            this.currentAnimation.play();
        }
    }

    /**
     * Stop current animation
     */
    stop() {
        if (this.currentAnimation) {
            this.currentAnimation.cancel();
        }
    }

    /**
     * Add custom animation
     */
    addAnimation(name, config) {
        this.animations.set(name, config);
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Handle reduced motion preference
        const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
        mediaQuery.addEventListener('change', () => this.handleReducedMotion(mediaQuery));
        this.handleReducedMotion(mediaQuery);
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        if (mediaQuery.matches && this.currentAnimation) {
            this.currentAnimation.updatePlaybackRate(0.1);
        }
    }
}

/**
 * Sacred Overlay Management
 * Based on sacred geometry principles and divine transitions
 */
class SacredOverlayManager {
    constructor(loader) {
        this.loader = loader;
        this.overlay = null;
        this.initialize();
    }

    /**
     * Initialize overlay system
     */
    initialize() {
        this.createOverlay();
        this.setupEventListeners();
    }

    /**
     * Create sacred overlay
     */
    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'sacred-loader-overlay';
        
        Object.assign(this.overlay.style, {
            position: 'fixed',
            inset: '0',
            background: 'var(--color-cosmic-background)',
            backdropFilter: 'blur(var(--transition-overlay-blur))',
            opacity: '0',
            visibility: 'hidden',
            transition: `
                opacity var(--time-natural) var(--ease-golden),
                visibility var(--time-natural) var(--ease-golden)
            `,
            zIndex: 'calc(var(--transition-z-index) - 1)'
        });

        // Add sacred geometry pattern
        this.addSacredPattern();
        
        document.body.appendChild(this.overlay);
    }

    /**
     * Add sacred geometry pattern to overlay
     */
    addSacredPattern() {
        const pattern = document.createElement('div');
        pattern.className = 'sacred-overlay-pattern';
        
        Object.assign(pattern.style, {
            position: 'absolute',
            inset: '0',
            background: `
                radial-gradient(
                    circle at var(--phi-inverse) var(--phi-inverse),
                    var(--color-ethereal-blue) 0%,
                    transparent 60%
                )
            `,
            opacity: '0.1',
            mixBlendMode: 'overlay'
        });

        this.overlay.appendChild(pattern);
    }

    /**
     * Show overlay with animation
     */
    show() {
        this.overlay.style.visibility = 'visible';
        requestAnimationFrame(() => {
            this.overlay.style.opacity = 'var(--transition-overlay-opacity)';
        });
    }

    /**
     * Hide overlay with animation
     */
    hide() {
        this.overlay.style.opacity = '0';
        this.overlay.addEventListener('transitionend', () => {
            if (this.overlay.style.opacity === '0') {
                this.overlay.style.visibility = 'hidden';
            }
        }, { once: true });
    }

    /**
     * Update overlay state based on loader state
     */
    updateState(state) {
        switch (state) {
            case LOADER_CONSTANTS.STATES.LOADING:
            case LOADER_CONSTANTS.STATES.ACTIVE:
                this.show();
                break;
            case LOADER_CONSTANTS.STATES.COMPLETE:
            case LOADER_CONSTANTS.STATES.ERROR:
                this.hide();
                break;
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Handle reduced motion preference
        const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
        mediaQuery.addEventListener('change', () => this.handleReducedMotion(mediaQuery));
        this.handleReducedMotion(mediaQuery);
    }

    /**
     * Handle reduced motion preference
     */
    handleReducedMotion(mediaQuery) {
        if (mediaQuery.matches) {
            this.overlay.style.transition = 'none';
        } else {
            this.overlay.style.transition = `
                opacity var(--time-natural) var(--ease-golden),
                visibility var(--time-natural) var(--ease-golden)
            `;
        }
    }

    /**
     * Clean up overlay
     */
    destroy() {
        if (this.overlay && this.overlay.parentNode) {
            this.overlay.parentNode.removeChild(this.overlay);
        }
        this.overlay = null;
    }
}

    // 2. Loading State Management
    // 3. Transition System
    // 4. Individual Loader Types
    // 5. Progress Tracking
    // 6. Event System
    // 7. Animation Controller
    // 8. Overlay Management

    return {
        create: function(type, options) {
            // Factory method to create specific loader types
        },
        
        show: function(type, container, options) {
            // Show loader in container
        },
        
        hide: function(container) {
            // Hide loader from container
        },
        
        update: function(container, progress) {
            // Update loader progress
        },

        CONSTANTS: LOADER_CONSTANTS
    };
})();
