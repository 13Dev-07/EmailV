/**
 * sacred-charts.js
 * Divine visualization system based on sacred geometry principles
 * Version: 1.0.0
 */

const SacredCharts = (function() {
    'use strict';

    /**
     * Chart Constants
     * Aligned with CSS variables
     */
    const CHART_CONSTANTS = {
        // Chart Dimensions (from --chart-* CSS vars)
        DIMENSIONS: {
            MIN_HEIGHT: 'var(--chart-min-height)',
            MAX_HEIGHT: 'var(--chart-max-height)',
            ASPECT_RATIO: 'var(--chart-aspect-ratio)',
            PADDING: {
                SM: 'var(--chart-padding-sm)',
                MD: 'var(--chart-padding-md)',
                LG: 'var(--chart-padding-lg)'
            }
        },

        // Chart Types
        TYPES: {
            LINE: 'sacred-chart-line',
            BAR: 'sacred-chart-bar',
            CIRCLE: 'sacred-chart-circle',
            RADAR: 'sacred-chart-radar',
            SCATTER: 'sacred-chart-scatter',
            AREA: 'sacred-chart-area',
            CANDLESTICK: 'sacred-chart-candlestick'
        },

        // Animation Timings
        ANIMATION: {
            DURATION: 'var(--chart-animation-duration)',
            EASING: 'var(--chart-animation-easing)'
        }
    };

    /**
     * Component Structure:
     * 1. Base Chart Class
     * 2. Chart Types
     * 3. Chart Grid System
     * 4. Chart Axes
     * 5. Chart Legend
     * 6. Chart Tooltip
     * 7. Chart Animations
     * 8. Chart Interactive Features
     */

/**
 * sacred-charts.js
 * Divine visualization system based on sacred geometry principles
 * Version: 1.0.0
 */

const SacredCharts = (function() {
    'use strict';

    /**
     * Chart Constants
     * Aligned with CSS variables
     */
    const CHART_CONSTANTS = {
        // Chart Dimensions (from --chart-* CSS vars)
        DIMENSIONS: {
            MIN_HEIGHT: 'var(--chart-min-height)',
            MAX_HEIGHT: 'var(--chart-max-height)',
            ASPECT_RATIO: 'var(--chart-aspect-ratio)',
            PADDING: {
                SM: 'var(--chart-padding-sm)',
                MD: 'var(--chart-padding-md)',
                LG: 'var(--chart-padding-lg)'
            }
        },

        // Chart Types
        TYPES: {
            LINE: 'sacred-chart-line',
            BAR: 'sacred-chart-bar',
            CIRCLE: 'sacred-chart-circle',
            RADAR: 'sacred-chart-radar',
            SCATTER: 'sacred-chart-scatter',
            AREA: 'sacred-chart-area',
            CANDLESTICK: 'sacred-chart-candlestick'
        },

        // Animation Timings
        ANIMATION: {
            DURATION: 'var(--chart-animation-duration)',
            EASING: 'var(--chart-animation-easing)'
        }
    };

/**
 * Base Chart Class
 * Foundation for all sacred chart types
 */
class SacredBaseChart {
    constructor(container, data, options = {}) {
        this.container = typeof container === 'string' ? 
            document.querySelector(container) : container;
        this.data = data;
        this.options = this.mergeOptions(options);
        
        // Core properties
        this.svg = null;
        this.dimensions = null;
        this.scales = {};
        this.axes = {};
        this.grid = null;
        this.tooltip = null;

        // Initialize chart
        this.initialize();
    }

    /**
     * Merge default options with user options
     */
    mergeOptions(options) {
        return {
            // Dimensions
            width: options.width || '100%',
            height: options.height || 'var(--chart-min-height)',
            padding: options.padding || 'var(--chart-padding-md)',
            aspectRatio: options.aspectRatio || 'var(--chart-aspect-ratio)',

            // Styling
            backgroundColor: options.backgroundColor || 'var(--surface-primary)',
            borderRadius: options.borderRadius || 'var(--border-radius-lg)',
            
            // Grid options
            grid: {
                show: options.grid?.show ?? true,
                color: options.grid?.color || 'var(--grid-line-color)',
                width: options.grid?.width || 'var(--grid-line-width)',
                style: options.grid?.style || 'var(--grid-line-style)'
            },

            // Animation
            animated: options.animated ?? true,
            animationDuration: options.animationDuration || 'var(--chart-animation-duration)',
            animationEasing: options.animationEasing || 'var(--chart-animation-easing)',

            // Interaction
            interactive: options.interactive ?? true,
            tooltip: options.tooltip ?? true,

            // Colors
            colors: options.colors || [
                'var(--chart-color-1)',
                'var(--chart-color-2)',
                'var(--chart-color-3)',
                'var(--chart-color-4)',
                'var(--chart-color-5)'
            ]
        };
    }

    /**
     * Initialize chart
     */
    initialize() {
        this.setupContainer();
        this.createSVG();
        this.setupDimensions();
        if (this.options.grid.show) {
            this.createGrid();
        }
        if (this.options.tooltip) {
            this.createTooltip();
        }
    }

    /**
     * Setup container with sacred proportions
     */
    setupContainer() {
        this.container.classList.add('sacred-chart');
        Object.assign(this.container.style, {
            width: this.options.width,
            height: this.options.height,
            padding: this.options.padding,
            backgroundColor: this.options.backgroundColor,
            borderRadius: this.options.borderRadius,
            aspectRatio: this.options.aspectRatio
        });
    }

    /**
     * Create SVG element
     */
    createSVG() {
        this.svg = d3.select(this.container)
            .append('svg')
            .attr('class', 'sacred-chart-svg')
            .attr('width', '100%')
            .attr('height', '100%')
            .attr('overflow', 'visible');

        // Add sacred geometry pattern background
        this.createSacredPattern();
    }

    /**
     * Create sacred geometry pattern
     */
    createSacredPattern() {
        const defs = this.svg.append('defs');
        
        // Create golden spiral pattern
        const pattern = defs.append('pattern')
            .attr('id', 'sacredPattern')
            .attr('patternUnits', 'userSpaceOnUse')
            .attr('width', 'var(--phi-space-6)')
            .attr('height', 'var(--phi-space-6)');

        // Add sacred geometry elements
        this.drawSacredPattern(pattern);
    }

    /**
     * Draw sacred pattern (to be implemented by specific chart types)
     */
    drawSacredPattern(pattern) {
        // Implementation varies by chart type
    }

    /**
     * Setup chart dimensions
     */
    setupDimensions() {
        const rect = this.container.getBoundingClientRect();
        
        this.dimensions = {
            width: rect.width,
            height: rect.height,
            padding: parseFloat(getComputedStyle(this.container).padding),
            innerWidth: 0,
            innerHeight: 0,
            center: { x: 0, y: 0 }
        };

        // Calculate inner dimensions
        this.dimensions.innerWidth = this.dimensions.width - (this.dimensions.padding * 2);
        this.dimensions.innerHeight = this.dimensions.height - (this.dimensions.padding * 2);
        this.dimensions.center.x = this.dimensions.innerWidth / 2;
        this.dimensions.center.y = this.dimensions.innerHeight / 2;
    }

    /**
     * Create grid system
     */
    createGrid() {
        this.grid = this.svg.append('g')
            .attr('class', 'sacred-chart-grid')
            .attr('transform', `translate(${this.dimensions.padding}, ${this.dimensions.padding})`);

        // Add Fibonacci grid lines
        this.addFibonacciGrid();
    }

    /**
     * Add Fibonacci grid lines
     */
    addFibonacciGrid() {
        const { innerWidth, innerHeight } = this.dimensions;
        const fibLines = [0, 0.236, 0.382, 0.618, 1];

        // Vertical lines
        fibLines.forEach(ratio => {
            this.grid.append('line')
                .attr('x1', innerWidth * ratio)
                .attr('x2', innerWidth * ratio)
                .attr('y1', 0)
                .attr('y2', innerHeight)
                .attr('stroke', this.options.grid.color)
                .attr('stroke-width', this.options.grid.width)
                .attr('stroke-dasharray', this.options.grid.style === 'dashed' ? '4,4' : null);
        });

        // Horizontal lines
        fibLines.forEach(ratio => {
            this.grid.append('line')
                .attr('x1', 0)
                .attr('x2', innerWidth)
                .attr('y1', innerHeight * ratio)
                .attr('y2', innerHeight * ratio)
                .attr('stroke', this.options.grid.color)
                .attr('stroke-width', this.options.grid.width)
                .attr('stroke-dasharray', this.options.grid.style === 'dashed' ? '4,4' : null);
        });
    }

    /**
     * Create tooltip
     */
    createTooltip() {
        this.tooltip = d3.select(this.container)
            .append('div')
            .attr('class', 'sacred-chart-tooltip')
            .style('opacity', 0);
    }
}
// Adding to sacred-charts.js...

/**
 * Chart Animation System
 */
const chartAnimations = {
    /**
     * Sacred entrance animation
     */
    entrance(selection, options = {}) {
        const duration = options.duration || 'var(--transition-golden-normal)';
        const delay = options.delay || 0;

        selection
            .style('opacity', 0)
            .style('transform', 'scale(var(--scale-phi-inverse))')
            .transition()
            .duration(duration)
            .delay(delay)
            .ease(d3.easeCubicInOut)
            .style('opacity', 1)
            .style('transform', 'scale(1)');
    },

    /**
     * Sacred flow animation
     */
    flow(selection, options = {}) {
        const duration = options.duration || 'var(--transition-golden-slow)';
        
        selection
            .style('opacity', 0)
            .style('transform', 'translateY(var(--transition-distance-md))')
            .transition()
            .duration(duration)
            .ease(d3.easeCubicInOut)
            .style('opacity', 1)
            .style('transform', 'translateY(0)');
    },

    /**
     * Sacred pulse animation
     */
    pulse(selection) {
        selection
            .transition()
            .duration('var(--transition-golden-normal)')
            .ease(d3.easeCubicInOut)
            .style('transform', 'scale(var(--scale-phi))')
            .transition()
            .duration('var(--transition-golden-normal)')
            .ease(d3.easeCubicInOut)
            .style('transform', 'scale(1)')
            .on('end', () => this.pulse(selection));
    }
};

/**
 * Chart Interactive Features
 */
const chartInteractions = {
    /**
     * Setup hover interactions
     */
    setupHover(element, options = {}) {
        element
            .on('mouseenter', function(event, d) {
                d3.select(this)
                    .transition()
                    .duration('var(--transition-duration-quick)')
                    .ease(d3.easeCubicOut)
                    .style('transform', 'scale(var(--scale-phi))')
                    .style('filter', 'brightness(1.2)');

                if (options.onHover) {
                    options.onHover(event, d);
                }
            })
            .on('mouseleave', function(event, d) {
                d3.select(this)
                    .transition()
                    .duration('var(--transition-duration-quick)')
                    .ease(d3.easeCubicOut)
                    .style('transform', 'scale(1)')
                    .style('filter', 'none');

                if (options.onLeave) {
                    options.onLeave(event, d);
                }
            });
    },

    /**
     * Setup click interactions
     */
    setupClick(element, options = {}) {
        element
            .style('cursor', 'pointer')
            .on('click', function(event, d) {
                d3.select(this)
                    .transition()
                    .duration('var(--transition-duration-instant)')
                    .ease(d3.easeCubicOut)
                    .style('transform', 'scale(var(--scale-phi-inverse))')
                    .transition()
                    .duration('var(--transition-duration-quick)')
                    .style('transform', 'scale(1)');

                if (options.onClick) {
                    options.onClick(event, d);
                }
            });
    },

    /**
     * Setup drag interactions
     */
    setupDrag(element, options = {}) {
        const drag = d3.drag()
            .on('start', options.onDragStart || null)
            .on('drag', options.onDrag || null)
            .on('end', options.onDragEnd || null);

        element.call(drag);
    }
};

// Add to SacredBaseChart class
Object.assign(SacredBaseChart.prototype, {
    animations: chartAnimations,
    interactions: chartInteractions,

    /**
     * Setup chart interactions
     */
    setupInteractions() {
        if (!this.options.interactive) return;

        // Setup tooltip
        if (this.options.tooltip) {
            this.tooltip = d3.select(this.container)
                .append('div')
                .attr('class', 'sacred-chart-tooltip')
                .style('opacity', 0);
        }

        // Setup zoom if enabled
        if (this.options.zoomable) {
            this.setupZoom();
        }

        // Setup pan if enabled
        if (this.options.pannable) {
            this.setupPan();
        }
    },

    /**
     * Setup zoom behavior
     */
    setupZoom() {
        const zoom = d3.zoom()
            .scaleExtent([1, Math.round(SACRED_CONSTANTS.MATH.PHI.SQUARED)])
            .on('zoom', (event) => {
                this.svg.attr('transform', event.transform);
            });

        this.svg.call(zoom);
    },

    /**
     * Setup pan behavior
     */
    setupPan() {
        const pan = d3.drag()
            .on('drag', (event) => {
                const transform = d3.zoomTransform(this.svg.node());
                this.svg.attr('transform', `translate(${event.x}, ${event.y}) scale(${transform.k})`);
            });

        this.svg.call(pan);
    }
});
/**
 * Sacred Line Chart Implementation
 * Based on sacred geometry and golden ratio principles
 */
class SacredLineChart extends SacredBaseChart {
    constructor(container, data, options) {
        super(container, {
            ...options,
            type: 'sacred-chart-line'
        });
        
        this.lineGroup = null;
        this.pointsGroup = null;
        this.areaGroup = null;
        this.setupScales();
        this.draw();
    }

    /**
     * Setup scales specific to line chart
     */
    setupScales() {
        const { innerWidth, innerHeight } = this.dimensions;

        this.scales = {
            x: d3.scaleLinear()
                .domain(d3.extent(this.data, d => d.x))
                .range([0, innerWidth]),

            y: d3.scaleLinear()
                .domain([0, d3.max(this.data, d => d.y) * SACRED_CONSTANTS.MATH.PHI])
                .range([innerHeight, 0])
        };
    }

    /**
     * Draw chart implementation
     */
    draw() {
        // Create groups
        this.lineGroup = this.svg.append('g')
            .attr('class', 'sacred-line-group');
        
        this.areaGroup = this.svg.append('g')
            .attr('class', 'sacred-area-group');
        
        this.pointsGroup = this.svg.append('g')
            .attr('class', 'sacred-points-group');

        // Draw sacred elements
        this.drawArea();
        this.drawLine();
        this.drawPoints();

        // Add animations if enabled
        if (this.options.animated) {
            this.animateChart();
        }

        // Add interactions if enabled
        if (this.options.interactive) {
            this.setupInteractions();
        }
    }

    /**
     * Draw line path
     */
    drawLine() {
        const linePath = d3.line()
            .x(d => this.scales.x(d.x))
            .y(d => this.scales.y(d.y))
            .curve(d3.curveCardinal.tension(SACRED_CONSTANTS.MATH.PHI_INVERSE));

        this.lineGroup.append('path')
            .attr('class', 'sacred-line')
            .attr('d', linePath(this.data))
            .style('fill', 'none')
            .style('stroke', 'var(--chart-line-color)')
            .style('stroke-width', 'var(--chart-line-width)');
    }

    /**
     * Draw area beneath line
     */
    drawArea() {
        const areaPath = d3.area()
            .x(d => this.scales.x(d.x))
            .y0(this.dimensions.innerHeight)
            .y1(d => this.scales.y(d.y))
            .curve(d3.curveCardinal.tension(SACRED_CONSTANTS.MATH.PHI_INVERSE));

        this.areaGroup.append('path')
            .attr('class', 'sacred-area')
            .attr('d', areaPath(this.data))
            .style('fill', 'var(--chart-area-fill)')
            .style('opacity', 'var(--chart-area-opacity)');
    }

    /**
     * Draw data points
     */
    drawPoints() {
        this.pointsGroup.selectAll('.sacred-point')
            .data(this.data)
            .enter()
            .append('circle')
            .attr('class', 'sacred-point')
            .attr('cx', d => this.scales.x(d.x))
            .attr('cy', d => this.scales.y(d.y))
            .attr('r', 'var(--chart-point-size)')
            .style('fill', 'var(--chart-point-fill)')
            .style('stroke', 'var(--chart-point-stroke)')
            .style('stroke-width', 'var(--chart-point-stroke-width)');
    }

    /**
     * Animate chart elements
     */
    animateChart() {
        // Animate line
        const linePath = this.lineGroup.select('.sacred-line');
        const length = linePath.node().getTotalLength();

        linePath
            .attr('stroke-dasharray', `${length} ${length}`)
            .attr('stroke-dashoffset', length)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .ease(d3.easeExpInOut)
            .attr('stroke-dashoffset', 0);

        // Animate area
        this.areaGroup.select('.sacred-area')
            .style('opacity', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .ease(d3.easeExpInOut)
            .style('opacity', 'var(--chart-area-opacity)');

        // Animate points
        this.pointsGroup.selectAll('.sacred-point')
            .attr('r', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .delay((d, i) => i * SACRED_CONSTANTS.TIMING.DELAY)
            .ease(d3.easeExpInOut)
            .attr('r', 'var(--chart-point-size)');
    }

    /**
     * Setup chart interactions
     */
    setupInteractions() {
        this.pointsGroup.selectAll('.sacred-point')
            .on('mouseenter', (event, d) => {
                const point = d3.select(event.target);
                
                point.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('r', `calc(var(--chart-point-size) * ${SACRED_CONSTANTS.MATH.PHI})`)
                    .style('opacity', 1);

                this.showTooltip(event, d);
            })
            .on('mouseleave', (event) => {
                const point = d3.select(event.target);
                
                point.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('r', 'var(--chart-point-size)')
                    .style('opacity', 'var(--chart-point-opacity)');

                this.hideTooltip();
            });
    }
}
/**
 * Sacred Bar Chart Implementation
 * Based on sacred geometry and golden ratio proportions
 */
class SacredBarChart extends SacredBaseChart {
    constructor(container, data, options) {
        super(container, {
            ...options,
            type: 'sacred-chart-bar'
        });
        
        this.barGroup = null;
        this.setupScales();
        this.draw();
    }

    /**
     * Setup scales specific to bar chart
     */
    setupScales() {
        const { innerWidth, innerHeight } = this.dimensions;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        // Calculate bar width using golden ratio
        const barWidth = (innerWidth / this.data.length) / phi;

        this.scales = {
            x: d3.scaleBand()
                .domain(this.data.map(d => d.label))
                .range([0, innerWidth])
                .padding(SACRED_CONSTANTS.MATH.PHI_INVERSE),

            y: d3.scaleLinear()
                .domain([0, d3.max(this.data, d => d.value) * phi])
                .range([innerHeight, 0])
        };

        this.scales.barWidth = barWidth;
    }

    /**
     * Draw chart implementation
     */
    draw() {
        // Create bar group
        this.barGroup = this.svg.append('g')
            .attr('class', 'sacred-bar-group');

        // Draw bars
        const bars = this.barGroup.selectAll('.sacred-bar')
            .data(this.data)
            .enter()
            .append('rect')
            .attr('class', 'sacred-bar')
            .attr('x', d => this.scales.x(d.label))
            .attr('width', this.scales.x.bandwidth())
            .attr('y', this.dimensions.innerHeight)
            .attr('height', 0)
            .style('fill', (d, i) => this.options.colors[i % this.options.colors.length]);

        // Add sacred geometry decorations
        this.addSacredDecorations();

        // Add animations if enabled
        if (this.options.animated) {
            this.animateBars(bars);
        } else {
            bars.attr('y', d => this.scales.y(d.value))
                .attr('height', d => this.dimensions.innerHeight - this.scales.y(d.value));
        }

        // Add interactions if enabled
        if (this.options.interactive) {
            this.setupBarInteractions(bars);
        }
    }

    /**
     * Add sacred geometry decorations
     */
    addSacredDecorations() {
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;
        const decorationGroup = this.svg.append('g')
            .attr('class', 'sacred-decorations');

        // Add golden spiral guides
        this.data.forEach((d, i) => {
            const x = this.scales.x(d.label) + this.scales.x.bandwidth() / 2;
            const y = this.scales.y(d.value);
            
            decorationGroup.append('circle')
                .attr('cx', x)
                .attr('cy', y)
                .attr('r', this.scales.x.bandwidth() / (phi * 2))
                .attr('class', 'sacred-decoration-circle')
                .style('fill', 'none')
                .style('stroke', 'var(--chart-decoration-color)')
                .style('stroke-width', 1)
                .style('opacity', 0.2);
        });
    }

    /**
     * Animate bars
     */
    animateBars(bars) {
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;
        const duration = SACRED_CONSTANTS.TIMING.DRAW;

        bars.transition()
            .duration(duration)
            .delay((d, i) => i * (duration / (this.data.length * phi)))
            .ease(d3.easeBounceOut)
            .attr('y', d => this.scales.y(d.value))
            .attr('height', d => this.dimensions.innerHeight - this.scales.y(d.value));
    }

    /**
     * Setup bar interactions
     */
    setupBarInteractions(bars) {
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        bars.on('mouseenter', (event, d) => {
            const bar = d3.select(event.target);
            
            // Scale up bar
            bar.transition()
                .duration(SACRED_CONSTANTS.TIMING.HOVER)
                .attr('transform', `scale(1, ${phi})`)
                .style('opacity', 1);

            // Show tooltip
            this.showTooltip(event, d);
        })
        .on('mouseleave', (event) => {
            const bar = d3.select(event.target);
            
            // Reset bar
            bar.transition()
                .duration(SACRED_CONSTANTS.TIMING.HOVER)
                .attr('transform', 'scale(1, 1)')
                .style('opacity', 0.8);

            // Hide tooltip
            this.hideTooltip();
        });
    }
}
/**
 * Sacred Circle Chart Implementation
 * Based on sacred geometry and divine proportions
 */
class SacredCircleChart extends SacredBaseChart {
    constructor(container, data, options) {
        super(container, {
            ...options,
            type: 'sacred-chart-circle'
        });
        
        this.pieGroup = null;
        this.labelGroup = null;
        this.setupScales();
        this.draw();
    }

    /**
     * Setup scales specific to circle chart
     */
    setupScales() {
        const { innerWidth, innerHeight } = this.dimensions;
        const radius = Math.min(innerWidth, innerHeight) / 2;

        this.scales = {
            color: d3.scaleOrdinal()
                .domain(this.data.map(d => d.label))
                .range(this.options.colors),

            radius: d3.scaleLinear()
                .domain([0, d3.max(this.data, d => d.value)])
                .range([0, radius * SACRED_CONSTANTS.MATH.PHI_INVERSE])
        };

        // Store radius for later use
        this.radius = radius;
    }

    /**
     * Draw chart implementation
     */
    draw() {
        // Create groups
        this.pieGroup = this.svg.append('g')
            .attr('class', 'sacred-pie-group')
            .attr('transform', `translate(${this.dimensions.center.x},${this.dimensions.center.y})`);

        this.labelGroup = this.svg.append('g')
            .attr('class', 'sacred-label-group')
            .attr('transform', `translate(${this.dimensions.center.x},${this.dimensions.center.y})`);

        // Generate pie layout
        const pieGenerator = d3.pie()
            .value(d => d.value)
            .sort(null)
            .padAngle(0.02 * SACRED_CONSTANTS.MATH.PHI_INVERSE);

        // Generate arc paths
        const arcGenerator = d3.arc()
            .innerRadius(this.radius * 0.382) // Golden ratio inverse
            .outerRadius(this.radius * 0.618); // Golden ratio inverse

        // Draw segments
        const segments = this.pieGroup.selectAll('.sacred-segment')
            .data(pieGenerator(this.data))
            .enter()
            .append('path')
            .attr('class', 'sacred-segment')
            .attr('d', arcGenerator)
            .style('fill', d => this.scales.color(d.data.label))
            .style('stroke', 'var(--surface-primary)')
            .style('stroke-width', '2px');

        // Add labels
        const labelArc = d3.arc()
            .innerRadius(this.radius * 0.75)
            .outerRadius(this.radius * 0.75);

        this.labelGroup.selectAll('.sacred-label')
            .data(pieGenerator(this.data))
            .enter()
            .append('text')
            .attr('class', 'sacred-label')
            .attr('transform', d => `translate(${labelArc.centroid(d)})`)
            .attr('dy', '0.35em')
            .style('text-anchor', 'middle')
            .style('font-size', 'var(--font-size-sm)')
            .style('fill', 'var(--color-text-primary)')
            .text(d => d.data.label);

        // Add sacred geometry decorations
        this.addSacredDecorations();

        // Add animations if enabled
        if (this.options.animated) {
            this.animateChart(segments);
        }

        // Add interactions if enabled
        if (this.options.interactive) {
            this.setupInteractions(segments);
        }
    }

    /**
     * Add sacred geometry decorations
     */
    addSacredDecorations() {
        const decorationGroup = this.pieGroup.append('g')
            .attr('class', 'sacred-decorations');

        // Add golden spiral guide
        const spiralPoints = this.generateGoldenSpiral();
        const spiralLine = d3.line()
            .x(d => d.x)
            .y(d => d.y)
            .curve(d3.curveBasis);

        decorationGroup.append('path')
            .attr('class', 'sacred-decoration-spiral')
            .attr('d', spiralLine(spiralPoints))
            .style('fill', 'none')
            .style('stroke', 'var(--chart-decoration-color)')
            .style('stroke-width', '1px')
            .style('opacity', '0.1');
    }

    /**
     * Generate golden spiral points
     */
    generateGoldenSpiral() {
        const points = [];
        const steps = 100;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        for (let i = 0; i < steps; i++) {
            const angle = i * SACRED_CONSTANTS.MATH.ANGLES.GOLDEN * Math.PI / 180;
            const radius = this.radius * Math.pow(phi, -angle / (2 * Math.PI));
            points.push({
                x: radius * Math.cos(angle),
                y: radius * Math.sin(angle)
            });
        }

        return points;
    }

    /**
     * Animate chart elements
     */
    animateChart(segments) {
        // Animate segments
        segments
            .style('opacity', 0)
            .attr('transform', 'scale(0.5)')
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .delay((d, i) => i * SACRED_CONSTANTS.TIMING.DELAY)
            .ease(d3.easeExpInOut)
            .style('opacity', 1)
            .attr('transform', 'scale(1)');

        // Animate decorations
        this.pieGroup.select('.sacred-decoration-spiral')
            .style('opacity', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .ease(d3.easeExpInOut)
            .style('opacity', 0.1);
    }

    /**
     * Setup chart interactions
     */
    setupInteractions(segments) {
        segments
            .on('mouseenter', (event, d) => {
                const segment = d3.select(event.target);
                
                segment.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('transform', `scale(${SACRED_CONSTANTS.MATH.PHI.VALUE})`)
                    .style('filter', 'brightness(1.2)');

                this.showTooltip(event, d.data);
            })
            .on('mouseleave', (event) => {
                const segment = d3.select(event.target);
                
                segment.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('transform', 'scale(1)')
                    .style('filter', 'none');

                this.hideTooltip();
            });
    }
}
/**
 * Sacred Radar Chart Implementation
 * Based on sacred geometry and divine angles
 */
class SacredRadarChart extends SacredBaseChart {
    constructor(container, data, options) {
        super(container, {
            ...options,
            type: 'sacred-chart-radar'
        });
        
        this.radarGroup = null;
        this.axisGroup = null;
        this.dataGroup = null;
        this.setupScales();
        this.draw();
    }

    /**
     * Setup scales specific to radar chart
     */
    setupScales() {
        const { innerWidth, innerHeight } = this.dimensions;
        const radius = Math.min(innerWidth, innerHeight) / 2;
        const categories = this.data[0].values.map(d => d.label);
        const angleSlice = (Math.PI * 2) / categories.length;

        this.scales = {
            radial: d3.scaleLinear()
                .domain([0, d3.max(this.data, d => d3.max(d.values, v => v.value))])
                .range([0, radius * SACRED_CONSTANTS.MATH.PHI_INVERSE]),

            angular: d3.scalePoint()
                .domain(categories)
                .range([0, Math.PI * 2]),

            color: d3.scaleOrdinal()
                .domain(this.data.map(d => d.category))
                .range(this.options.colors)
        };

        this.scales.angleSlice = angleSlice;
        this.scales.radius = radius;
    }

    /**
     * Draw chart implementation
     */
    draw() {
        // Create groups
        this.radarGroup = this.svg.append('g')
            .attr('class', 'sacred-radar-group')
            .attr('transform', `translate(${this.dimensions.center.x},${this.dimensions.center.y})`);

        // Draw sacred background
        this.drawSacredBackground();
        
        // Draw axes
        this.drawAxes();
        
        // Draw data
        this.drawData();

        // Add animations if enabled
        if (this.options.animated) {
            this.animateChart();
        }

        // Add interactions if enabled
        if (this.options.interactive) {
            this.setupInteractions();
        }
    }

    /**
     * Draw sacred geometry background
     */
    drawSacredBackground() {
        const { radius } = this.scales;
        const levels = 5; // Sacred number
        
        // Draw circular levels
        for (let i = 0; i < levels; i++) {
            const levelRadius = (radius / levels) * (i + 1);
            
            this.radarGroup.append('circle')
                .attr('class', 'sacred-radar-level')
                .attr('r', levelRadius)
                .attr('fill', 'none')
                .attr('stroke', 'var(--chart-grid-color)')
                .attr('stroke-width', '0.5')
                .attr('opacity', 0.3);
        }

        // Draw sacred geometry pattern
        this.drawSacredPattern();
    }

    /**
     * Draw sacred pattern
     */
    drawSacredPattern() {
        const { radius, angleSlice } = this.scales;
        const vertices = this.data[0].values.length;
        
        // Create sacred polygon
        const points = [];
        for (let i = 0; i < vertices; i++) {
            const angle = angleSlice * i;
            points.push([
                radius * Math.cos(angle - Math.PI/2),
                radius * Math.sin(angle - Math.PI/2)
            ]);
        }

        this.radarGroup.append('polygon')
            .attr('class', 'sacred-radar-pattern')
            .attr('points', points.join(' '))
            .attr('fill', 'none')
            .attr('stroke', 'var(--chart-decoration-color)')
            .attr('stroke-width', '0.5')
            .attr('opacity', 0.2);
    }

    /**
     * Draw axes
     */
    drawAxes() {
        const { radius, angleSlice } = this.scales;
        const categories = this.data[0].values.map(d => d.label);

        this.axisGroup = this.radarGroup.append('g')
            .attr('class', 'sacred-radar-axes');

        // Draw axes lines
        categories.forEach((category, i) => {
            const angle = angleSlice * i;
            const line = this.axisGroup.append('line')
                .attr('class', 'sacred-radar-axis')
                .attr('x1', 0)
                .attr('y1', 0)
                .attr('x2', radius * Math.cos(angle - Math.PI/2))
                .attr('y2', radius * Math.sin(angle - Math.PI/2))
                .attr('stroke', 'var(--chart-grid-color)')
                .attr('stroke-width', '0.5')
                .attr('opacity', 0.5);

            // Add labels
            this.axisGroup.append('text')
                .attr('class', 'sacred-radar-label')
                .attr('x', (radius * 1.1) * Math.cos(angle - Math.PI/2))
                .attr('y', (radius * 1.1) * Math.sin(angle - Math.PI/2))
                .attr('text-anchor', 'middle')
                .attr('dominant-baseline', 'middle')
                .style('font-size', 'var(--chart-label-size)')
                .style('fill', 'var(--chart-label-color)')
                .text(category);
        });
    }

    /**
     * Draw data paths
     */
    drawData() {
        const radarLine = d3.lineRadial()
            .radius(d => this.scales.radial(d.value))
            .angle((d, i) => this.scales.angleSlice * i)
            .curve(d3.curveCardinalClosed.tension(SACRED_CONSTANTS.MATH.PHI_INVERSE));

        this.dataGroup = this.radarGroup.append('g')
            .attr('class', 'sacred-radar-data');

        // Draw data paths
        this.data.forEach((dataset, i) => {
            const path = this.dataGroup.append('path')
                .attr('class', 'sacred-radar-path')
                .attr('d', radarLine(dataset.values))
                .attr('fill', this.scales.color(dataset.category))
                .attr('fill-opacity', 0.2)
                .attr('stroke', this.scales.color(dataset.category))
                .attr('stroke-width', 2);
        });
    }

    /**
     * Animate chart
     */
    animateChart() {
        // Animate background
        this.radarGroup.selectAll('.sacred-radar-level')
            .attr('r', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .ease(d3.easeExpInOut)
            .attr('r', d => d);

        // Animate axes
        this.axisGroup.selectAll('.sacred-radar-axis')
            .attr('x2', 0)
            .attr('y2', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .ease(d3.easeExpInOut)
            .attr('x2', d => d.x2)
            .attr('y2', d => d.y2);

        // Animate data paths
        this.dataGroup.selectAll('.sacred-radar-path')
            .style('opacity', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .ease(d3.easeExpInOut)
            .style('opacity', 1);
    }

    /**
     * Setup interactions
     */
    setupInteractions() {
        this.dataGroup.selectAll('.sacred-radar-path')
            .on('mouseenter', (event, d) => {
                const path = d3.select(event.target);
                
                path.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('fill-opacity', 0.4)
                    .attr('stroke-width', 3);

                this.showTooltip(event, d);
            })
            .on('mouseleave', (event) => {
                const path = d3.select(event.target);
                
                path.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('fill-opacity', 0.2)
                    .attr('stroke-width', 2);

                this.hideTooltip();
            });
    }
}
/**
 * Sacred Area Chart Implementation
 * Based on sacred geometry and divine flow patterns
 */
class SacredAreaChart extends SacredBaseChart {
    constructor(container, data, options) {
        super(container, {
            ...options,
            type: 'sacred-chart-area'
        });
        
        this.areaGroup = null;
        this.lineGroup = null;
        this.gradientId = `sacred-gradient-${Date.now()}`;
        this.setupScales();
        this.draw();
    }

    /**
     * Setup scales specific to area chart
     */
    setupScales() {
        const { innerWidth, innerHeight } = this.dimensions;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        this.scales = {
            x: d3.scaleLinear()
                .domain(d3.extent(this.data, d => d.x))
                .range([0, innerWidth]),

            y: d3.scaleLinear()
                .domain([0, d3.max(this.data, d => d.y) * phi])
                .range([innerHeight, 0]),

            color: d3.scaleOrdinal()
                .domain(this.data.map(d => d.category))
                .range(this.options.colors)
        };
    }

    /**
     * Draw chart implementation
     */
    draw() {
        // Create gradient definition
        this.createGradient();

        // Create groups
        this.areaGroup = this.svg.append('g')
            .attr('class', 'sacred-area-group');
        
        this.lineGroup = this.svg.append('g')
            .attr('class', 'sacred-line-group');

        // Draw sacred elements
        this.drawArea();
        this.drawLine();
        this.drawPoints();

        // Add sacred decorations
        this.addSacredDecorations();

        // Add animations if enabled
        if (this.options.animated) {
            this.animateChart();
        }

        // Add interactions if enabled
        if (this.options.interactive) {
            this.setupInteractions();
        }
    }

    /**
     * Create gradient definition
     */
    createGradient() {
        const gradient = this.svg.append('defs')
            .append('linearGradient')
            .attr('id', this.gradientId)
            .attr('x1', '0%')
            .attr('y1', '0%')
            .attr('x2', '0%')
            .attr('y2', '100%');

        gradient.append('stop')
            .attr('offset', '0%')
            .attr('stop-color', this.options.colors[0])
            .attr('stop-opacity', 0.8);

        gradient.append('stop')
            .attr('offset', `${SACRED_CONSTANTS.MATH.PHI_INVERSE * 100}%`)
            .attr('stop-color', this.options.colors[0])
            .attr('stop-opacity', 0.3);

        gradient.append('stop')
            .attr('offset', '100%')
            .attr('stop-color', this.options.colors[0])
            .attr('stop-opacity', 0.1);
    }

    /**
     * Draw area path
     */
    drawArea() {
        const areaGenerator = d3.area()
            .x(d => this.scales.x(d.x))
            .y0(this.dimensions.innerHeight)
            .y1(d => this.scales.y(d.y))
            .curve(d3.curveCardinal.tension(SACRED_CONSTANTS.MATH.PHI_INVERSE));

        this.areaGroup.append('path')
            .attr('class', 'sacred-area')
            .attr('d', areaGenerator(this.data))
            .style('fill', `url(#${this.gradientId})`);
    }

    /**
     * Draw line path
     */
    drawLine() {
        const lineGenerator = d3.line()
            .x(d => this.scales.x(d.x))
            .y(d => this.scales.y(d.y))
            .curve(d3.curveCardinal.tension(SACRED_CONSTANTS.MATH.PHI_INVERSE));

        this.lineGroup.append('path')
            .attr('class', 'sacred-line')
            .attr('d', lineGenerator(this.data))
            .style('fill', 'none')
            .style('stroke', this.options.colors[0])
            .style('stroke-width', 2);
    }

    /**
     * Draw data points
     */
    drawPoints() {
        this.lineGroup.selectAll('.sacred-point')
            .data(this.data)
            .enter()
            .append('circle')
            .attr('class', 'sacred-point')
            .attr('cx', d => this.scales.x(d.x))
            .attr('cy', d => this.scales.y(d.y))
            .attr('r', 4)
            .style('fill', this.options.colors[0])
            .style('stroke', '#fff')
            .style('stroke-width', 2);
    }

    /**
     * Add sacred geometry decorations
     */
    addSacredDecorations() {
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;
        const decorationGroup = this.svg.append('g')
            .attr('class', 'sacred-decorations');

        // Add golden ratio guides
        this.data.forEach((d, i) => {
            if (i % Math.round(phi) === 0) {
                decorationGroup.append('line')
                    .attr('class', 'sacred-guide')
                    .attr('x1', this.scales.x(d.x))
                    .attr('x2', this.scales.x(d.x))
                    .attr('y1', this.dimensions.innerHeight)
                    .attr('y2', this.scales.y(d.y))
                    .style('stroke', 'var(--chart-decoration-color)')
                    .style('stroke-width', 0.5)
                    .style('stroke-dasharray', '2,2')
                    .style('opacity', 0.3);
            }
        });
    }

    /**
     * Animate chart elements
     */
    animateChart() {
        // Animate area
        const areaPath = this.areaGroup.select('.sacred-area');
        const areaLength = areaPath.node().getTotalLength();

        areaPath
            .attr('stroke-dasharray', `${areaLength} ${areaLength}`)
            .attr('stroke-dashoffset', areaLength)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .ease(d3.easeExpInOut)
            .attr('stroke-dashoffset', 0);

        // Animate line
        const linePath = this.lineGroup.select('.sacred-line');
        const lineLength = linePath.node().getTotalLength();

        linePath
            .attr('stroke-dasharray', `${lineLength} ${lineLength}`)
            .attr('stroke-dashoffset', lineLength)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .ease(d3.easeExpInOut)
            .attr('stroke-dashoffset', 0);

        // Animate points
        this.lineGroup.selectAll('.sacred-point')
            .attr('r', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .delay((d, i) => i * SACRED_CONSTANTS.TIMING.DELAY)
            .ease(d3.easeExpInOut)
            .attr('r', 4);
    }

    /**
     * Setup chart interactions
     */
    setupInteractions() {
        this.lineGroup.selectAll('.sacred-point')
            .on('mouseenter', (event, d) => {
                const point = d3.select(event.target);
                
                point.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('r', 6)
                    .style('opacity', 1);

                this.showTooltip(event, d);
            })
            .on('mouseleave', (event) => {
                const point = d3.select(event.target);
                
                point.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('r', 4)
                    .style('opacity', 0.8);

                this.hideTooltip();
            });
    }
}
/**
 * Sacred Candlestick Chart Implementation
 * Based on sacred geometry and golden ratio patterns
 */
class SacredCandlestickChart extends SacredBaseChart {
    constructor(container, data, options) {
        super(container, {
            ...options,
            type: 'sacred-chart-candlestick'
        });
        
        this.candleGroup = null;
        this.volumeGroup = null;
        this.setupScales();
        this.draw();
    }

    /**
     * Setup scales specific to candlestick chart
     */
    setupScales() {
        const { innerWidth, innerHeight } = this.dimensions;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        // Calculate price range with golden ratio padding
        const priceRange = {
            min: d3.min(this.data, d => d.low) * phi_inverse,
            max: d3.max(this.data, d => d.high) * phi
        };

        this.scales = {
            x: d3.scaleBand()
                .domain(this.data.map(d => d.date))
                .range([0, innerWidth])
                .padding(SACRED_CONSTANTS.MATH.PHI_INVERSE),

            y: d3.scaleLinear()
                .domain([priceRange.min, priceRange.max])
                .range([innerHeight, 0]),

            volume: d3.scaleLinear()
                .domain([0, d3.max(this.data, d => d.volume)])
                .range([0, innerHeight * SACRED_CONSTANTS.MATH.PHI_INVERSE])
        };
    }

    /**
     * Draw chart implementation
     */
    draw() {
        // Create groups
        this.volumeGroup = this.svg.append('g')
            .attr('class', 'sacred-volume-group');

        this.candleGroup = this.svg.append('g')
            .attr('class', 'sacred-candle-group');

        // Draw elements
        this.drawVolume();
        this.drawCandles();
        this.drawFibonacciLevels();

        // Add animations if enabled
        if (this.options.animated) {
            this.animateChart();
        }

        // Add interactions if enabled
        if (this.options.interactive) {
            this.setupInteractions();
        }
    }

    /**
     * Draw volume bars
     */
    drawVolume() {
        this.volumeGroup.selectAll('.sacred-volume-bar')
            .data(this.data)
            .enter()
            .append('rect')
            .attr('class', 'sacred-volume-bar')
            .attr('x', d => this.scales.x(d.date))
            .attr('y', d => this.dimensions.innerHeight - this.scales.volume(d.volume))
            .attr('width', this.scales.x.bandwidth())
            .attr('height', d => this.scales.volume(d.volume))
            .attr('fill', d => d.close > d.open ? 'var(--chart-up-color)' : 'var(--chart-down-color)')
            .attr('opacity', 0.3);
    }

    /**
     * Draw candlesticks
     */
    drawCandles() {
        // Draw wicks
        const wicks = this.candleGroup.selectAll('.sacred-candle-wick')
            .data(this.data)
            .enter()
            .append('line')
            .attr('class', 'sacred-candle-wick')
            .attr('x1', d => this.scales.x(d.date) + this.scales.x.bandwidth() / 2)
            .attr('x2', d => this.scales.x(d.date) + this.scales.x.bandwidth() / 2)
            .attr('y1', d => this.scales.y(d.high))
            .attr('y2', d => this.scales.y(d.low))
            .attr('stroke', d => d.close > d.open ? 'var(--chart-up-color)' : 'var(--chart-down-color)');

        // Draw candle bodies
        const candles = this.candleGroup.selectAll('.sacred-candle-body')
            .data(this.data)
            .enter()
            .append('rect')
            .attr('class', 'sacred-candle-body')
            .attr('x', d => this.scales.x(d.date))
            .attr('y', d => this.scales.y(Math.max(d.open, d.close)))
            .attr('width', this.scales.x.bandwidth())
            .attr('height', d => Math.abs(this.scales.y(d.open) - this.scales.y(d.close)))
            .attr('fill', d => d.close > d.open ? 'var(--chart-up-color)' : 'var(--chart-down-color)');
    }

    /**
     * Draw Fibonacci levels
     */
    drawFibonacciLevels() {
        const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];
        const priceRange = this.scales.y.domain();
        const range = priceRange[1] - priceRange[0];

        this.fibGroup = this.svg.append('g')
            .attr('class', 'sacred-fibonacci-group');

        levels.forEach(level => {
            const y = this.scales.y(priceRange[0] + range * level);
            
            this.fibGroup.append('line')
                .attr('class', 'sacred-fibonacci-line')
                .attr('x1', 0)
                .attr('x2', this.dimensions.innerWidth)
                .attr('y1', y)
                .attr('y2', y)
                .attr('stroke', 'var(--chart-grid-color)')
                .attr('stroke-width', 0.5)
                .attr('stroke-dasharray', '2,2')
                .attr('opacity', 0.3);

            this.fibGroup.append('text')
                .attr('class', 'sacred-fibonacci-label')
                .attr('x', this.dimensions.innerWidth + 5)
                .attr('y', y)
                .attr('dy', '0.32em')
                .text(`${(level * 100).toFixed(1)}%`)
                .style('font-size', 'var(--chart-label-size)')
                .style('fill', 'var(--chart-label-color)');
        });
    }

    /**
     * Animate chart elements
     */
    animateChart() {
        // Animate volume bars
        this.volumeGroup.selectAll('.sacred-volume-bar')
            .attr('y', this.dimensions.innerHeight)
            .attr('height', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .delay((d, i) => i * SACRED_CONSTANTS.TIMING.DELAY)
            .attr('y', d => this.dimensions.innerHeight - this.scales.volume(d.volume))
            .attr('height', d => this.scales.volume(d.volume));

        // Animate candles
        this.candleGroup.selectAll('.sacred-candle-body')
            .attr('transform', 'scaleY(0)')
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .delay((d, i) => i * SACRED_CONSTANTS.TIMING.DELAY)
            .attr('transform', 'scaleY(1)');

        // Animate wicks
        this.candleGroup.selectAll('.sacred-candle-wick')
            .attr('y1', d => this.scales.y((d.high + d.low) / 2))
            .attr('y2', d => this.scales.y((d.high + d.low) / 2))
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .delay((d, i) => i * SACRED_CONSTANTS.TIMING.DELAY)
            .attr('y1', d => this.scales.y(d.high))
            .attr('y2', d => this.scales.y(d.low));
    }
}
/**
 * Sacred Scatter Chart Implementation
 * Based on sacred geometry and divine proportions
 */
class SacredScatterChart extends SacredBaseChart {
    constructor(container, data, options) {
        super(container, {
            ...options,
            type: 'sacred-chart-scatter'
        });
        
        this.pointsGroup = null;
        this.gridGroup = null;
        this.setupScales();
        this.draw();
    }

    /**
     * Setup scales specific to scatter chart
     */
    setupScales() {
        const { innerWidth, innerHeight } = this.dimensions;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        this.scales = {
            x: d3.scaleLinear()
                .domain([
                    d3.min(this.data, d => d.x) * phi_inverse,
                    d3.max(this.data, d => d.x) * phi
                ])
                .range([0, innerWidth]),

            y: d3.scaleLinear()
                .domain([
                    d3.min(this.data, d => d.y) * phi_inverse,
                    d3.max(this.data, d => d.y) * phi
                ])
                .range([innerHeight, 0]),

            size: d3.scaleLinear()
                .domain(d3.extent(this.data, d => d.value || 1))
                .range([
                    4 * SACRED_CONSTANTS.MATH.PHI_INVERSE,
                    4 * SACRED_CONSTANTS.MATH.PHI
                ]),

            color: d3.scaleOrdinal()
                .domain(this.data.map(d => d.category))
                .range(this.options.colors)
        };
    }

    /**
     * Draw chart implementation
     */
    draw() {
        // Create groups
        this.gridGroup = this.svg.append('g')
            .attr('class', 'sacred-grid-group');
        
        this.pointsGroup = this.svg.append('g')
            .attr('class', 'sacred-points-group');

        // Draw elements
        this.drawGrid();
        this.drawPoints();
        this.drawGoldenRatioGuides();

        // Add animations if enabled
        if (this.options.animated) {
            this.animateChart();
        }

        // Add interactions if enabled
        if (this.options.interactive) {
            this.setupInteractions();
        }
    }

    /**
     * Draw sacred grid
     */
    drawGrid() {
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;
        const gridLines = [0, phi_inverse, 1/phi, 1, phi, phi * phi];

        // Draw vertical lines
        gridLines.forEach(ratio => {
            const x = this.scales.x.range()[1] * ratio;
            this.gridGroup.append('line')
                .attr('class', 'sacred-grid-line')
                .attr('x1', x)
                .attr('x2', x)
                .attr('y1', 0)
                .attr('y2', this.dimensions.innerHeight)
                .attr('stroke', 'var(--chart-grid-color)')
                .attr('stroke-width', 0.5)
                .attr('opacity', 0.2);
        });

        // Draw horizontal lines
        gridLines.forEach(ratio => {
            const y = this.scales.y.range()[0] * ratio;
            this.gridGroup.append('line')
                .attr('class', 'sacred-grid-line')
                .attr('x1', 0)
                .attr('x2', this.dimensions.innerWidth)
                .attr('y1', y)
                .attr('y2', y)
                .attr('stroke', 'var(--chart-grid-color)')
                .attr('stroke-width', 0.5)
                .attr('opacity', 0.2);
        });
    }

    /**
     * Draw data points
     */
    drawPoints() {
        this.pointsGroup.selectAll('.sacred-point')
            .data(this.data)
            .enter()
            .append('circle')
            .attr('class', 'sacred-point')
            .attr('cx', d => this.scales.x(d.x))
            .attr('cy', d => this.scales.y(d.y))
            .attr('r', d => this.scales.size(d.value || 1))
            .attr('fill', d => this.scales.color(d.category))
            .attr('stroke', 'var(--surface-primary)')
            .attr('stroke-width', 1)
            .attr('opacity', 0.8);
    }

    /**
     * Draw golden ratio guides
     */
    drawGoldenRatioGuides() {
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;
        const { innerWidth, innerHeight } = this.dimensions;

        // Draw golden spiral guide
        const spiralPoints = [];
        let radius = Math.min(innerWidth, innerHeight) / (phi * 2);
        let angle = 0;

        for (let i = 0; i < 360; i += 5) {
            angle = i * Math.PI / 180;
            radius = radius * Math.pow(phi, -angle / (2 * Math.PI));
            spiralPoints.push([
                innerWidth/2 + radius * Math.cos(angle),
                innerHeight/2 + radius * Math.sin(angle)
            ]);
        }

        const spiralLine = d3.line()(spiralPoints);

        this.gridGroup.append('path')
            .attr('class', 'sacred-spiral-guide')
            .attr('d', spiralLine)
            .attr('fill', 'none')
            .attr('stroke', 'var(--chart-decoration-color)')
            .attr('stroke-width', 0.5)
            .attr('opacity', 0.1);
    }

    /**
     * Animate chart elements
     */
    animateChart() {
        this.pointsGroup.selectAll('.sacred-point')
            .attr('r', 0)
            .attr('opacity', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .delay((d, i) => i * SACRED_CONSTANTS.TIMING.DELAY)
            .attr('r', d => this.scales.size(d.value || 1))
            .attr('opacity', 0.8);

        this.gridGroup.selectAll('.sacred-grid-line')
            .attr('opacity', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .attr('opacity', 0.2);

        this.gridGroup.select('.sacred-spiral-guide')
            .attr('opacity', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .attr('opacity', 0.1);
    }

    /**
     * Setup chart interactions
     */
    setupInteractions() {
        this.pointsGroup.selectAll('.sacred-point')
            .on('mouseenter', (event, d) => {
                const point = d3.select(event.target);
                
                point.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('r', r => r * SACRED_CONSTANTS.MATH.PHI)
                    .attr('opacity', 1);

                this.showTooltip(event, d);
            })
            .on('mouseleave', (event) => {
                const point = d3.select(event.target);
                
                point.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('r', d => this.scales.size(d.value || 1))
                    .attr('opacity', 0.8);

                this.hideTooltip();
            });
    }
}
/**
 * Sacred Grid System
 * Based on sacred geometry and golden ratio principles
 */
class SacredGridSystem {
    constructor(chart) {
        this.chart = chart;
        this.gridGroup = null;
        this.axisGroup = null;
        this.setupGrid();
    }

    /**
     * Setup grid system
     */
    setupGrid() {
        this.gridGroup = this.chart.svg.append('g')
            .attr('class', 'sacred-grid-group');
        
        this.axisGroup = this.chart.svg.append('g')
            .attr('class', 'sacred-axis-group');

        this.drawGrid();
        this.drawAxes();
        this.addSacredGuides();
    }

    /**
     * Draw grid lines
     */
    drawGrid() {
        const { innerWidth, innerHeight } = this.chart.dimensions;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;
        
        // Calculate sacred divisions
        const divisions = [0, phi_inverse, 1/phi, 1, phi, phi * phi];

        // Draw vertical lines
        divisions.forEach(ratio => {
            const x = innerWidth * ratio;
            this.gridGroup.append('line')
                .attr('class', 'sacred-grid-line sacred-grid-line-vertical')
                .attr('x1', x)
                .attr('x2', x)
                .attr('y1', 0)
                .attr('y2', innerHeight)
                .style('stroke', 'var(--chart-grid-color)')
                .style('stroke-width', 'var(--chart-grid-width)')
                .style('opacity', 0.2);
        });

        // Draw horizontal lines
        divisions.forEach(ratio => {
            const y = innerHeight * ratio;
            this.gridGroup.append('line')
                .attr('class', 'sacred-grid-line sacred-grid-line-horizontal')
                .attr('x1', 0)
                .attr('x2', innerWidth)
                .attr('y1', y)
                .attr('y2', y)
                .style('stroke', 'var(--chart-grid-color)')
                .style('stroke-width', 'var(--chart-grid-width)')
                .style('opacity', 0.2);
        });
    }

    /**
     * Draw chart axes
     */
    drawAxes() {
        const { innerWidth, innerHeight } = this.chart.dimensions;

        // Create axes
        const xAxis = d3.axisBottom(this.chart.scales.x)
            .ticks(Math.round(innerWidth / (100 * SACRED_CONSTANTS.MATH.PHI_INVERSE)))
            .tickSize(-innerHeight);

        const yAxis = d3.axisLeft(this.chart.scales.y)
            .ticks(Math.round(innerHeight / (100 * SACRED_CONSTANTS.MATH.PHI_INVERSE)))
            .tickSize(-innerWidth);

        // Add X axis
        this.axisGroup.append('g')
            .attr('class', 'sacred-axis sacred-axis-x')
            .attr('transform', `translate(0,${innerHeight})`)
            .call(xAxis)
            .call(g => g.select('.domain').remove())
            .call(g => g.selectAll('.tick line')
                .attr('class', 'sacred-grid-line')
                .style('stroke', 'var(--chart-grid-color)')
                .style('stroke-width', 'var(--chart-grid-width)')
                .style('opacity', 0.1));

        // Add Y axis
        this.axisGroup.append('g')
            .attr('class', 'sacred-axis sacred-axis-y')
            .call(yAxis)
            .call(g => g.select('.domain').remove())
            .call(g => g.selectAll('.tick line')
                .attr('class', 'sacred-grid-line')
                .style('stroke', 'var(--chart-grid-color)')
                .style('stroke-width', 'var(--chart-grid-width)')
                .style('opacity', 0.1));
    }

    /**
     * Add sacred geometry guides
     */
    addSacredGuides() {
        const { innerWidth, innerHeight } = this.chart.dimensions;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        // Add golden rectangles
        this.drawGoldenRectangles(innerWidth, innerHeight);
        
        // Add golden spiral guide
        this.drawGoldenSpiral(Math.min(innerWidth, innerHeight) / 2);
    }

    /**
     * Draw golden rectangles
     */
    drawGoldenRectangles(width, height) {
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;
        
        this.gridGroup.append('rect')
            .attr('class', 'sacred-guide sacred-golden-rectangle')
            .attr('width', width / phi)
            .attr('height', height / phi)
            .attr('fill', 'none')
            .attr('stroke', 'var(--chart-decoration-color)')
            .attr('stroke-width', 0.5)
            .attr('opacity', 0.1);
    }

    /**
     * Draw golden spiral
     */
    drawGoldenSpiral(radius) {
        const spiral = d3.lineRadial()
            .angle(d => d * SACRED_CONSTANTS.MATH.ANGLES.GOLDEN)
            .radius(d => d * radius * SACRED_CONSTANTS.MATH.PHI_INVERSE);

        const points = d3.range(0, 4 * Math.PI, 0.1);

        this.gridGroup.append('path')
            .attr('class', 'sacred-guide sacred-golden-spiral')
            .attr('d', spiral(points))
            .attr('fill', 'none')
            .attr('stroke', 'var(--chart-decoration-color)')
            .attr('stroke-width', 0.5)
            .attr('opacity', 0.1);
    }

    /**
     * Update grid on resize
     */
    update() {
        // Clear existing grid
        this.gridGroup.selectAll('*').remove();
        this.axisGroup.selectAll('*').remove();

        // Redraw grid
        this.drawGrid();
        this.drawAxes();
        this.addSacredGuides();
    }
}
/**
 * Sacred Candlestick Chart Implementation
 * Based on sacred geometry and divine proportions for financial visualization
 */
class SacredCandlestickChart extends SacredBaseChart {
    constructor(container, data, options) {
        super(container, {
            ...options,
            type: 'sacred-chart-candlestick'
        });
        
        this.candleGroup = null;
        this.volumeGroup = null;
        this.setupScales();
        this.draw();
    }

    /**
     * Setup scales specific to candlestick chart
     */
    setupScales() {
        const { innerWidth, innerHeight } = this.dimensions;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        this.scales = {
            x: d3.scaleBand()
                .domain(this.data.map(d => d.date))
                .range([0, innerWidth])
                .padding(SACRED_CONSTANTS.MATH.PHI_INVERSE),

            y: d3.scaleLinear()
                .domain([
                    d3.min(this.data, d => d.low) * phi_inverse,
                    d3.max(this.data, d => d.high) * phi
                ])
                .range([innerHeight, 0]),

            volume: d3.scaleLinear()
                .domain([0, d3.max(this.data, d => d.volume)])
                .range([0, innerHeight * SACRED_CONSTANTS.MATH.PHI_INVERSE])
        };
    }

    /**
     * Draw chart implementation
     */
    draw() {
        // Create groups
        this.volumeGroup = this.svg.append('g')
            .attr('class', 'sacred-volume-group');
            
        this.candleGroup = this.svg.append('g')
            .attr('class', 'sacred-candle-group');

        // Draw elements
        this.drawVolume();
        this.drawCandles();
        this.drawFibonacciLevels();

        // Add animations if enabled
        if (this.options.animated) {
            this.animateChart();
        }

        // Add interactions if enabled
        if (this.options.interactive) {
            this.setupInteractions();
        }
    }

    /**
     * Setup interactions for candlesticks
     */
    setupInteractions() {
        // Candle interactions
        this.candleGroup.selectAll('.sacred-candle-body')
            .on('mouseenter', (event, d) => {
                const candle = d3.select(event.target);
                const wick = d3.select(
                    this.candleGroup.select(`#wick-${d.date}`)
                );
                
                // Highlight candle
                candle.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .style('opacity', 1)
                    .style('filter', 'brightness(1.2)');
                
                wick.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .style('opacity', 1)
                    .style('stroke-width', 2);

                this.showTooltip(event, d);
            })
            .on('mouseleave', (event, d) => {
                const candle = d3.select(event.target);
                const wick = d3.select(
                    this.candleGroup.select(`#wick-${d.date}`)
                );
                
                // Reset candle
                candle.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .style('opacity', 0.8)
                    .style('filter', null);
                
                wick.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .style('opacity', 0.8)
                    .style('stroke-width', 1);

                this.hideTooltip();
            });
    }

    /**
     * Show tooltip with candlestick data
     */
    showTooltip(event, d) {
        const formatPrice = d3.format(',.2f');
        const formatVolume = d3.format(',.0f');
        
        this.tooltip
            .style('display', 'block')
            .html(`
                <div class="sacred-tooltip-content">
                    <div class="sacred-tooltip-date">${d.date}</div>
                    <div class="sacred-tooltip-price">
                        <span>O: ${formatPrice(d.open)}</span>
                        <span>H: ${formatPrice(d.high)}</span>
                        <span>L: ${formatPrice(d.low)}</span>
                        <span>C: ${formatPrice(d.close)}</span>
                    </div>
                    <div class="sacred-tooltip-volume">
                        Vol: ${formatVolume(d.volume)}
                    </div>
                </div>
            `)
            .style('left', `${event.pageX + 10}px`)
            .style('top', `${event.pageY - 10}px`);
    }

    /**
     * Draw Fibonacci levels
     */
    drawFibonacciLevels() {
        const priceRange = this.scales.y.domain();
        const range = priceRange[1] - priceRange[0];
        const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];

        this.fibGroup = this.svg.append('g')
            .attr('class', 'sacred-fibonacci-group');

        levels.forEach(level => {
            const y = this.scales.y(priceRange[0] + range * level);
            
            // Draw level line
            this.fibGroup.append('line')
                .attr('class', 'sacred-fibonacci-line')
                .attr('x1', 0)
                .attr('x2', this.dimensions.innerWidth)
                .attr('y1', y)
                .attr('y2', y)
                .attr('stroke', 'var(--chart-grid-color)')
                .attr('stroke-width', 0.5)
                .attr('stroke-dasharray', '2,2')
                .attr('opacity', 0.3);

            // Add level label
            this.fibGroup.append('text')
                .attr('class', 'sacred-fibonacci-label')
                .attr('x', this.dimensions.innerWidth + 5)
                .attr('y', y)
                .attr('dy', '0.32em')
                .text(`${(level * 100).toFixed(1)}%`)
                .style('font-size', 'var(--chart-label-size)')
                .style('fill', 'var(--chart-label-color)');
        });
    }

    /**
     * Clean up chart
     */
    destroy() {
        // Remove event listeners
        this.candleGroup.selectAll('.sacred-candle-body')
            .on('mouseenter', null)
            .on('mouseleave', null);

        // Remove tooltip
        if (this.tooltip) {
            this.tooltip.remove();
        }

        super.destroy();
    }
}
/**
 * Sacred Chart Legend Component
 * Based on sacred geometry and divine proportions
 */
class SacredChartLegend {
    constructor(chart, options = {}) {
        this.chart = chart;
        this.options = this.mergeOptions(options);
        this.container = null;
        this.items = [];
        this.initialize();
    }

    /**
     * Merge default options with user options
     */
    mergeOptions(options) {
        return {
            position: options.position || 'right',
            alignment: options.alignment || 'middle',
            itemSpacing: options.itemSpacing || 
                `var(--space-md)`,
            symbolSize: options.symbolSize || 
                `calc(var(--font-size-base) * var(--phi-inverse))`,
            interactive: options.interactive !== false,
            animated: options.animated !== false
        };
    }

    /**
     * Initialize legend
     */
    initialize() {
        this.container = this.chart.svg.append('g')
            .attr('class', 'sacred-chart-legend')
            .attr('transform', this.calculatePosition());

        this.createItems();
        
        if (this.options.animated) {
            this.animateEntrance();
        }

        if (this.options.interactive) {
            this.setupInteractions();
        }
    }

    /**
     * Create legend items
     */
    createItems() {
        const data = this.chart.data;
        const colors = this.chart.options.colors;

        this.items = this.container.selectAll('.legend-item')
            .data(data)
            .enter()
            .append('g')
            .attr('class', 'legend-item')
            .attr('transform', (d, i) => 
                `translate(0, ${i * this.calculateItemSpacing()})`);

        // Add symbols
        this.items.append('rect')
            .attr('width', this.options.symbolSize)
            .attr('height', this.options.symbolSize)
            .attr('rx', `calc(${this.options.symbolSize} * var(--phi-inverse))`)
            .attr('fill', (d, i) => colors[i % colors.length]);

        // Add labels
        this.items.append('text')
            .attr('x', `calc(${this.options.symbolSize} * var(--phi))`)
            .attr('y', `calc(${this.options.symbolSize} * var(--phi-inverse))`)
            .attr('dy', '0.32em')
            .attr('class', 'sacred-chart-legend-label')
            .text(d => d.label || d.category)
            .style('font-size', 'var(--font-size-sm)')
            .style('fill', 'var(--color-text-primary)');
    }

    /**
     * Calculate legend position
     */
    calculatePosition() {
        const { width, height } = this.chart.dimensions;
        const legendBBox = this.container?.node()?.getBBox() || { width: 0, height: 0 };

        switch (this.options.position) {
            case 'right':
                return `translate(${width + 20}, ${this.getVerticalAlignment(height, legendBBox.height)})`;
            case 'left':
                return `translate(-${legendBBox.width + 20}, ${this.getVerticalAlignment(height, legendBBox.height)})`;
            case 'bottom':
                return `translate(${this.getHorizontalAlignment(width, legendBBox.width)}, ${height + 20})`;
            case 'top':
                return `translate(${this.getHorizontalAlignment(width, legendBBox.width)}, -20)`;
            default:
                return `translate(${width + 20}, 0)`;
        }
    }

    /**
     * Calculate item spacing using golden ratio
     */
    calculateItemSpacing() {
        return parseFloat(this.options.symbolSize) * SacredCore.constants.MATH.PHI.VALUE;
    }

    /**
     * Get vertical alignment
     */
    getVerticalAlignment(containerHeight, legendHeight) {
        switch (this.options.alignment) {
            case 'start': return 0;
            case 'end': return containerHeight - legendHeight;
            default: return (containerHeight - legendHeight) / 2;
        }
    }

    /**
     * Get horizontal alignment
     */
    getHorizontalAlignment(containerWidth, legendWidth) {
        switch (this.options.alignment) {
            case 'start': return 0;
            case 'end': return containerWidth - legendWidth;
            default: return (containerWidth - legendWidth) / 2;
        }
    }

    /**
     * Animate legend entrance
     */
    animateEntrance() {
        this.items
            .attr('opacity', 0)
            .attr('transform', (d, i) => 
                `translate(-20, ${i * this.calculateItemSpacing()})`)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .delay((d, i) => i * SACRED_CONSTANTS.TIMING.DELAY)
            .attr('opacity', 1)
            .attr('transform', (d, i) => 
                `translate(0, ${i * this.calculateItemSpacing()})`);
    }

    /**
     * Setup legend interactions
     */
    setupInteractions() {
        this.items
            .style('cursor', 'pointer')
            .on('mouseenter', (event, d) => {
                const item = d3.select(event.currentTarget);
                
                item.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('transform', (d, i) => 
                        `translate(5, ${i * this.calculateItemSpacing()})`)
                    .attr('opacity', 1);

                this.chart.highlightData(d);
            })
            .on('mouseleave', (event, d) => {
                const item = d3.select(event.currentTarget);
                
                item.transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('transform', (d, i) => 
                        `translate(0, ${i * this.calculateItemSpacing()})`)
                    .attr('opacity', 0.8);

                this.chart.unhighlightData(d);
            });
    }

    /**
     * Update legend
     */
    update() {
        this.container
            .attr('transform', this.calculatePosition());
        
        this.items
            .attr('transform', (d, i) => 
                `translate(0, ${i * this.calculateItemSpacing()})`);
    }
}
/**
 * Sacred Chart Tooltip Component
 * Based on sacred geometry and divine proportions
 */
class SacredChartTooltip {
    constructor(chart, options = {}) {
        this.chart = chart;
        this.options = this.mergeOptions(options);
        this.element = null;
        this.visible = false;
        this.initialize();
    }

    /**
     * Merge default options with user options
     */
    mergeOptions(options) {
        return {
            position: options.position || 'dynamic',
            offset: options.offset || {
                x: 10 * SACRED_CONSTANTS.MATH.PHI_INVERSE,
                y: -10 * SACRED_CONSTANTS.MATH.PHI_INVERSE
            },
            animation: options.animation !== false,
            className: options.className || 'sacred-chart-tooltip',
            showDelay: options.showDelay || SACRED_CONSTANTS.TIMING.HOVER,
            hideDelay: options.hideDelay || SACRED_CONSTANTS.TIMING.HOVER
        };
    }

    /**
     * Initialize tooltip
     */
    initialize() {
        this.element = document.createElement('div');
        this.element.className = this.options.className;
        this.element.style.position = 'absolute';
        this.element.style.visibility = 'hidden';
        this.element.style.opacity = '0';
        this.element.style.pointerEvents = 'none';
        this.element.style.transition = `
            opacity var(--transition-duration-quick) var(--ease-golden),
            transform var(--transition-duration-quick) var(--ease-golden)
        `;

        document.body.appendChild(this.element);
    }

    /**
     * Show tooltip
     */
    show(event, data) {
        if (!this.element) return;

        // Update content
        this.updateContent(data);

        // Calculate position
        const position = this.calculatePosition(event);

        // Apply position
        this.element.style.left = `${position.x}px`;
        this.element.style.top = `${position.y}px`;

        // Show with animation
        if (this.options.animation) {
            this.element.style.transform = 'scale(var(--scale-phi-inverse))';
            this.element.style.visibility = 'visible';
            
            requestAnimationFrame(() => {
                this.element.style.opacity = '1';
                this.element.style.transform = 'scale(1)';
            });
        } else {
            this.element.style.visibility = 'visible';
            this.element.style.opacity = '1';
        }

        this.visible = true;
    }

    /**
     * Hide tooltip
     */
    hide() {
        if (!this.element || !this.visible) return;

        if (this.options.animation) {
            this.element.style.opacity = '0';
            this.element.style.transform = 'scale(var(--scale-phi-inverse))';
            
            setTimeout(() => {
                this.element.style.visibility = 'hidden';
            }, this.options.hideDelay);
        } else {
            this.element.style.visibility = 'hidden';
            this.element.style.opacity = '0';
        }

        this.visible = false;
    }

    /**
     * Calculate tooltip position
     */
    calculatePosition(event) {
        const rect = this.element.getBoundingClientRect();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        let x = event.pageX + this.options.offset.x;
        let y = event.pageY + this.options.offset.y;

        // Adjust for viewport boundaries
        if (x + rect.width > viewportWidth) {
            x = event.pageX - rect.width - this.options.offset.x;
        }

        if (y + rect.height > viewportHeight) {
            y = event.pageY - rect.height - this.options.offset.y;
        }

        return { x, y };
    }

    /**
     * Update tooltip content
     */
    updateContent(data) {
        if (typeof data === 'string') {
            this.element.innerHTML = data;
        } else {
            this.element.innerHTML = this.formatContent(data);
        }
    }

    /**
     * Format tooltip content
     */
    formatContent(data) {
        if (!data) return '';

        return `
            <div class="sacred-tooltip-content">
                ${data.title ? `
                    <div class="sacred-tooltip-title">${data.title}</div>
                ` : ''}
                ${data.value ? `
                    <div class="sacred-tooltip-value">${data.value}</div>
                ` : ''}
                ${data.details ? `
                    <div class="sacred-tooltip-details">
                        ${Object.entries(data.details)
                            .map(([key, value]) => `
                                <div class="sacred-tooltip-detail">
                                    <span class="sacred-tooltip-key">${key}:</span>
                                    <span class="sacred-tooltip-value">${value}</span>
                                </div>
                            `).join('')}
                    </div>
                ` : ''}
            </div>
        `;
    }

    /**
     * Clean up tooltip
     */
    destroy() {
        if (this.element && this.element.parentNode) {
            this.element.parentNode.removeChild(this.element);
        }
        this.element = null;
    }
}
/**
 * Sacred Chart Axis System
 * Based on sacred geometry and divine proportions
 */
class SacredAxisSystem {
    constructor(chart) {
        this.chart = chart;
        this.xAxis = null;
        this.yAxis = null;
        this.gridGroup = null;
        this.initialize();
    }

    /**
     * Initialize axis system
     */
    initialize() {
        this.gridGroup = this.chart.svg.append('g')
            .attr('class', 'sacred-grid-group');

        this.xAxis = this.chart.svg.append('g')
            .attr('class', 'sacred-axis sacred-axis-x')
            .attr('transform', `translate(0,${this.chart.dimensions.innerHeight})`);

        this.yAxis = this.chart.svg.append('g')
            .attr('class', 'sacred-axis sacred-axis-y');

        this.setupAxes();
        this.setupGrid();
        
        if (this.chart.options.animated) {
            this.animateAxes();
        }
    }

    /**
     * Setup axes with sacred proportions
     */
    setupAxes() {
        const { innerWidth, innerHeight } = this.chart.dimensions;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        // Calculate tick counts based on golden ratio
        const xTickCount = Math.round(innerWidth / (100 * SACRED_CONSTANTS.MATH.PHI_INVERSE));
        const yTickCount = Math.round(innerHeight / (100 * SACRED_CONSTANTS.MATH.PHI_INVERSE));

        // Create axis generators
        const xAxisGenerator = d3.axisBottom(this.chart.scales.x)
            .ticks(xTickCount)
            .tickSize(-innerHeight)
            .tickPadding(10);

        const yAxisGenerator = d3.axisLeft(this.chart.scales.y)
            .ticks(yTickCount)
            .tickSize(-innerWidth)
            .tickPadding(10);

        // Apply axes
        this.xAxis.call(xAxisGenerator);
        this.yAxis.call(yAxisGenerator);

        // Style axes
        this.styleAxes();
    }

    /**
     * Setup sacred grid
     */
    setupGrid() {
        const { innerWidth, innerHeight } = this.chart.dimensions;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        // Create golden section lines
        const goldenSections = [0, phi_inverse, 1/phi, 1, phi];

        // Vertical golden lines
        goldenSections.forEach(ratio => {
            this.gridGroup.append('line')
                .attr('class', 'sacred-grid-line sacred-grid-golden')
                .attr('x1', innerWidth * ratio)
                .attr('x2', innerWidth * ratio)
                .attr('y1', 0)
                .attr('y2', innerHeight)
                .style('stroke', 'var(--chart-grid-color)')
                .style('stroke-width', 0.5)
                .style('opacity', 0.3);
        });

        // Horizontal golden lines
        goldenSections.forEach(ratio => {
            this.gridGroup.append('line')
                .attr('class', 'sacred-grid-line sacred-grid-golden')
                .attr('x1', 0)
                .attr('x2', innerWidth)
                .attr('y1', innerHeight * ratio)
                .attr('y2', innerHeight * ratio)
                .style('stroke', 'var(--chart-grid-color)')
                .style('stroke-width', 0.5)
                .style('opacity', 0.3);
        });
    }

    /**
     * Style axes with sacred geometry principles
     */
    styleAxes() {
        // Remove domain paths
        this.xAxis.select('.domain').remove();
        this.yAxis.select('.domain').remove();

        // Style tick lines
        this.xAxis.selectAll('.tick line')
            .attr('class', 'sacred-grid-line')
            .style('stroke', 'var(--chart-grid-color)')
            .style('stroke-width', 0.5)
            .style('opacity', 0.2);

        this.yAxis.selectAll('.tick line')
            .attr('class', 'sacred-grid-line')
            .style('stroke', 'var(--chart-grid-color)')
            .style('stroke-width', 0.5)
            .style('opacity', 0.2);

        // Style tick text
        this.xAxis.selectAll('.tick text')
            .style('font-size', 'var(--chart-label-size)')
            .style('fill', 'var(--chart-label-color)');

        this.yAxis.selectAll('.tick text')
            .style('font-size', 'var(--chart-label-size)')
            .style('fill', 'var(--chart-label-color)');
    }

    /**
     * Animate axes entrance
     */
    animateAxes() {
        // Animate grid lines
        this.gridGroup.selectAll('.sacred-grid-line')
            .style('opacity', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .style('opacity', 0.2);

        // Animate X-axis
        this.xAxis.selectAll('.tick')
            .style('opacity', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .delay((d, i) => i * SACRED_CONSTANTS.TIMING.DELAY)
            .style('opacity', 1);

        // Animate Y-axis
        this.yAxis.selectAll('.tick')
            .style('opacity', 0)
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .delay((d, i) => i * SACRED_CONSTANTS.TIMING.DELAY)
            .style('opacity', 1);
    }

    /**
     * Update axes on data change
     */
    update() {
        this.setupAxes();
        this.setupGrid();
    }
}
/**
 * Sacred Scatter Chart Implementation
 * Based on sacred geometry and divine proportions
 */
class SacredScatterChart extends SacredBaseChart {
    constructor(container, data, options) {
        super(container, {
            ...options,
            type: 'sacred-chart-scatter'
        });
        
        this.pointsGroup = null;
        this.setupScales();
        this.draw();
    }

    /**
     * Setup scales specific to scatter chart
     */
    setupScales() {
        const { innerWidth, innerHeight } = this.dimensions;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        this.scales = {
            x: d3.scaleLinear()
                .domain([
                    d3.min(this.data, d => d.x) * phi_inverse,
                    d3.max(this.data, d => d.x) * phi
                ])
                .range([0, innerWidth]),

            y: d3.scaleLinear()
                .domain([
                    d3.min(this.data, d => d.y) * phi_inverse,
                    d3.max(this.data, d => d.y) * phi
                ])
                .range([innerHeight, 0]),

            size: d3.scaleLinear()
                .domain(d3.extent(this.data, d => d.value || 1))
                .range([4 * phi_inverse, 4 * phi]),

            color: d3.scaleOrdinal()
                .domain(this.data.map(d => d.category))
                .range(this.options.colors)
        };
    }

    /**
     * Draw chart implementation
     */
    draw() {
        this.pointsGroup = this.svg.append('g')
            .attr('class', 'sacred-points-group');

        // Draw sacred geometry background
        this.drawSacredBackground();
        
        // Draw points
        this.drawPoints();

        // Add animations if enabled
        if (this.options.animated) {
            this.animateChart();
        }

        // Add interactions if enabled
        if (this.options.interactive) {
            this.setupInteractions();
        }
    }

    /**
     * Draw sacred geometry background
     */
    drawSacredBackground() {
        const { innerWidth, innerHeight } = this.dimensions;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        // Create golden spiral guide
        const spiralPoints = [];
        let radius = Math.min(innerWidth, innerHeight) / (phi * 2);
        let angle = 0;

        for (let i = 0; i < 360; i += 5) {
            angle = i * Math.PI / 180;
            radius = radius * Math.pow(phi, -angle / (2 * Math.PI));
            spiralPoints.push([
                innerWidth/2 + radius * Math.cos(angle),
                innerHeight/2 + radius * Math.sin(angle)
            ]);
        }

        const spiralLine = d3.line()(spiralPoints);

        this.svg.append('path')
            .attr('class', 'sacred-spiral-guide')
            .attr('d', spiralLine)
            .attr('fill', 'none')
            .attr('stroke', 'var(--chart-decoration-color)')
            .attr('stroke-width', 0.5)
            .attr('opacity', 0.1);
    }

    /**
     * Draw data points
     */
    drawPoints() {
        this.pointsGroup.selectAll('.sacred-point')
            .data(this.data)
            .enter()
            .append('g')
            .attr('class', 'sacred-point')
            .each((d, i, nodes) => {
                const point = d3.select(nodes[i]);
                
                // Draw point circle
                point.append('circle')
                    .attr('cx', d => this.scales.x(d.x))
                    .attr('cy', d => this.scales.y(d.y))
                    .attr('r', d => this.scales.size(d.value || 1))
                    .attr('fill', d => this.scales.color(d.category))
                    .attr('stroke', 'var(--surface-primary)')
                    .attr('stroke-width', 1)
                    .attr('opacity', 0.8);

                // Add sacred geometry decoration
                this.addPointDecoration(point, d);
            });
    }

    /**
     * Add sacred geometry decoration to point
     */
    addPointDecoration(point, data) {
        const radius = this.scales.size(data.value || 1);
        const x = this.scales.x(data.x);
        const y = this.scales.y(data.y);

        // Add hexagonal pattern
        const hexPoints = [];
        for (let i = 0; i < 6; i++) {
            const angle = (i * Math.PI) / 3;
            hexPoints.push([
                x + radius * 1.5 * Math.cos(angle),
                y + radius * 1.5 * Math.sin(angle)
            ]);
        }

        point.append('path')
            .attr('d', d3.line()(hexPoints))
            .attr('fill', 'none')
            .attr('stroke', this.scales.color(data.category))
            .attr('stroke-width', 0.5)
            .attr('opacity', 0.3);
    }

    /**
     * Animate chart elements
     */
    animateChart() {
        this.pointsGroup.selectAll('.sacred-point')
            .style('opacity', 0)
            .attr('transform', 'scale(0)')
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .delay((d, i) => i * SACRED_CONSTANTS.TIMING.DELAY)
            .style('opacity', 1)
            .attr('transform', 'scale(1)');
    }

    /**
     * Setup chart interactions
     */
    setupInteractions() {
        this.pointsGroup.selectAll('.sacred-point')
            .on('mouseenter', (event, d) => {
                const point = d3.select(event.currentTarget);
                
                point.select('circle')
                    .transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('r', r => r * SACRED_CONSTANTS.MATH.PHI)
                    .style('opacity', 1);

                point.select('path')
                    .transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .style('opacity', 0.6);

                this.showTooltip(event, d);
            })
            .on('mouseleave', (event) => {
                const point = d3.select(event.currentTarget);
                
                point.select('circle')
                    .transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .attr('r', d => this.scales.size(d.value || 1))
                    .style('opacity', 0.8);

                point.select('path')
                    .transition()
                    .duration(SACRED_CONSTANTS.TIMING.HOVER)
                    .style('opacity', 0.3);

                this.hideTooltip();
            });
    }
}
/**
 * Sacred Chart Zoom Controller
 * Based on sacred geometry and divine proportions
 */
class SacredZoomController {
    constructor(chart) {
        this.chart = chart;
        this.zoomBehavior = null;
        this.zoomExtent = [1, SACRED_CONSTANTS.MATH.PHI.SQUARED];
        this.currentScale = 1;
        this.initialize();
    }

    /**
     * Initialize zoom controller
     */
    initialize() {
        this.zoomBehavior = d3.zoom()
            .scaleExtent(this.zoomExtent)
            .on('zoom', this.handleZoom.bind(this))
            .on('start', this.handleZoomStart.bind(this))
            .on('end', this.handleZoomEnd.bind(this));

        this.chart.svg.call(this.zoomBehavior);
        this.setupZoomControls();
    }

    /**
     * Setup zoom control buttons
     */
    setupZoomControls() {
        const controlGroup = this.chart.svg.append('g')
            .attr('class', 'sacred-zoom-controls')
            .attr('transform', `translate(${this.chart.dimensions.innerWidth - 60}, 20)`);

        // Zoom In button
        controlGroup.append('rect')
            .attr('class', 'sacred-zoom-button sacred-zoom-in')
            .attr('x', 30)
            .attr('width', 24)
            .attr('height', 24)
            .attr('rx', 4)
            .on('click', () => this.zoomByStep(1));

        // Zoom Out button
        controlGroup.append('rect')
            .attr('class', 'sacred-zoom-button sacred-zoom-out')
            .attr('x', 0)
            .attr('width', 24)
            .attr('height', 24)
            .attr('rx', 4)
            .on('click', () => this.zoomByStep(-1));

        // Add icons
        this.addZoomIcons(controlGroup);
    }

    /**
     * Add zoom control icons
     */
    addZoomIcons(group) {
        // Zoom In icon
        group.append('path')
            .attr('class', 'sacred-zoom-icon')
            .attr('d', 'M38,13h-6V7c0-0.6-0.4-1-1-1s-1,0.4-1,1v6h-6c-0.6,0-1,0.4-1,1s0.4,1,1,1h6v6c0,0.6,0.4,1,1,1s1-0.4,1-1v-6h6c0.6,0,1-0.4,1-1S38.6,13,38,13z')
            .attr('transform', 'translate(30, 0) scale(0.5)');

        // Zoom Out icon
        group.append('path')
            .attr('class', 'sacred-zoom-icon')
            .attr('d', 'M8,13h12c0.6,0,1,0.4,1,1s-0.4,1-1,1H8c-0.6,0-1-0.4-1-1S7.4,13,8,13z')
            .attr('transform', 'translate(0, 0) scale(0.5)');
    }

    /**
     * Handle zoom event
     */
    handleZoom(event) {
        const { transform } = event;
        this.currentScale = transform.k;

        // Transform chart content
        this.chart.contentGroup.attr('transform', transform);

        // Update axes if needed
        if (this.chart.xAxis) {
            this.chart.xAxis.call(
                d3.axisBottom(this.chart.scales.x.scale(transform))
            );
        }
        if (this.chart.yAxis) {
            this.chart.yAxis.call(
                d3.axisLeft(this.chart.scales.y.scale(transform))
            );
        }

        // Emit zoom event
        if (this.chart.options.onZoom) {
            this.chart.options.onZoom({
                scale: transform.k,
                x: transform.x,
                y: transform.y
            });
        }
    }

    /**
     * Handle zoom start
     */
    handleZoomStart() {
        this.chart.svg.classed('sacred-zooming', true);
        
        if (this.chart.tooltip) {
            this.chart.tooltip.style('display', 'none');
        }
    }

    /**
     * Handle zoom end
     */
    handleZoomEnd() {
        this.chart.svg.classed('sacred-zooming', false);
        
        if (this.chart.tooltip) {
            this.chart.tooltip.style('display', null);
        }
    }

    /**
     * Zoom by step
     */
    zoomByStep(direction) {
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;
        const newScale = this.currentScale * (direction > 0 ? phi : 1/phi);

        this.zoomTo(newScale);
    }

    /**
     * Zoom to specific scale
     */
    zoomTo(scale) {
        this.chart.svg.transition()
            .duration(SACRED_CONSTANTS.TIMING.NORMAL)
            .call(
                this.zoomBehavior.transform,
                d3.zoomIdentity.scale(
                    Math.max(
                        this.zoomExtent[0],
                        Math.min(this.zoomExtent[1], scale)
                    )
                )
            );
    }

    /**
     * Reset zoom
     */
    reset() {
        this.chart.svg.transition()
            .duration(SACRED_CONSTANTS.TIMING.NORMAL)
            .call(this.zoomBehavior.transform, d3.zoomIdentity);
    }

    /**
     * Enable/disable zoom
     */
    setEnabled(enabled) {
        if (enabled) {
            this.chart.svg.call(this.zoomBehavior);
        } else {
            this.chart.svg.on('.zoom', null);
        }
    }
}
/**
 * Sacred Chart Pan Controller
 * Based on sacred geometry and divine proportions
 */
class SacredPanController {
    constructor(chart) {
        this.chart = chart;
        this.panBehavior = null;
        this.isPanning = false;
        this.startPosition = { x: 0, y: 0 };
        this.currentPosition = { x: 0, y: 0 };
        this.initialize();
    }

    /**
     * Initialize pan controller
     */
    initialize() {
        this.panBehavior = d3.drag()
            .on('start', this.handlePanStart.bind(this))
            .on('drag', this.handlePan.bind(this))
            .on('end', this.handlePanEnd.bind(this));

        this.chart.svg.call(this.panBehavior);
        this.setupPanBoundaries();
    }

    /**
     * Setup pan boundaries using sacred proportions
     */
    setupPanBoundaries() {
        const { innerWidth, innerHeight } = this.chart.dimensions;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        this.boundaries = {
            x: {
                min: -innerWidth * phi_inverse,
                max: innerWidth * phi_inverse
            },
            y: {
                min: -innerHeight * phi_inverse,
                max: innerHeight * phi_inverse
            }
        };
    }

    /**
     * Handle pan start
     */
    handlePanStart(event) {
        this.isPanning = true;
        this.chart.svg.classed('sacred-panning', true);
        
        this.startPosition = {
            x: this.currentPosition.x,
            y: this.currentPosition.y
        };

        if (this.chart.tooltip) {
            this.chart.tooltip.style('display', 'none');
        }
    }

    /**
     * Handle pan movement
     */
    handlePan(event) {
        if (!this.isPanning) return;

        const newX = this.startPosition.x + event.dx;
        const newY = this.startPosition.y + event.dy;

        // Apply boundaries with sacred proportions
        this.currentPosition = {
            x: this.clampToBoundaries(newX, 'x'),
            y: this.clampToBoundaries(newY, 'y')
        };

        this.applyTransform();
    }

    /**
     * Handle pan end
     */
    handlePanEnd() {
        this.isPanning = false;
        this.chart.svg.classed('sacred-panning', false);

        if (this.chart.tooltip) {
            this.chart.tooltip.style('display', null);
        }

        // Emit pan end event
        if (this.chart.options.onPanEnd) {
            this.chart.options.onPanEnd({
                x: this.currentPosition.x,
                y: this.currentPosition.y
            });
        }
    }

    /**
     * Clamp value to boundaries
     */
    clampToBoundaries(value, axis) {
        const { min, max } = this.boundaries[axis];
        return Math.max(min, Math.min(max, value));
    }

    /**
     * Apply transform to chart content
     */
    applyTransform() {
        const transform = d3.zoomTransform(this.chart.svg.node());
        const newTransform = d3.zoomIdentity
            .translate(this.currentPosition.x, this.currentPosition.y)
            .scale(transform.k);

        this.chart.contentGroup.attr('transform', newTransform);

        // Update axes if needed
        if (this.chart.xAxis) {
            this.chart.xAxis.call(
                d3.axisBottom(this.chart.scales.x.scale(newTransform))
            );
        }
        if (this.chart.yAxis) {
            this.chart.yAxis.call(
                d3.axisLeft(this.chart.scales.y.scale(newTransform))
            );
        }

        // Emit pan event
        if (this.chart.options.onPan) {
            this.chart.options.onPan({
                x: this.currentPosition.x,
                y: this.currentPosition.y,
                transform: newTransform
            });
        }
    }

    /**
     * Pan to specific position
     */
    panTo(x, y, duration = SACRED_CONSTANTS.TIMING.NORMAL) {
        const targetX = this.clampToBoundaries(x, 'x');
        const targetY = this.clampToBoundaries(y, 'y');

        this.chart.contentGroup
            .transition()
            .duration(duration)
            .ease(d3.easeCubicInOut)
            .attr('transform', `translate(${targetX},${targetY})`);

        this.currentPosition = { x: targetX, y: targetY };
    }

    /**
     * Reset pan position
     */
    reset(duration = SACRED_CONSTANTS.TIMING.NORMAL) {
        this.panTo(0, 0, duration);
    }

    /**
     * Enable/disable pan
     */
    setEnabled(enabled) {
        if (enabled) {
            this.chart.svg.call(this.panBehavior);
        } else {
            this.chart.svg.on('.drag', null);
        }
    }
}
/**
 * Sacred Chart Data Labels Component
 * Based on sacred geometry and divine proportions
 */
class SacredDataLabels {
    constructor(chart) {
        this.chart = chart;
        this.labelsGroup = null;
        this.initialize();
    }

    /**
     * Initialize data labels
     */
    initialize() {
        this.labelsGroup = this.chart.svg.append('g')
            .attr('class', 'sacred-data-labels');

        if (this.chart.options.animated) {
            this.setupAnimations();
        }

        this.drawLabels();
    }

    /**
     * Draw data labels
     */
    drawLabels() {
        const labels = this.labelsGroup.selectAll('.sacred-data-label')
            .data(this.chart.data)
            .enter()
            .append('g')
            .attr('class', 'sacred-data-label')
            .attr('transform', d => this.calculatePosition(d));

        // Add label background
        labels.append('rect')
            .attr('class', 'sacred-label-background')
            .attr('rx', 'var(--border-radius-sm)')
            .attr('fill', 'var(--surface-primary)')
            .attr('opacity', 0.8);

        // Add label text
        labels.append('text')
            .attr('class', 'sacred-label-text')
            .attr('dy', '0.32em')
            .attr('text-anchor', 'middle')
            .style('font-size', 'var(--chart-label-size)')
            .style('fill', 'var(--chart-label-color)')
            .text(d => this.formatLabel(d));

        // Adjust background size to text
        labels.each(function() {
            const text = d3.select(this).select('text');
            const bbox = text.node().getBBox();
            const padding = SACRED_CONSTANTS.MATH.PHI_INVERSE * 8;

            d3.select(this).select('rect')
                .attr('x', bbox.x - padding)
                .attr('y', bbox.y - padding)
                .attr('width', bbox.width + (padding * 2))
                .attr('height', bbox.height + (padding * 2));
        });
    }

    /**
     * Calculate label position
     */
    calculatePosition(d) {
        const x = this.chart.scales.x(d.x || d.label);
        const y = this.chart.scales.y(d.y || d.value);
        const offset = SACRED_CONSTANTS.MATH.PHI_INVERSE * 20;

        return `translate(${x},${y - offset})`;
    }

    /**
     * Format label text
     */
    formatLabel(d) {
        if (typeof d.label === 'string') {
            return d.label;
        }
        return d3.format(this.chart.options.labelFormat || ',.2f')(d.value);
    }

    /**
     * Setup label animations
     */
    setupAnimations() {
        this.labelsGroup.selectAll('.sacred-data-label')
            .style('opacity', 0)
            .attr('transform', d => {
                const [x, y] = this.calculatePosition(d).split(',');
                return `translate(${x},${parseFloat(y) + 20})`;
            })
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.DRAW)
            .delay((d, i) => i * SACRED_CONSTANTS.TIMING.DELAY)
            .style('opacity', 1)
            .attr('transform', d => this.calculatePosition(d));
    }

    /**
     * Update labels
     */
    update() {
        this.labelsGroup.selectAll('.sacred-data-label')
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.NORMAL)
            .attr('transform', d => this.calculatePosition(d))
            .select('text')
            .text(d => this.formatLabel(d));
    }

    /**
     * Show/hide specific labels
     */
    toggleLabels(indices, visible) {
        this.labelsGroup.selectAll('.sacred-data-label')
            .filter((d, i) => indices.includes(i))
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.QUICK)
            .style('opacity', visible ? 1 : 0);
    }
}
/**
 * Sacred Chart Crosshair Component
 * Based on sacred geometry and divine proportions
 */
class SacredCrosshair {
    constructor(chart) {
        this.chart = chart;
        this.crosshairGroup = null;
        this.verticalLine = null;
        this.horizontalLine = null;
        this.coordinates = null;
        this.initialize();
    }

    /**
     * Initialize crosshair
     */
    initialize() {
        this.crosshairGroup = this.chart.svg.append('g')
            .attr('class', 'sacred-crosshair')
            .style('opacity', 0)
            .style('pointer-events', 'none');

        // Create vertical line
        this.verticalLine = this.crosshairGroup.append('line')
            .attr('class', 'sacred-crosshair-line sacred-crosshair-vertical')
            .attr('y1', 0)
            .attr('y2', this.chart.dimensions.innerHeight)
            .style('stroke', 'var(--chart-crosshair-color)')
            .style('stroke-width', 'var(--chart-crosshair-width)')
            .style('stroke-dasharray', '3,3');

        // Create horizontal line
        this.horizontalLine = this.crosshairGroup.append('line')
            .attr('class', 'sacred-crosshair-line sacred-crosshair-horizontal')
            .attr('x1', 0)
            .attr('x2', this.chart.dimensions.innerWidth)
            .style('stroke', 'var(--chart-crosshair-color)')
            .style('stroke-width', 'var(--chart-crosshair-width)')
            .style('stroke-dasharray', '3,3');

        // Create coordinates label
        this.coordinates = this.crosshairGroup.append('text')
            .attr('class', 'sacred-crosshair-coordinates')
            .style('font-size', 'var(--chart-label-size)')
            .style('fill', 'var(--chart-label-color)');

        this.setupEventListeners();
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        this.chart.svg
            .on('mouseenter', () => this.show())
            .on('mouseleave', () => this.hide())
            .on('mousemove', (event) => this.updatePosition(event));
    }

    /**
     * Show crosshair
     */
    show() {
        this.crosshairGroup
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.HOVER)
            .style('opacity', 1);
    }

    /**
     * Hide crosshair
     */
    hide() {
        this.crosshairGroup
            .transition()
            .duration(SACRED_CONSTANTS.TIMING.HOVER)
            .style('opacity', 0);
    }

    /**
     * Update crosshair position
     */
    updatePosition(event) {
        const [x, y] = d3.pointer(event);
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        // Update lines
        this.verticalLine.attr('x1', x).attr('x2', x);
        this.horizontalLine.attr('y1', y).attr('y2', y);

        // Calculate coordinates
        const xValue = this.chart.scales.x.invert(x);
        const yValue = this.chart.scales.y.invert(y);

        // Update coordinates label
        this.coordinates
            .attr('x', x + 10)
            .attr('y', y - 10)
            .text(`(${this.formatValue(xValue)}, ${this.formatValue(yValue)})`)
            .call(this.wrapCoordinates.bind(this));

        // Add sacred geometry decoration
        this.updateDecoration(x, y);
    }

    /**
     * Format coordinate values
     */
    formatValue(value) {
        return d3.format('.2f')(value);
    }

    /**
     * Wrap coordinates within chart bounds
     */
    wrapCoordinates(selection) {
        const { innerWidth, innerHeight } = this.chart.dimensions;
        const bbox = selection.node().getBBox();
        const x = parseFloat(selection.attr('x'));
        const y = parseFloat(selection.attr('y'));

        if (x + bbox.width > innerWidth) {
            selection.attr('x', x - bbox.width - 20);
        }
        if (y - bbox.height < 0) {
            selection.attr('y', y + bbox.height);
        }
    }

    /**
     * Update sacred geometry decoration
     */
    updateDecoration(x, y) {
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;
        const radius = 4;

        // Remove previous decoration
        this.crosshairGroup.selectAll('.sacred-crosshair-decoration').remove();

        // Add sacred geometry pattern
        this.crosshairGroup.append('circle')
            .attr('class', 'sacred-crosshair-decoration')
            .attr('cx', x)
            .attr('cy', y)
            .attr('r', radius)
            .style('fill', 'var(--chart-crosshair-color)')
            .style('opacity', 0.5);

        // Add golden spiral guide
        const spiralPoints = this.generateSpiralPoints(x, y, radius * phi);
        const spiralLine = d3.line()
            .x(d => d.x)
            .y(d => d.y)
            .curve(d3.curveCardinal.tension(SACRED_CONSTANTS.MATH.PHI_INVERSE));

        this.crosshairGroup.append('path')
            .attr('class', 'sacred-crosshair-decoration')
            .attr('d', spiralLine(spiralPoints))
            .style('fill', 'none')
            .style('stroke', 'var(--chart-crosshair-color)')
            .style('opacity', 0.2);
    }

    /**
     * Generate golden spiral points
     */
    generateSpiralPoints(centerX, centerY, radius) {
        const points = [];
        const steps = 20;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        for (let i = 0; i < steps; i++) {
            const angle = i * SACRED_CONSTANTS.MATH.ANGLES.GOLDEN * Math.PI / 180;
            const r = radius * Math.pow(phi, -angle / (2 * Math.PI));
            points.push({
                x: centerX + r * Math.cos(angle),
                y: centerY + r * Math.sin(angle)
            });
        }

        return points;
    }
}
/**
 * Sacred Chart Export System
 * Based on sacred geometry and divine proportions
 */
class SacredExportSystem {
    constructor(chart) {
        this.chart = chart;
        this.exportFormats = {
            PNG: 'image/png',
            JPEG: 'image/jpeg',
            SVG: 'image/svg+xml',
            PDF: 'application/pdf'
        };
        this.initialize();
    }

    /**
     * Initialize export system
     */
    initialize() {
        this.setupExportControls();
    }

    /**
     * Setup export control buttons
     */
    setupExportControls() {
        const controlGroup = this.chart.svg.append('g')
            .attr('class', 'sacred-export-controls')
            .attr('transform', `translate(${this.chart.dimensions.innerWidth - 40}, 20)`);

        // Export button
        const exportButton = controlGroup.append('rect')
            .attr('class', 'sacred-export-button')
            .attr('width', 24)
            .attr('height', 24)
            .attr('rx', 4)
            .style('cursor', 'pointer')
            .on('click', () => this.showExportMenu());

        // Add icon
        controlGroup.append('path')
            .attr('class', 'sacred-export-icon')
            .attr('d', this.getExportIconPath())
            .attr('transform', 'translate(4, 4)');
    }

    /**
     * Export chart as image
     */
    async exportImage(format = 'PNG') {
        const svgData = this.getSVGData();
        const mimeType = this.exportFormats[format];

        if (format === 'SVG') {
            this.downloadFile(svgData, 'sacred-chart.svg', mimeType);
            return;
        }

        const imageData = await this.convertSVGToImage(svgData, mimeType);
        this.downloadFile(imageData, `sacred-chart.${format.toLowerCase()}`, mimeType);
    }

    /**
     * Get SVG data
     */
    getSVGData() {
        const svgNode = this.chart.svg.node();
        const serializer = new XMLSerializer();
        const svgString = serializer.serializeToString(svgNode);
        
        return 'data:image/svg+xml;base64,' + btoa(svgString);
    }

    /**
     * Convert SVG to image
     */
    convertSVGToImage(svgData, mimeType) {
        return new Promise((resolve, reject) => {
            const image = new Image();
            image.onload = () => {
                const canvas = document.createElement('canvas');
                const scale = window.devicePixelRatio || 1;
                canvas.width = this.chart.dimensions.width * scale;
                canvas.height = this.chart.dimensions.height * scale;

                const context = canvas.getContext('2d');
                context.scale(scale, scale);
                context.drawImage(image, 0, 0);

                resolve(canvas.toDataURL(mimeType));
            };
            image.onerror = reject;
            image.src = svgData;
        });
    }

    /**
     * Download file
     */
    downloadFile(data, filename, mimeType) {
        const link = document.createElement('a');
        link.download = filename;
        link.href = data;
        link.type = mimeType;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    /**
     * Show export menu
     */
    showExportMenu() {
        const menu = this.chart.svg.append('g')
            .attr('class', 'sacred-export-menu')
            .attr('transform', `translate(${this.chart.dimensions.innerWidth - 120}, 50)`);

        const formats = Object.keys(this.exportFormats);
        const itemHeight = 30;

        // Menu background
        menu.append('rect')
            .attr('width', 100)
            .attr('height', formats.length * itemHeight)
            .attr('rx', 4)
            .attr('fill', 'var(--surface-primary)')
            .attr('opacity', 0.9);

        // Menu items
        formats.forEach((format, i) => {
            const item = menu.append('g')
                .attr('class', 'sacred-export-menu-item')
                .attr('transform', `translate(0, ${i * itemHeight})`)
                .style('cursor', 'pointer')
                .on('click', () => {
                    this.exportImage(format);
                    menu.remove();
                });

            item.append('text')
                .attr('x', 10)
                .attr('y', 20)
                .text(format)
                .style('font-size', 'var(--chart-label-size)')
                .style('fill', 'var(--chart-label-color)');
        });

        // Close menu on outside click
        d3.select('body').on('click.export-menu', (event) => {
            if (!event.target.closest('.sacred-export-menu')) {
                menu.remove();
                d3.select('body').on('click.export-menu', null);
            }
        });
    }
}
/**
 * Sacred Chart Annotations Component
 * Based on sacred geometry and divine proportions
 */
class SacredAnnotations {
    constructor(chart) {
        this.chart = chart;
        this.annotationGroup = null;
        this.annotations = new Map();
        this.initialize();
    }

    /**
     * Initialize annotations system
     */
    initialize() {
        this.annotationGroup = this.chart.svg.append('g')
            .attr('class', 'sacred-annotations')
            .style('pointer-events', 'none');
    }

    /**
     * Add annotation
     */
    add(config) {
        const id = `annotation-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        const annotation = this.createAnnotation(config, id);
        this.annotations.set(id, annotation);
        
        if (this.chart.options.animated) {
            this.animateAnnotation(annotation);
        }

        return id;
    }

    /**
     * Create annotation
     */
    createAnnotation(config, id) {
        const group = this.annotationGroup.append('g')
            .attr('class', 'sacred-annotation')
            .attr('id', id);

        // Add connector line
        const connector = group.append('path')
            .attr('class', 'sacred-annotation-connector')
            .attr('d', this.calculateConnectorPath(config))
            .style('fill', 'none')
            .style('stroke', 'var(--chart-annotation-color)')
            .style('stroke-width', 1)
            .style('stroke-dasharray', '3,3');

        // Add annotation box
        const box = group.append('rect')
            .attr('class', 'sacred-annotation-box')
            .attr('x', config.x)
            .attr('y', config.y)
            .attr('rx', 'var(--border-radius-sm)')
            .style('fill', 'var(--surface-primary)')
            .style('stroke', 'var(--chart-annotation-color)')
            .style('opacity', 0.9);

        // Add annotation text
        const text = group.append('text')
            .attr('class', 'sacred-annotation-text')
            .attr('x', config.x + 8)
            .attr('y', config.y + 16)
            .style('font-size', 'var(--chart-label-size)')
            .style('fill', 'var(--chart-label-color)')
            .text(config.text);

        // Adjust box size to text
        const textBBox = text.node().getBBox();
        box.attr('width', textBBox.width + 16)
            .attr('height', textBBox.height + 16);

        return { group, connector, box, text, config };
    }

    /**
     * Calculate connector path using golden ratio
     */
    calculateConnectorPath(config) {
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;
        const start = { x: config.targetX, y: config.targetY };
        const end = { x: config.x, y: config.y };
        
        const controlPoint = {
            x: start.x + (end.x - start.x) / phi,
            y: start.y + (end.y - start.y) / phi
        };

        return `M ${start.x},${start.y} 
                Q ${controlPoint.x},${controlPoint.y} 
                  ${end.x},${end.y}`;
    }

    /**
     * Animate annotation entrance
     */
    animateAnnotation(annotation) {
        const duration = SACRED_CONSTANTS.TIMING.DRAW;
        const phi = SACRED_CONSTANTS.MATH.PHI.VALUE;

        // Animate connector
        const connectorLength = annotation.connector.node().getTotalLength();
        annotation.connector
            .attr('stroke-dasharray', `${connectorLength} ${connectorLength}`)
            .attr('stroke-dashoffset', connectorLength)
            .transition()
            .duration(duration)
            .ease(d3.easeExpInOut)
            .attr('stroke-dashoffset', 0);

        // Animate box and text
        annotation.box
            .style('opacity', 0)
            .attr('transform', 'scale(0.8)')
            .transition()
            .duration(duration)
            .delay(duration / phi)
            .ease(d3.easeExpInOut)
            .style('opacity', 0.9)
            .attr('transform', 'scale(1)');

        annotation.text
            .style('opacity', 0)
            .transition()
            .duration(duration)
            .delay(duration / phi)
            .ease(d3.easeExpInOut)
            .style('opacity', 1);
    }

    /**
     * Update annotation positions
     */
    update() {
        this.annotations.forEach((annotation) => {
            annotation.connector
                .attr('d', this.calculateConnectorPath(annotation.config));
            
            annotation.box
                .attr('x', annotation.config.x)
                .attr('y', annotation.config.y);
            
            annotation.text
                .attr('x', annotation.config.x + 8)
                .attr('y', annotation.config.y + 16);
        });
    }

    /**
     * Remove annotation
     */
    remove(id) {
        const annotation = this.annotations.get(id);
        if (annotation) {
            annotation.group.remove();
            this.annotations.delete(id);
        }
    }

    /**
     * Clear all annotations
     */
    clear() {
        this.annotations.forEach((annotation) => {
            annotation.group.remove();
        });
        this.annotations.clear();
    }
}
