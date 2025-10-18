#!/usr/bin/env python3
"""
Tests for Functional Prompt Engineering Library

These tests demonstrate the key functional programming concepts
and validate the implementation.
"""

import sys
from functional_prompt import (
    create_basic_prompt,
    create_structured_prompt,
    compose,
    Prompt,
    PromptPipeline,
    PromptMonad,
    add_formality,
    add_politeness,
    add_urgency,
    add_role_instruction,
    add_context_marker,
    map_prompts,
    filter_prompts,
    reduce_prompts,
    curry_prompt_builder,
    create_prompt_factory,
)

# Helper functions for tests
def add_greeting(text):
    return f"Hello! {text}"

def add_closing(text):
    return f"{text}\nThank you!"


def test_pure_functions():
    """Test that pure functions are deterministic"""
    print("Testing pure functions...")
    
    # Same inputs should always produce same outputs
    prompt1 = create_basic_prompt("Task A", "Context B")
    prompt2 = create_basic_prompt("Task A", "Context B")
    
    assert prompt1 == prompt2, "Pure functions should be deterministic"
    print("✓ Pure functions are deterministic")


def test_immutability():
    """Test that Prompt objects are immutable"""
    print("\nTesting immutability...")
    
    original = Prompt("Original task", "Original context")
    modified = original.with_task("New task")
    
    # Original should be unchanged
    assert original.task == "Original task", "Original should be unchanged"
    assert modified.task == "New task", "Modified should have new task"
    print("✓ Prompt objects are immutable")


def test_composition():
    """Test function composition"""
    print("\nTesting function composition...")
    
    # Compose multiple transformations
    transform = compose(add_closing, add_formality, add_greeting)
    result = transform("test prompt")
    
    # Should apply transformations in order: greeting -> formality -> closing
    assert "Hello!" in result, "Should have greeting"
    assert "Respectfully" in result, "Should have formality"
    assert "Thank you!" in result, "Should have closing"
    print("✓ Function composition works correctly")


def test_higher_order_functions():
    """Test higher-order functions"""
    print("\nTesting higher-order functions...")
    
    # Create a specialized function using a higher-order function
    add_professor_role = add_role_instruction("professor")
    result = add_professor_role("Explain quantum physics")
    
    assert "professor" in result, "Should include role"
    assert "Explain quantum physics" in result, "Should include original text"
    print("✓ Higher-order functions work correctly")


def test_pipeline():
    """Test pipeline pattern"""
    print("\nTesting pipeline...")
    
    result = (PromptPipeline("base prompt")
              .pipe(add_greeting, add_formality)
              .build())
    
    assert "Hello!" in result, "Pipeline should apply greeting"
    assert "Respectfully" in result, "Pipeline should apply formality"
    print("✓ Pipeline pattern works correctly")


def test_monadic_composition():
    """Test monadic composition"""
    print("\nTesting monadic composition...")
    
    def wrap_brackets(text):
        return PromptMonad(f"[{text}]")
    
    def add_prefix(text):
        return PromptMonad(f"PREFIX: {text}")
    
    result = (PromptMonad("test")
              .bind(wrap_brackets)
              .bind(add_prefix)
              .value)
    
    assert result == "PREFIX: [test]", "Monad should compose correctly"
    print("✓ Monadic composition works correctly")


def test_map_filter_reduce():
    """Test functional collection operations"""
    print("\nTesting map/filter/reduce...")
    
    prompts = ["short", "a bit longer", "tiny", "this one is quite long"]
    
    # Map
    upper = map_prompts(prompts, str.upper)
    assert all(p.isupper() for p in upper), "All should be uppercase"
    
    # Filter
    short = filter_prompts(prompts, lambda p: len(p) < 10)
    assert all(len(p) < 10 for p in short), "All should be short"
    
    # Reduce
    combined = reduce_prompts(prompts, lambda acc, p: f"{acc}|{p}", "START")
    assert combined.startswith("START|"), "Should start with initial value"
    
    print("✓ Map/Filter/Reduce work correctly")


def test_currying():
    """Test currying"""
    print("\nTesting currying...")
    
    # Build prompt step by step
    build_ai = curry_prompt_builder("Explain AI")
    build_ai_edu = build_ai("Educational")
    detailed = build_ai_edu("Detailed")
    
    assert "Explain AI" in detailed, "Should include task"
    assert "Educational" in detailed, "Should include context"
    assert "Detailed" in detailed, "Should include style"
    print("✓ Currying works correctly")


def test_factory_pattern():
    """Test factory pattern"""
    print("\nTesting factory pattern...")
    
    template = "Q: {question}\nA: {answer}"
    factory = create_prompt_factory(template)
    
    result = factory(question="What is AI?", answer="Artificial Intelligence")
    
    assert "What is AI?" in result, "Should include question"
    assert "Artificial Intelligence" in result, "Should include answer"
    print("✓ Factory pattern works correctly")


def test_chaining():
    """Test chaining immutable operations"""
    print("\nTesting chaining...")
    
    prompt = (Prompt("Base task", "Base context")
              .add_constraint("Constraint 1")
              .add_constraint("Constraint 2")
              .with_role("Expert")
              .with_temperature(0.3))
    
    assert len(prompt.constraints) == 2, "Should have 2 constraints"
    assert prompt.role == "Expert", "Should have role"
    assert prompt.temperature == 0.3, "Should have temperature"
    print("✓ Chaining works correctly")


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("Running Functional Prompt Engineering Tests")
    print("=" * 70)
    
    tests = [
        test_pure_functions,
        test_immutability,
        test_composition,
        test_higher_order_functions,
        test_pipeline,
        test_monadic_composition,
        test_map_filter_reduce,
        test_currying,
        test_factory_pattern,
        test_chaining,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    if failed == 0:
        print("✓ All tests passed!")
    else:
        print(f"✗ {failed} test(s) failed")
    print("=" * 70)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
