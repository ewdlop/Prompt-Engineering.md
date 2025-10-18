# Functional Prompt Engineering - Quick Reference

## Overview

This directory contains a comprehensive implementation of functional programming concepts applied to prompt engineering. The functional approach provides composable, reusable, and maintainable solutions for creating and managing AI prompts.

## Files

- **`functional-prompt.md`** - Complete guide to functional programming concepts in prompt engineering
- **`functional_prompt.py`** - Python implementation with functional utilities
- **`functional_prompt.js`** - JavaScript/Node.js implementation with functional utilities

## Key Concepts

### 1. Pure Functions
Functions that always return the same output for the same input with no side effects.

```python
# Python
prompt = create_basic_prompt("Explain AI", "Educational context")

# JavaScript
const prompt = createBasicPrompt('Explain AI', 'Educational context');
```

### 2. Function Composition
Combining simple functions to create complex ones.

```python
# Python
builder = compose(add_closing, add_formality, add_greeting)
result = builder("Help me understand ML")

# JavaScript
const builder = compose(addClosing, addFormality, addGreeting);
const result = builder('Help me understand ML');
```

### 3. Immutable Data Structures
Data that cannot be modified after creation.

```python
# Python
prompt = (Prompt("Analyze data", "Research")
          .add_constraint("Use scientific terminology")
          .with_role("Data Scientist"))

# JavaScript
const prompt = createPrompt({ task: 'Analyze data', context: 'Research' })
    .addConstraint('Use scientific terminology')
    .withRole('Data Scientist');
```

### 4. Higher-Order Functions
Functions that take or return other functions.

```python
# Python
add_role = add_role_instruction("professor")
transformed = prompt_transformer(base_prompt, add_role)

# JavaScript
const addRole = addRoleInstruction('professor');
const transformed = promptTransformer(basePrompt, addRole);
```

### 5. Pipeline Pattern
Chaining transformations in a readable way.

```python
# Python
result = (PromptPipeline("explain quantum computing")
          .pipe(add_role, add_context, add_politeness)
          .build())

# JavaScript
const result = createPipeline('explain quantum computing')
    .pipe(addRole, addContext, addPoliteness)
    .build();
```

## Quick Start

### Python

```bash
# Run examples
python3 functional_prompt.py

# Use in your code
from functional_prompt import create_basic_prompt, compose, Prompt

prompt = create_basic_prompt("My task", "My context")
```

### JavaScript

```bash
# Run examples
node functional_prompt.js

# Use in your code
const { createBasicPrompt, compose, createPrompt } = require('./functional_prompt');

const prompt = createBasicPrompt('My task', 'My context');
```

## Core Functions

### Python API

- `create_basic_prompt(task, context)` - Create a simple prompt
- `create_structured_prompt(role, task, constraints, format_style)` - Create structured prompt
- `compose(*functions)` - Compose functions
- `Prompt(task, context, constraints, role, temperature)` - Immutable prompt class
- `PromptPipeline(initial_prompt)` - Pipeline builder
- `PromptMonad(value)` - Monadic composition
- `curry_prompt_builder(task)` - Curried prompt builder
- `create_prompt_factory(template)` - Template-based factory

### JavaScript API

- `createBasicPrompt(task, context)` - Create a simple prompt
- `createStructuredPrompt(role, task, constraints, formatStyle)` - Create structured prompt
- `compose(...fns)` - Compose functions
- `createPrompt({task, context, constraints, role, temperature})` - Immutable prompt factory
- `createPipeline(initialPrompt)` - Pipeline builder
- `PromptMonad(value)` - Monadic composition
- `curryPromptBuilder(task)` - Curried prompt builder
- `createPromptFactory(template)` - Template-based factory

## Examples

### Example 1: Simple Prompt
```python
prompt = create_basic_prompt(
    "Explain machine learning",
    "Educational context for beginners"
)
```

### Example 2: Composed Transformations
```python
transform = compose(
    add_closing,
    add_formality,
    add_greeting
)
result = transform("Please help me")
```

### Example 3: Immutable Prompt Building
```python
prompt = (Prompt("Analyze data", "Research project")
          .add_constraint("Use scientific terminology")
          .add_constraint("Cite sources")
          .with_role("Data Scientist")
          .with_temperature(0.5))
```

### Example 4: Pipeline
```python
result = (PromptPipeline("explain quantum computing")
          .pipe(
              add_role_instruction("physics professor"),
              add_context_marker("undergraduate lecture"),
              add_politeness
          )
          .build())
```

### Example 5: Factory Pattern
```python
qa_factory = create_prompt_factory(
    "Question: {question}\nDomain: {domain}\nStyle: {style}"
)

prompt = qa_factory(
    question="How does neural networks work?",
    domain="Machine Learning",
    style="Technical"
)
```

## Benefits

1. **Predictability** - Pure functions always produce the same output
2. **Composability** - Small functions combine to create complex behavior
3. **Reusability** - Generic functions work across contexts
4. **Testability** - Pure functions are easy to test
5. **Maintainability** - Immutability reduces bugs
6. **Clarity** - Declarative style is easier to understand

## Resources

- **Full Documentation**: See `functional-prompt.md` for comprehensive guide
- **Python Implementation**: `functional_prompt.py` with complete examples
- **JavaScript Implementation**: `functional_prompt.js` with complete examples

## Contributing

When adding new functional utilities:
1. Ensure functions are pure (no side effects)
2. Make data structures immutable
3. Provide both Python and JavaScript implementations
4. Add examples demonstrating usage
5. Update this README with new functions

---

**Last Updated**: 2025-10-18  
**Topics**: Functional Programming, Prompt Engineering, Python, JavaScript
