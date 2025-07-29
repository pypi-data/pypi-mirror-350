"""
Tests for the type inference module.
"""

import pytest
from typing import Any, Dict, List, Optional, Union
from whatif_analyzer.type_inference import infer_parameter_types, is_valid_type

def test_basic_type_inference():
    """Test basic type inference."""
    def func(a: int, b: str) -> bool:
        return len(b) > a
    
    types = infer_parameter_types(func)
    assert types["a"] == int
    assert types["b"] == str

def test_optional_type_inference():
    """Test inference of optional types."""
    def func(a: Optional[int] = None, b: str = "") -> bool:
        return len(b) > (a or 0)
    
    types = infer_parameter_types(func)
    assert types["a"] == int
    assert types["b"] == str

def test_union_type_inference():
    """Test inference of union types."""
    def func(a: Union[int, float], b: Union[str, None]) -> bool:
        return len(str(b or "")) > a
    
    types = infer_parameter_types(func)
    assert types["a"] in (int, float)
    assert types["b"] == str

def test_list_type_inference():
    """Test inference of list types."""
    def func(a: List[int], b: List[str]) -> int:
        return len(a) + len(b)
    
    types = infer_parameter_types(func)
    assert types["a"] == int
    assert types["b"] == str

def test_dict_type_inference():
    """Test inference of dictionary types."""
    def func(a: Dict[str, int], b: Dict[int, str]) -> int:
        return len(a) + len(b)
    
    types = infer_parameter_types(func)
    assert types["a"] == int
    assert types["b"] == str

def test_complex_type_inference():
    """Test inference of complex nested types."""
    def func(
        a: List[Dict[str, int]],
        b: Dict[str, List[float]]
    ) -> int:
        return len(a) + len(b)
    
    types = infer_parameter_types(func)
    assert types["a"] == int
    assert types["b"] == float

def test_method_type_inference():
    """Test type inference for class methods."""
    class TestClass:
        def method(self, a: int, b: str) -> bool:
            return len(b) > a
    
    types = infer_parameter_types(TestClass.method)
    assert "self" not in types
    assert types["a"] == int
    assert types["b"] == str

def test_no_type_hints():
    """Test inference with no type hints."""
    def func(a, b):
        return a + b
    
    types = infer_parameter_types(func)
    assert types["a"] == Any
    assert types["b"] == Any

def test_is_valid_type():
    """Test type validation."""
    assert is_valid_type(int)
    assert is_valid_type(float)
    assert is_valid_type(str)
    assert is_valid_type(bool)
    assert is_valid_type(list)
    assert is_valid_type(dict)
    assert is_valid_type(type(None))
    assert is_valid_type(Any)
    
    assert is_valid_type(Optional[int])
    assert is_valid_type(Union[int, float])
    assert is_valid_type(List[int])
    assert is_valid_type(Dict[str, int])
    
    assert not is_valid_type(object)
    assert not is_valid_type(Exception)
    assert not is_valid_type(type)

def test_nested_type_validation():
    """Test validation of nested types."""
    assert is_valid_type(List[Dict[str, int]])
    assert is_valid_type(Dict[str, List[float]])
    assert is_valid_type(Union[List[int], Dict[str, float]])
    
    assert not is_valid_type(List[object])
    assert not is_valid_type(Dict[str, Exception])
    assert not is_valid_type(Union[List[object], Dict[str, Exception]])

def test_type_inference_with_defaults():
    """Test type inference with default values."""
    def func(a: int = 0, b: str = "", c: bool = False) -> bool:
        return len(b) > a and c
    
    types = infer_parameter_types(func)
    assert types["a"] == int
    assert types["b"] == str
    assert types["c"] == bool

def test_type_inference_with_complex_defaults():
    """Test type inference with complex default values."""
    def func(
        a: List[int] = None,
        b: Dict[str, int] = None,
        c: Optional[str] = None
    ) -> bool:
        return bool(a and b and c)
    
    types = infer_parameter_types(func)
    assert types["a"] == int
    assert types["b"] == int
    assert types["c"] == str 