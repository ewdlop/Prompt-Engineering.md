#!/usr/bin/env python3
"""
Functional Prompt Engineering Library

This module provides functional programming utilities for creating,
composing, and managing prompts in a pure functional style.
"""

from typing import Callable, List, Tuple, Any, TypeVar, Generic, Optional
from functools import reduce, wraps
from dataclasses import dataclass, replace


T = TypeVar('T')
U = TypeVar('U')


# ============================================================================
# Pure Functions for Prompt Generation
# ============================================================================

def create_basic_prompt(task: str, context: str) -> str:
    """
    Pure function that creates a basic prompt.
    
    Args:
        task: The task description
        context: The context for the task
        
    Returns:
        A formatted prompt string
    """
    return f"Task: {task}\nContext: {context}\nPlease provide a detailed response."


def create_structured_prompt(
    role: str,
    task: str,
    constraints: List[str],
    format_style: str = "markdown"
) -> str:
    """
    Pure function that creates a structured prompt.
    
    Args:
        role: The role for the AI to assume
        task: The task description
        constraints: List of constraints
        format_style: The desired output format
        
    Returns:
        A structured prompt string
    """
    constraints_text = "\n".join(f"- {c}" for c in constraints)
    return f"""Role: {role}

Task: {task}

Constraints:
{constraints_text}

Output Format: {format_style}"""


# ============================================================================
# Higher-Order Functions
# ============================================================================

def prompt_transformer(
    prompt: str,
    transformer: Callable[[str], str]
) -> str:
    """
    Higher-order function that applies a transformation to a prompt.
    
    Args:
        prompt: The input prompt
        transformer: Function to transform the prompt
        
    Returns:
        The transformed prompt
    """
    return transformer(prompt)


def create_prompt_modifier(prefix: str, suffix: str) -> Callable[[str], str]:
    """
    Factory function that creates a prompt modifier.
    
    Args:
        prefix: Text to add before the prompt
        suffix: Text to add after the prompt
        
    Returns:
        A function that modifies prompts
    """
    def modifier(prompt: str) -> str:
        return f"{prefix}{prompt}{suffix}"
    return modifier


def compose(*functions: Callable) -> Callable:
    """
    Compose multiple functions into a single function.
    
    Args:
        *functions: Functions to compose (applied right to left)
        
    Returns:
        A composed function
    """
    def identity(x):
        return x
    
    return reduce(
        lambda f, g: lambda x: f(g(x)),
        functions,
        identity
    )


# ============================================================================
# Transformation Functions
# ============================================================================

def add_formality(prompt: str) -> str:
    """Add formal tone to a prompt."""
    return f"Respectfully, {prompt}"


def add_urgency(prompt: str) -> str:
    """Add urgency indicator to a prompt."""
    return f"URGENT: {prompt}"


def add_politeness(prompt: str) -> str:
    """Add polite phrasing to a prompt."""
    return f"Please {prompt.lower()}\nThank you."


def add_context_marker(context: str) -> Callable[[str], str]:
    """Create a function that adds context to prompts."""
    def add_context(prompt: str) -> str:
        return f"{prompt}\n\nContext: {context}"
    return add_context


def add_role_instruction(role: str) -> Callable[[str], str]:
    """Create a function that adds role instruction to prompts."""
    def add_role(prompt: str) -> str:
        return f"You are a {role}. {prompt}"
    return add_role


# ============================================================================
# Immutable Prompt Structure
# ============================================================================

@dataclass(frozen=True)
class Prompt:
    """
    Immutable prompt data structure.
    
    All modification methods return new Prompt instances.
    """
    task: str
    context: str
    constraints: Tuple[str, ...] = ()
    role: Optional[str] = None
    temperature: float = 0.7
    
    def with_task(self, new_task: str) -> 'Prompt':
        """Return new Prompt with updated task."""
        return replace(self, task=new_task)
    
    def with_context(self, new_context: str) -> 'Prompt':
        """Return new Prompt with updated context."""
        return replace(self, context=new_context)
    
    def add_constraint(self, constraint: str) -> 'Prompt':
        """Return new Prompt with additional constraint."""
        return replace(self, constraints=self.constraints + (constraint,))
    
    def with_role(self, role: str) -> 'Prompt':
        """Return new Prompt with role set."""
        return replace(self, role=role)
    
    def with_temperature(self, temp: float) -> 'Prompt':
        """Return new Prompt with updated temperature."""
        return replace(self, temperature=temp)
    
    def to_string(self) -> str:
        """Convert Prompt to formatted string."""
        parts = []
        
        if self.role:
            parts.append(f"Role: {self.role}")
        
        parts.append(f"Task: {self.task}")
        parts.append(f"Context: {self.context}")
        
        if self.constraints:
            constraints_text = "\n".join(f"- {c}" for c in self.constraints)
            parts.append(f"Constraints:\n{constraints_text}")
        
        parts.append(f"Temperature: {self.temperature}")
        
        return "\n\n".join(parts)


# ============================================================================
# Functional Collections Operations
# ============================================================================

def map_prompts(
    prompts: List[str],
    func: Callable[[str], str]
) -> List[str]:
    """Map a function over a list of prompts."""
    return list(map(func, prompts))


def filter_prompts(
    prompts: List[str],
    predicate: Callable[[str], bool]
) -> List[str]:
    """Filter prompts based on a predicate."""
    return list(filter(predicate, prompts))


def reduce_prompts(
    prompts: List[str],
    combiner: Callable[[str, str], str],
    initial: str = ""
) -> str:
    """Reduce a list of prompts to a single prompt."""
    return reduce(combiner, prompts, initial)


# ============================================================================
# Prompt Pipeline
# ============================================================================

class PromptPipeline:
    """
    Functional pipeline for prompt processing.
    
    Supports chaining transformations in a functional style.
    """
    
    def __init__(self, initial_prompt: str):
        self._prompt = initial_prompt
    
    def pipe(self, *operations: Callable[[str], str]) -> 'PromptPipeline':
        """
        Apply a series of operations to the prompt.
        
        Args:
            *operations: Functions to apply sequentially
            
        Returns:
            Self for chaining
        """
        for operation in operations:
            self._prompt = operation(self._prompt)
        return self
    
    def build(self) -> str:
        """Return the final prompt."""
        return self._prompt
    
    @staticmethod
    def from_prompt(prompt: str) -> 'PromptPipeline':
        """Create a pipeline from a prompt string."""
        return PromptPipeline(prompt)


# ============================================================================
# Monadic Composition
# ============================================================================

class PromptMonad(Generic[T]):
    """
    Monad for composing prompt transformations.
    
    Provides monadic operations: bind, map, and unit.
    """
    
    def __init__(self, value: T):
        self.value = value
    
    def bind(self, func: Callable[[T], 'PromptMonad[U]']) -> 'PromptMonad[U]':
        """
        Monadic bind operation (flatMap).
        
        Args:
            func: Function that returns a PromptMonad
            
        Returns:
            Result of applying func to the wrapped value
        """
        return func(self.value)
    
    def map(self, func: Callable[[T], U]) -> 'PromptMonad[U]':
        """
        Functor map operation.
        
        Args:
            func: Function to apply to the wrapped value
            
        Returns:
            New PromptMonad with transformed value
        """
        return PromptMonad(func(self.value))
    
    @staticmethod
    def unit(value: T) -> 'PromptMonad[T]':
        """
        Wrap a value in the monad.
        
        Args:
            value: Value to wrap
            
        Returns:
            PromptMonad containing the value
        """
        return PromptMonad(value)
    
    def __repr__(self) -> str:
        return f"PromptMonad({self.value!r})"


# ============================================================================
# Currying
# ============================================================================

def curry_prompt_builder(task: str) -> Callable[[str], Callable[[str], str]]:
    """
    Curried function for building prompts step by step.
    
    Args:
        task: The task description
        
    Returns:
        A curried function expecting context, then style
    """
    def with_context(context: str) -> Callable[[str], str]:
        def with_style(style: str) -> str:
            return f"Task: {task}\nContext: {context}\nStyle: {style}"
        return with_style
    return with_context


# ============================================================================
# Prompt Factories
# ============================================================================

def create_prompt_factory(template: str) -> Callable[..., str]:
    """
    Create a factory function for generating prompts from a template.
    
    Args:
        template: String template with format placeholders
        
    Returns:
        A function that generates prompts from keyword arguments
    """
    def generate_prompt(**kwargs: Any) -> str:
        return template.format(**kwargs)
    return generate_prompt


# ============================================================================
# Utility Functions
# ============================================================================

def memoize(func: Callable) -> Callable:
    """
    Memoization decorator for caching pure function results.
    
    Args:
        func: Function to memoize
        
    Returns:
        Memoized version of the function
    """
    cache = {}
    
    @wraps(func)
    def memoized(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    
    return memoized


def partial(func: Callable, *fixed_args, **fixed_kwargs) -> Callable:
    """
    Partial application of a function.
    
    Args:
        func: Function to partially apply
        *fixed_args: Fixed positional arguments
        **fixed_kwargs: Fixed keyword arguments
        
    Returns:
        Partially applied function
    """
    def partial_func(*args, **kwargs):
        return func(*fixed_args, *args, **{**fixed_kwargs, **kwargs})
    return partial_func


# ============================================================================
# Example Usage
# ============================================================================

def main():
    """Demonstrate functional prompt engineering."""
    
    print("=" * 80)
    print("Functional Prompt Engineering Examples")
    print("=" * 80)
    
    # Example 1: Pure function
    print("\n1. Pure Function:")
    prompt1 = create_basic_prompt("Explain AI", "Educational context")
    print(prompt1)
    
    # Example 2: Function composition
    print("\n2. Function Composition:")
    add_greeting = lambda text: f"Hello! {text}"
    add_closing = lambda text: f"{text}\nThank you!"
    
    full_builder = compose(add_closing, add_formality, add_greeting)
    prompt2 = full_builder("Please help me understand machine learning")
    print(prompt2)
    
    # Example 3: Immutable prompt
    print("\n3. Immutable Prompt Structure:")
    prompt3 = (Prompt("Analyze data", "Research project")
               .add_constraint("Use scientific terminology")
               .add_constraint("Cite sources")
               .with_role("Data Scientist")
               .with_temperature(0.5))
    print(prompt3.to_string())
    
    # Example 4: Pipeline
    print("\n4. Prompt Pipeline:")
    prompt4 = (PromptPipeline("explain quantum computing")
               .pipe(add_role_instruction("physics professor"),
                     add_context_marker("undergraduate lecture"),
                     add_politeness)
               .build())
    print(prompt4)
    
    # Example 5: Monadic composition
    print("\n5. Monadic Composition:")
    def wrap_in_markdown(text: str) -> PromptMonad[str]:
        return PromptMonad(f"```\n{text}\n```")
    
    def add_title(text: str) -> PromptMonad[str]:
        return PromptMonad(f"# Prompt\n\n{text}")
    
    prompt5 = (PromptMonad("What is machine learning?")
               .bind(wrap_in_markdown)
               .bind(add_title)
               .value)
    print(prompt5)
    
    # Example 6: Map/Filter/Reduce
    print("\n6. Map/Filter/Reduce:")
    prompts = ["explain AI", "describe ML", "define NLP", "what is deep learning?"]
    
    # Map: capitalize
    capitalized = map_prompts(prompts, str.upper)
    print(f"Capitalized: {capitalized[:2]}")
    
    # Filter: short prompts
    short = filter_prompts(prompts, lambda p: len(p) < 15)
    print(f"Short prompts: {short}")
    
    # Reduce: combine
    combined = reduce_prompts(
        prompts,
        lambda acc, p: f"{acc}\n- {p}",
        "Multi-task prompt:"
    )
    print(combined)
    
    # Example 7: Currying
    print("\n7. Currying:")
    build_ai_prompt = curry_prompt_builder("Explain AI")
    build_educational = build_ai_prompt("Educational")
    detailed = build_educational("Detailed")
    print(detailed)
    
    # Example 8: Factory
    print("\n8. Prompt Factory:")
    qa_factory = create_prompt_factory(
        "Question: {question}\nDomain: {domain}\nStyle: {style}"
    )
    prompt8 = qa_factory(
        question="How does neural networks work?",
        domain="Machine Learning",
        style="Technical"
    )
    print(prompt8)


if __name__ == "__main__":
    main()
