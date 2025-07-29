"""
Type inference module for WhatIF Analyzer.
"""

import inspect
from typing import Any, Dict, Type, get_type_hints, get_origin, get_args, Union

def infer_parameter_types(func: Any) -> Dict[str, Type]:
    """
    Infer the types of a function's parameters.
    
    Args:
        func: The function to analyze
        
    Returns:
        Dictionary mapping parameter names to their inferred types
    """
    # Get type hints from the function
    type_hints = get_type_hints(func)
    
    # Get the function's signature
    sig = inspect.signature(func)
    
    # Map parameter names to their types
    param_types = {}
    
    for param_name, param in sig.parameters.items():
        # Skip self parameter for methods
        if param_name == 'self':
            continue
            
        # Get the type from type hints
        param_type = type_hints.get(param_name, Any)
        
        # Handle Optional types
        if get_origin(param_type) is Union:
            args = get_args(param_type)
            if type(None) in args:
                # Get the non-None type
                param_type = next(arg for arg in args if arg is not type(None))
        
        # Handle container types
        if get_origin(param_type) in (list, tuple, set):
            args = get_args(param_type)
            if args:
                # Use the first type argument as the element type
                param_type = args[0]
            else:
                # Default to Any for unparameterized containers
                param_type = Any
        
        param_types[param_name] = param_type
    
    return param_types

def is_valid_type(type_: Type) -> bool:
    """
    Check if a type is valid for analysis.
    
    Args:
        type_: The type to check
        
    Returns:
        True if the type is valid for analysis, False otherwise
    """
    valid_types = {
        int, float, str, bool, list, dict, tuple, set,
        type(None), Any
    }
    
    # Check if it's a basic type
    if type_ in valid_types:
        return True
    
    # Check if it's a Union type
    if get_origin(type_) is Union:
        return all(is_valid_type(arg) for arg in get_args(type_))
    
    # Check if it's a container type
    if get_origin(type_) in (list, tuple, set):
        args = get_args(type_)
        return not args or all(is_valid_type(arg) for arg in args)
    
    # Check if it's a dict type
    if get_origin(type_) is dict:
        args = get_args(type_)
        return not args or all(is_valid_type(arg) for arg in args)
    
    return False 