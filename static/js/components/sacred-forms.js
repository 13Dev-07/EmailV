/**
 * Sacred Forms System
 * Based on sacred geometry and divine proportions
 */
const SacredForms = (function() {
    'use strict';

    // Core Constants
    const FORM_CONSTANTS = {
        STATES: {
            PRISTINE: 'pristine',
            VALID: 'valid',
            INVALID: 'invalid',
            SUBMITTING: 'submitting',
            SUCCESS: 'success',
            ERROR: 'error'
        },
        
        PATTERNS: {
            EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            PHONE: /^\+?[\d\s-]{10,}$/,
            URL: /^https?:\/\/[\w\-]+(\.[\w\-]+)+[/#?]?.*$/
        },

        TRANSITIONS: {
            DURATION: 'var(--transition-golden-normal)',
            EASING: 'var(--ease-golden)'
        }
    };

    /**
     * Sacred Form Class
     */
    class SacredForm {
        constructor(element, options = {}) {
            this.element = element;
            this.options = this.mergeOptions(options);
            this.state = FORM_CONSTANTS.STATES.PRISTINE;
            this.fields = new Map();
            this.initialize();
        }

        /**
         * Merge default options with user options
         */
        mergeOptions(options) {
            return {
                validateOnInput: options.validateOnInput !== false,
                validateOnBlur: options.validateOnBlur !== false,
                animateValidation: options.animateValidation !== false,
                showIcons: options.showIcons !== false,
                preventSubmit: options.preventSubmit !== false,
                successMessage: options.successMessage || 'Form submitted successfully',
                errorMessage: options.errorMessage || 'Please correct the errors',
                onSubmit: options.onSubmit || null,
                onValidate: options.onValidate || null,
                onError: options.onError || null
            };
        }

        /**
         * Initialize form
         */
        initialize() {
            this.setupFormAttributes();
            this.initializeFields();
            this.setupEventListeners();
            if (this.options.animateValidation) {
                this.setupAnimations();
            }
        }

        /**
         * Setup form attributes
         */
        setupFormAttributes() {
            this.element.classList.add('sacred-form');
            this.element.setAttribute('novalidate', '');
            this.element.dataset.state = this.state;
        }
    }

    return {
        create: function(element, options) {
            return new SacredForm(element, options);
        },
        CONSTANTS: FORM_CONSTANTS
    };
})();
