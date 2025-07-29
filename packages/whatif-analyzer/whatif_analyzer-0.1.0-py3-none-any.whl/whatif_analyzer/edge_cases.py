"""
Edge case generation module for WhatIF Analyzer.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Type, Union

@dataclass
class EdgeCase:
    """Represents an edge case for testing."""
    name: str
    value: Any
    condition: Optional[Callable[[Any], bool]] = None

def generate_edge_cases(type_: Type) -> List[EdgeCase]:
    """
    Generate edge cases for a given type.
    
    Args:
        type_: The type to generate edge cases for
        
    Returns:
        List of EdgeCase objects
    """
    if type_ == int:
        return [
            EdgeCase("zero", 0),
            EdgeCase("negative", -1),
            EdgeCase("large_positive", 2**31 - 1),
            EdgeCase("large_negative", -2**31),
            EdgeCase("one", 1),
            EdgeCase("minus_one", -1),
        ]
    elif type_ == float:
        return [
            EdgeCase("zero", 0.0),
            EdgeCase("negative", -1.0),
            EdgeCase("large_positive", 1e308),
            EdgeCase("large_negative", -1e308),
            EdgeCase("small_positive", 1e-308),
            EdgeCase("small_negative", -1e-308),
            EdgeCase("infinity", float('inf')),
            EdgeCase("negative_infinity", float('-inf')),
            EdgeCase("nan", float('nan')),
        ]
    elif type_ == str:
        return [
            EdgeCase("empty", ""),
            EdgeCase("whitespace", "   "),
            EdgeCase("newline", "\n"),
            EdgeCase("tab", "\t"),
            EdgeCase("special_chars", "!@#$%^&*()"),
            EdgeCase("unicode", "你好世界"),
            EdgeCase("long", "x" * 1000),
        ]
    elif type_ == list:
        return [
            EdgeCase("empty", []),
            EdgeCase("single_element", [None]),
            EdgeCase("large", [None] * 1000),
        ]
    elif type_ == dict:
        return [
            EdgeCase("empty", {}),
            EdgeCase("single_key", {"key": None}),
            EdgeCase("large", {str(i): i for i in range(1000)}),
        ]
    elif type_ == bool:
        return [
            EdgeCase("true", True),
            EdgeCase("false", False),
        ]
    elif type_ == type(None):
        return [EdgeCase("none", None)]
    
    # For custom types or unknown types, return basic edge cases
    return [
        EdgeCase("none", None),
        EdgeCase("empty", ""),
        EdgeCase("zero", 0),
    ]

def generate_custom_edge_cases(
    type_: Type,
    custom_cases: Dict[str, Any]
) -> List[EdgeCase]:
    """
    Generate custom edge cases for a given type.
    
    Args:
        type_: The type to generate edge cases for
        custom_cases: Dictionary of custom case names and values
        
    Returns:
        List of EdgeCase objects
    """
    base_cases = generate_edge_cases(type_)
    custom_edge_cases = [
        EdgeCase(name, value)
        for name, value in custom_cases.items()
    ]
    return base_cases + custom_edge_cases 