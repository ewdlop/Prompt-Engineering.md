# Functional Prompt Engineering

## Introduction

Functional programming provides powerful paradigms for creating, composing, and managing prompts. This document explores how functional programming concepts can be applied to prompt engineering.

## Core Functional Programming Concepts in Prompt Engineering

### 1. Pure Functions

Pure functions always produce the same output for the same input and have no side effects.

```python
# Pure function for prompt generation
def create_basic_prompt(task: str, context: str) -> str:
    """Pure function that creates a basic prompt"""
    return f"Task: {task}\nContext: {context}\nPlease provide a detailed response."

# Always produces the same output for the same inputs
prompt1 = create_basic_prompt("Explain AI", "Educational context")
prompt2 = create_basic_prompt("Explain AI", "Educational context")
assert prompt1 == prompt2  # True
```

### 2. Higher-Order Functions

Functions that take other functions as arguments or return functions.

```python
from typing import Callable

def prompt_transformer(prompt: str, transformer: Callable[[str], str]) -> str:
    """Higher-order function that transforms prompts"""
    return transformer(prompt)

# Define transformers
def add_formality(prompt: str) -> str:
    return f"Respectfully, {prompt}"

def add_urgency(prompt: str) -> str:
    return f"URGENT: {prompt}"

# Use higher-order function
base_prompt = "Please review this document"
formal_prompt = prompt_transformer(base_prompt, add_formality)
urgent_prompt = prompt_transformer(base_prompt, add_urgency)
```

### 3. Function Composition

Combining simple functions to create more complex ones.

```python
from functools import reduce
from typing import List, Callable

def compose(*functions: Callable) -> Callable:
    """Compose multiple functions into one"""
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def add_greeting(text: str) -> str:
    return f"Hello! {text}"

def add_context(text: str) -> str:
    return f"{text}\nContext: AI Assistant"

def add_closing(text: str) -> str:
    return f"{text}\nThank you!"

# Compose all transformations
full_prompt_builder = compose(add_closing, add_context, add_greeting)
result = full_prompt_builder("Please help me with my task")
```

### 4. Immutability

Data structures that cannot be modified after creation.

```python
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Prompt:
    """Immutable prompt structure"""
    task: str
    context: str
    constraints: Tuple[str, ...]
    
    def with_task(self, new_task: str) -> 'Prompt':
        """Return new Prompt with updated task"""
        return Prompt(new_task, self.context, self.constraints)
    
    def add_constraint(self, constraint: str) -> 'Prompt':
        """Return new Prompt with additional constraint"""
        return Prompt(self.task, self.context, self.constraints + (constraint,))

# Usage
original = Prompt("Analyze data", "Scientific research", ("Be precise", "Use citations"))
modified = original.add_constraint("Include visualizations")
# original remains unchanged
```

### 5. Map, Filter, and Reduce

Functional operations for transforming collections.

```python
from functools import reduce
from typing import List

# Map: Transform each prompt in a collection
prompts = ["explain AI", "describe ML", "define NLP"]
capitalized = list(map(str.upper, prompts))

# Filter: Select prompts meeting criteria
def is_short(prompt: str) -> bool:
    return len(prompt) < 15

short_prompts = list(filter(is_short, prompts))

# Reduce: Combine prompts into one
def combine_prompts(acc: str, prompt: str) -> str:
    return f"{acc}\n- {prompt}"

combined = reduce(combine_prompts, prompts, "Multi-task prompt:")
```

## Functional Prompt Patterns

### Pattern 1: Prompt Pipeline

```python
from typing import List, Callable

class PromptPipeline:
    """Functional pipeline for prompt processing"""
    
    def __init__(self, initial_prompt: str):
        self.prompt = initial_prompt
    
    def pipe(self, *operations: Callable[[str], str]) -> 'PromptPipeline':
        """Apply a series of operations to the prompt"""
        for operation in operations:
            self.prompt = operation(self.prompt)
        return self
    
    def build(self) -> str:
        """Return the final prompt"""
        return self.prompt

# Usage
def add_role(prompt: str) -> str:
    return f"As an expert, {prompt}"

def add_format(prompt: str) -> str:
    return f"{prompt}\nFormat: Markdown"

final_prompt = (PromptPipeline("explain quantum computing")
                .pipe(add_role, add_format)
                .build())
```

### Pattern 2: Prompt Factory

```python
from typing import Dict, Any

def create_prompt_factory(template: str):
    """Factory function that returns a prompt generator"""
    def generate_prompt(**kwargs: Any) -> str:
        return template.format(**kwargs)
    return generate_prompt

# Create specialized factories
question_factory = create_prompt_factory(
    "Question: {question}\nContext: {context}\nPlease provide a {style} answer."
)

# Generate prompts
prompt1 = question_factory(
    question="What is AI?",
    context="Educational",
    style="detailed"
)

prompt2 = question_factory(
    question="How does ML work?",
    context="Technical",
    style="concise"
)
```

### Pattern 3: Currying

```python
from typing import Callable

def curried_prompt_builder(task: str) -> Callable[[str], Callable[[str], str]]:
    """Curried function for building prompts step by step"""
    def with_context(context: str) -> Callable[[str], str]:
        def with_style(style: str) -> str:
            return f"Task: {task}\nContext: {context}\nStyle: {style}"
        return with_style
    return with_context

# Usage
build_ai_prompt = curried_prompt_builder("Explain AI")
build_ai_educational = build_ai_prompt("Educational")
detailed_prompt = build_ai_educational("Detailed")
concise_prompt = build_ai_educational("Concise")
```

## JavaScript Examples

```javascript
// Pure function
const createPrompt = (task, context) => 
    `Task: ${task}\nContext: ${context}`;

// Higher-order function
const withTransformation = (prompt, transformer) => 
    transformer(prompt);

// Function composition
const compose = (...fns) => 
    fns.reduce((f, g) => (...args) => f(g(...args)));

const addGreeting = text => `Hello! ${text}`;
const addContext = text => `${text}\nContext: AI`;
const addClosing = text => `${text}\nThank you!`;

const buildPrompt = compose(addClosing, addContext, addGreeting);
const result = buildPrompt("Please help me");

// Map/Filter/Reduce
const prompts = ["explain AI", "describe ML", "define NLP"];

const capitalized = prompts.map(p => p.toUpperCase());
const short = prompts.filter(p => p.length < 15);
const combined = prompts.reduce((acc, p) => `${acc}\n- ${p}`, "Tasks:");
```

## Haskell-Style Examples

```haskell
-- Type definitions
data Prompt = Prompt 
    { task :: String
    , context :: String
    , constraints :: [String]
    } deriving (Show)

-- Pure function
createPrompt :: String -> String -> Prompt
createPrompt t c = Prompt t c []

-- Function composition
addConstraint :: String -> Prompt -> Prompt
addConstraint constraint prompt = 
    prompt { constraints = constraints prompt ++ [constraint] }

-- Functor mapping
instance Functor PromptWrapper where
    fmap f (PromptWrapper p) = PromptWrapper (f p)

-- Applicative for combining prompts
instance Applicative PromptWrapper where
    pure = PromptWrapper
    (PromptWrapper f) <*> (PromptWrapper x) = PromptWrapper (f x)

-- Monadic composition
instance Monad PromptWrapper where
    return = pure
    (PromptWrapper p) >>= f = f p
```

## Scala Examples

```scala
// Pure function
def createPrompt(task: String, context: String): String =
  s"Task: $task\nContext: $context"

// Higher-order function
def transformPrompt(prompt: String)(transformer: String => String): String =
  transformer(prompt)

// Function composition
val addGreeting: String => String = text => s"Hello! $text"
val addContext: String => String = text => s"$text\nContext: AI"
val addClosing: String => String = text => s"$text\nThank you!"

val buildPrompt = addGreeting andThen addContext andThen addClosing

// Pattern matching
sealed trait PromptStyle
case object Formal extends PromptStyle
case object Casual extends PromptStyle

def stylePrompt(prompt: String, style: PromptStyle): String = style match {
  case Formal => s"Dear Sir/Madam, $prompt"
  case Casual => s"Hey! $prompt"
}

// For comprehension (monadic)
case class PromptBuilder(prompt: String) {
  def map(f: String => String): PromptBuilder = 
    PromptBuilder(f(prompt))
  
  def flatMap(f: String => PromptBuilder): PromptBuilder = 
    f(prompt)
}

val result = for {
  p1 <- PromptBuilder("explain AI")
  p2 <- p1.map(addGreeting)
  p3 <- p2.map(addContext)
} yield p3
```

## Benefits of Functional Approach

1. **Predictability**: Pure functions ensure consistent outputs
2. **Composability**: Small functions can be combined to create complex prompts
3. **Reusability**: Generic functions can be reused across different contexts
4. **Testability**: Pure functions are easy to test
5. **Maintainability**: Immutability and pure functions reduce bugs
6. **Parallelization**: Pure functions can be safely parallelized

## Advanced Patterns

### Monadic Prompt Composition

```python
from typing import TypeVar, Generic, Callable, Optional

T = TypeVar('T')
U = TypeVar('U')

class PromptMonad(Generic[T]):
    """Monad for composing prompt transformations"""
    
    def __init__(self, value: T):
        self.value = value
    
    def bind(self, func: Callable[[T], 'PromptMonad[U]']) -> 'PromptMonad[U]':
        """Monadic bind operation"""
        return func(self.value)
    
    def map(self, func: Callable[[T], U]) -> 'PromptMonad[U]':
        """Functor map operation"""
        return PromptMonad(func(self.value))
    
    @staticmethod
    def unit(value: T) -> 'PromptMonad[T]':
        """Wrap a value in the monad"""
        return PromptMonad(value)

# Usage
def add_prefix(text: str) -> PromptMonad[str]:
    return PromptMonad(f"Prompt: {text}")

def add_suffix(text: str) -> PromptMonad[str]:
    return PromptMonad(f"{text}\nEnd of prompt")

result = (PromptMonad("Hello World")
          .bind(add_prefix)
          .bind(add_suffix)
          .value)
```

### Lens Pattern for Prompt Modification

```python
from typing import Callable, TypeVar, Generic

T = TypeVar('T')
A = TypeVar('A')

class Lens(Generic[T, A]):
    """Lens for focusing on parts of a prompt structure"""
    
    def __init__(self, 
                 getter: Callable[[T], A],
                 setter: Callable[[T, A], T]):
        self.get = getter
        self.set = setter
    
    def modify(self, obj: T, func: Callable[[A], A]) -> T:
        """Modify the focused part"""
        return self.set(obj, func(self.get(obj)))

# Example with Prompt class
@dataclass(frozen=True)
class PromptData:
    task: str
    context: str
    temperature: float

# Define lenses
task_lens = Lens(
    getter=lambda p: p.task,
    setter=lambda p, t: PromptData(t, p.context, p.temperature)
)

temperature_lens = Lens(
    getter=lambda p: p.temperature,
    setter=lambda p, temp: PromptData(p.task, p.context, temp)
)

# Usage
original = PromptData("Explain AI", "Educational", 0.7)
modified = task_lens.modify(original, lambda t: t.upper())
warmer = temperature_lens.modify(original, lambda temp: temp + 0.1)
```

## Conclusion

Functional programming provides a powerful paradigm for prompt engineering, offering:
- Clear, composable abstractions
- Predictable behavior through pure functions
- Elegant solutions through higher-order functions and composition
- Better maintainability through immutability

By applying these functional concepts, prompt engineers can create more robust, reusable, and maintainable prompt systems.

---

**Generated**: 2025-10-18
**Topics**: Functional Programming, Prompt Engineering, Pure Functions, Higher-Order Functions, Composition
