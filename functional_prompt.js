/**
 * Functional Prompt Engineering Library (JavaScript)
 * 
 * This module provides functional programming utilities for creating,
 * composing, and managing prompts in a pure functional style.
 */

// ============================================================================
// Pure Functions for Prompt Generation
// ============================================================================

/**
 * Pure function that creates a basic prompt
 * @param {string} task - The task description
 * @param {string} context - The context for the task
 * @returns {string} A formatted prompt string
 */
const createBasicPrompt = (task, context) =>
    `Task: ${task}\nContext: ${context}\nPlease provide a detailed response.`;

/**
 * Pure function that creates a structured prompt
 * @param {string} role - The role for the AI to assume
 * @param {string} task - The task description
 * @param {string[]} constraints - List of constraints
 * @param {string} formatStyle - The desired output format
 * @returns {string} A structured prompt string
 */
const createStructuredPrompt = (role, task, constraints, formatStyle = 'markdown') => {
    const constraintsText = constraints.map(c => `- ${c}`).join('\n');
    return `Role: ${role}

Task: ${task}

Constraints:
${constraintsText}

Output Format: ${formatStyle}`;
};

// ============================================================================
// Higher-Order Functions
// ============================================================================

/**
 * Higher-order function that applies a transformation to a prompt
 * @param {string} prompt - The input prompt
 * @param {Function} transformer - Function to transform the prompt
 * @returns {string} The transformed prompt
 */
const promptTransformer = (prompt, transformer) => transformer(prompt);

/**
 * Factory function that creates a prompt modifier
 * @param {string} prefix - Text to add before the prompt
 * @param {string} suffix - Text to add after the prompt
 * @returns {Function} A function that modifies prompts
 */
const createPromptModifier = (prefix, suffix) => 
    prompt => `${prefix}${prompt}${suffix}`;

/**
 * Compose multiple functions into a single function
 * @param {...Function} fns - Functions to compose (applied right to left)
 * @returns {Function} A composed function
 */
const compose = (...fns) => 
    fns.reduce((f, g) => (...args) => f(g(...args)));

/**
 * Pipe functions (compose in left-to-right order)
 * @param {...Function} fns - Functions to pipe
 * @returns {Function} A piped function
 */
const pipe = (...fns) => 
    fns.reduce((f, g) => (...args) => g(f(...args)));

// ============================================================================
// Transformation Functions
// ============================================================================

const addFormality = prompt => `Respectfully, ${prompt}`;

const addUrgency = prompt => `URGENT: ${prompt}`;

const addPoliteness = prompt => `Please ${prompt.toLowerCase()}\nThank you.`;

const addContextMarker = context => prompt => 
    `${prompt}\n\nContext: ${context}`;

const addRoleInstruction = role => prompt => 
    `You are a ${role}. ${prompt}`;

const addGreeting = text => `Hello! ${text}`;

const addClosing = text => `${text}\nThank you!`;

// ============================================================================
// Immutable Prompt Structure
// ============================================================================

/**
 * Create an immutable prompt object
 * @param {Object} config - Prompt configuration
 * @returns {Object} Immutable prompt with transformation methods
 */
const createPrompt = ({
    task,
    context,
    constraints = [],
    role = null,
    temperature = 0.7
}) => {
    // Return frozen object with transformation methods
    return Object.freeze({
        task,
        context,
        constraints: Object.freeze([...constraints]),
        role,
        temperature,
        
        withTask(newTask) {
            return createPrompt({
                ...this,
                task: newTask,
                constraints: [...this.constraints]
            });
        },
        
        withContext(newContext) {
            return createPrompt({
                ...this,
                context: newContext,
                constraints: [...this.constraints]
            });
        },
        
        addConstraint(constraint) {
            return createPrompt({
                ...this,
                constraints: [...this.constraints, constraint]
            });
        },
        
        withRole(newRole) {
            return createPrompt({
                ...this,
                role: newRole,
                constraints: [...this.constraints]
            });
        },
        
        withTemperature(temp) {
            return createPrompt({
                ...this,
                temperature: temp,
                constraints: [...this.constraints]
            });
        },
        
        toString() {
            const parts = [];
            
            if (this.role) {
                parts.push(`Role: ${this.role}`);
            }
            
            parts.push(`Task: ${this.task}`);
            parts.push(`Context: ${this.context}`);
            
            if (this.constraints.length > 0) {
                const constraintsText = this.constraints
                    .map(c => `- ${c}`)
                    .join('\n');
                parts.push(`Constraints:\n${constraintsText}`);
            }
            
            parts.push(`Temperature: ${this.temperature}`);
            
            return parts.join('\n\n');
        }
    });
};

// ============================================================================
// Functional Collections Operations
// ============================================================================

const mapPrompts = (prompts, func) => prompts.map(func);

const filterPrompts = (prompts, predicate) => prompts.filter(predicate);

const reducePrompts = (prompts, combiner, initial = '') => 
    prompts.reduce(combiner, initial);

// ============================================================================
// Prompt Pipeline
// ============================================================================

/**
 * Create a functional pipeline for prompt processing
 * @param {string} initialPrompt - The starting prompt
 * @returns {Object} Pipeline with pipe and build methods
 */
const createPipeline = (initialPrompt) => {
    let prompt = initialPrompt;
    
    return {
        pipe(...operations) {
            operations.forEach(operation => {
                prompt = operation(prompt);
            });
            return this;
        },
        
        build() {
            return prompt;
        }
    };
};

// ============================================================================
// Monadic Composition
// ============================================================================

/**
 * Create a PromptMonad for composing transformations
 * @param {*} value - Value to wrap in the monad
 * @returns {Object} Monad with bind, map, and unit operations
 */
const PromptMonad = value => ({
    value,
    
    // Monadic bind (flatMap)
    bind(func) {
        return func(this.value);
    },
    
    // Functor map
    map(func) {
        return PromptMonad(func(this.value));
    },
    
    // Static unit method
    unit: PromptMonad
});

// ============================================================================
// Currying
// ============================================================================

/**
 * Curried function for building prompts step by step
 * @param {string} task - The task description
 * @returns {Function} Curried function expecting context, then style
 */
const curryPromptBuilder = task => context => style =>
    `Task: ${task}\nContext: ${context}\nStyle: ${style}`;

/**
 * General curry function
 * @param {Function} fn - Function to curry
 * @returns {Function} Curried version of the function
 */
const curry = (fn) => {
    const arity = fn.length;
    
    return function curried(...args) {
        if (args.length >= arity) {
            return fn(...args);
        }
        
        return (...nextArgs) => curried(...args, ...nextArgs);
    };
};

// ============================================================================
// Prompt Factories
// ============================================================================

/**
 * Create a factory function for generating prompts from a template
 * @param {string} template - Template string
 * @returns {Function} Factory function
 */
const createPromptFactory = (template) => (values) => {
    return template.replace(/\{(\w+)\}/g, (match, key) => values[key] || match);
};

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Memoization for caching pure function results
 * @param {Function} fn - Function to memoize
 * @returns {Function} Memoized version of the function
 */
const memoize = (fn) => {
    const cache = new Map();
    
    return (...args) => {
        const key = JSON.stringify(args);
        
        if (cache.has(key)) {
            return cache.get(key);
        }
        
        const result = fn(...args);
        cache.set(key, result);
        return result;
    };
};

/**
 * Partial application of a function
 * @param {Function} fn - Function to partially apply
 * @param {...*} fixedArgs - Fixed arguments
 * @returns {Function} Partially applied function
 */
const partial = (fn, ...fixedArgs) => 
    (...remainingArgs) => fn(...fixedArgs, ...remainingArgs);

// ============================================================================
// Example Usage
// ============================================================================

const main = () => {
    console.log('='.repeat(80));
    console.log('Functional Prompt Engineering Examples (JavaScript)');
    console.log('='.repeat(80));
    
    // Example 1: Pure function
    console.log('\n1. Pure Function:');
    const prompt1 = createBasicPrompt('Explain AI', 'Educational context');
    console.log(prompt1);
    
    // Example 2: Function composition
    console.log('\n2. Function Composition:');
    const fullBuilder = compose(addClosing, addFormality, addGreeting);
    const prompt2 = fullBuilder('Please help me understand machine learning');
    console.log(prompt2);
    
    // Example 3: Immutable prompt
    console.log('\n3. Immutable Prompt Structure:');
    const prompt3 = createPrompt({
        task: 'Analyze data',
        context: 'Research project'
    })
        .addConstraint('Use scientific terminology')
        .addConstraint('Cite sources')
        .withRole('Data Scientist')
        .withTemperature(0.5);
    console.log(prompt3.toString());
    
    // Example 4: Pipeline
    console.log('\n4. Prompt Pipeline:');
    const prompt4 = createPipeline('explain quantum computing')
        .pipe(
            addRoleInstruction('physics professor'),
            addContextMarker('undergraduate lecture'),
            addPoliteness
        )
        .build();
    console.log(prompt4);
    
    // Example 5: Monadic composition
    console.log('\n5. Monadic Composition:');
    const wrapInMarkdown = text => PromptMonad(`\`\`\`\n${text}\n\`\`\``);
    const addTitle = text => PromptMonad(`# Prompt\n\n${text}`);
    
    const prompt5 = PromptMonad('What is machine learning?')
        .bind(wrapInMarkdown)
        .bind(addTitle)
        .value;
    console.log(prompt5);
    
    // Example 6: Map/Filter/Reduce
    console.log('\n6. Map/Filter/Reduce:');
    const prompts = ['explain AI', 'describe ML', 'define NLP', 'what is deep learning?'];
    
    // Map: capitalize
    const capitalized = mapPrompts(prompts, p => p.toUpperCase());
    console.log('Capitalized:', capitalized.slice(0, 2));
    
    // Filter: short prompts
    const short = filterPrompts(prompts, p => p.length < 15);
    console.log('Short prompts:', short);
    
    // Reduce: combine
    const combined = reducePrompts(
        prompts,
        (acc, p) => `${acc}\n- ${p}`,
        'Multi-task prompt:'
    );
    console.log(combined);
    
    // Example 7: Currying
    console.log('\n7. Currying:');
    const buildAiPrompt = curryPromptBuilder('Explain AI');
    const buildEducational = buildAiPrompt('Educational');
    const detailed = buildEducational('Detailed');
    console.log(detailed);
    
    // Example 8: Factory
    console.log('\n8. Prompt Factory:');
    const qaFactory = createPromptFactory(
        'Question: {question}\nDomain: {domain}\nStyle: {style}'
    );
    const prompt8 = qaFactory({
        question: 'How does neural networks work?',
        domain: 'Machine Learning',
        style: 'Technical'
    });
    console.log(prompt8);
};

// ============================================================================
// Exports
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        // Pure functions
        createBasicPrompt,
        createStructuredPrompt,
        
        // Higher-order functions
        promptTransformer,
        createPromptModifier,
        compose,
        pipe,
        
        // Transformations
        addFormality,
        addUrgency,
        addPoliteness,
        addContextMarker,
        addRoleInstruction,
        addGreeting,
        addClosing,
        
        // Immutable structure
        createPrompt,
        
        // Collections
        mapPrompts,
        filterPrompts,
        reducePrompts,
        
        // Pipeline
        createPipeline,
        
        // Monad
        PromptMonad,
        
        // Currying
        curryPromptBuilder,
        curry,
        
        // Factories
        createPromptFactory,
        
        // Utils
        memoize,
        partial
    };
}

// Run examples if executed directly
if (typeof require !== 'undefined' && require.main === module) {
    main();
}
