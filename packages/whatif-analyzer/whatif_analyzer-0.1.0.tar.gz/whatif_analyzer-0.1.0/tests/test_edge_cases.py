"""
Tests for the edge cases module.
"""

import pytest
from whatif_analyzer.edge_cases import EdgeCase, generate_edge_cases, generate_custom_edge_cases

def test_edge_case_creation():
    """Test creating edge cases."""
    case = EdgeCase("test", 42)
    assert case.name == "test"
    assert case.value == 42
    assert case.condition is None
    
    case_with_condition = EdgeCase("test", 42, lambda x: x > 0)
    assert case_with_condition.name == "test"
    assert case_with_condition.value == 42
    assert case_with_condition.condition(42) is True

def test_generate_edge_cases_int():
    """Test generating edge cases for integers."""
    cases = generate_edge_cases(int)
    assert len(cases) > 0
    
    # Check for specific cases
    case_names = {case.name for case in cases}
    assert "zero" in case_names
    assert "negative" in case_names
    assert "large_positive" in case_names
    assert "large_negative" in case_names

def test_generate_edge_cases_float():
    """Test generating edge cases for floats."""
    cases = generate_edge_cases(float)
    assert len(cases) > 0
    
    # Check for specific cases
    case_names = {case.name for case in cases}
    assert "zero" in case_names
    assert "infinity" in case_names
    assert "nan" in case_names
    assert "small_positive" in case_names
    assert "small_negative" in case_names

def test_generate_edge_cases_str():
    """Test generating edge cases for strings."""
    cases = generate_edge_cases(str)
    assert len(cases) > 0
    
    # Check for specific cases
    case_names = {case.name for case in cases}
    assert "empty" in case_names
    assert "whitespace" in case_names
    assert "unicode" in case_names
    assert "long" in case_names

def test_generate_edge_cases_list():
    """Test generating edge cases for lists."""
    cases = generate_edge_cases(list)
    assert len(cases) > 0
    
    # Check for specific cases
    case_names = {case.name for case in cases}
    assert "empty" in case_names
    assert "single_element" in case_names
    assert "large" in case_names

def test_generate_edge_cases_dict():
    """Test generating edge cases for dictionaries."""
    cases = generate_edge_cases(dict)
    assert len(cases) > 0
    
    # Check for specific cases
    case_names = {case.name for case in cases}
    assert "empty" in case_names
    assert "single_key" in case_names
    assert "large" in case_names

def test_generate_edge_cases_bool():
    """Test generating edge cases for booleans."""
    cases = generate_edge_cases(bool)
    assert len(cases) == 2
    
    # Check for specific cases
    case_names = {case.name for case in cases}
    assert "true" in case_names
    assert "false" in case_names

def test_generate_edge_cases_none():
    """Test generating edge cases for None."""
    cases = generate_edge_cases(type(None))
    assert len(cases) == 1
    assert cases[0].name == "none"
    assert cases[0].value is None

def test_generate_custom_edge_cases():
    """Test generating custom edge cases."""
    custom_cases = {
        "special": 42,
        "boundary": 0,
        "invalid": -1
    }
    
    cases = generate_custom_edge_cases(int, custom_cases)
    assert len(cases) > len(custom_cases)  # Should include both custom and default cases
    
    # Check for custom cases
    case_names = {case.name for case in cases}
    assert "special" in case_names
    assert "boundary" in case_names
    assert "invalid" in case_names
    
    # Check for default cases
    assert "zero" in case_names
    assert "negative" in case_names

def test_edge_case_condition():
    """Test edge case conditions."""
    case = EdgeCase("test", 42, lambda x: x > 0)
    assert case.condition(42) is True
    assert case.condition(0) is False
    assert case.condition(-1) is False

def test_edge_case_str_representation():
    """Test string representation of edge cases."""
    case = EdgeCase("test", 42)
    assert str(case) == "test"
    
    case_with_condition = EdgeCase("test", 42, lambda x: x > 0)
    assert str(case_with_condition) == "test"

def test_edge_case_equality():
    """Test edge case equality."""
    case1 = EdgeCase("test", 42)
    case2 = EdgeCase("test", 42)
    case3 = EdgeCase("other", 42)
    
    assert case1 == case2
    assert case1 != case3 