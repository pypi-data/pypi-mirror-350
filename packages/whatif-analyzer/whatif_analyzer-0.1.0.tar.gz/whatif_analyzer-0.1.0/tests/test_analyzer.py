"""
Tests for the WhatIF Analyzer.
"""

import pytest
from whatif_analyzer import WhatIfAnalyzer, analyze, EdgeCase
from whatif_analyzer.analyzer import AnalyzerConfig

def test_basic_function_analysis():
    """Test basic function analysis."""
    def divide(a: float, b: float) -> float:
        return a / b
    
    analyzer = WhatIfAnalyzer()
    report = analyzer.analyze_function(divide)
    
    assert report.function_name == "divide"
    assert len(report.results) > 0
    assert any(not r.success for r in report.results)  # Should find division by zero

def test_decorator_usage():
    """Test the @analyze decorator."""
    @analyze
    def process_string(s: str) -> int:
        return len(s.strip())
    
    # The decorator should not affect the function's behavior
    assert process_string("  hello  ") == 5

def test_custom_edge_cases():
    """Test analysis with custom edge cases."""
    def check_number(n: int) -> bool:
        return n > 0
    
    custom_cases = [
        EdgeCase("special_value", 42),
        EdgeCase("boundary", 0)
    ]
    
    analyzer = WhatIfAnalyzer()
    report = analyzer.analyze_function(check_number, custom_edge_cases=custom_cases)
    
    # Should find both custom cases in results
    case_names = {r.edge_case.name for r in report.results}
    assert "special_value" in case_names
    assert "boundary" in case_names

def test_fuzzing():
    """Test fuzzing functionality."""
    def add_numbers(a: int, b: int) -> int:
        return a + b
    
    config = AnalyzerConfig(enable_fuzzing=True, max_fuzz_cases=10)
    analyzer = WhatIfAnalyzer(config)
    report = analyzer.analyze_function(add_numbers)
    
    # Should have at least the fuzzing cases
    assert len(report.results) >= 10

def test_timeout():
    """Test analysis timeout."""
    def slow_function(x: int) -> int:
        import time
        time.sleep(0.1)  # Simulate slow operation
        return x * 2
    
    config = AnalyzerConfig(timeout_seconds=1)
    analyzer = WhatIfAnalyzer(config)
    report = analyzer.analyze_function(slow_function)
    
    # Should complete within timeout
    assert len(report.results) > 0

def test_error_handling():
    """Test error handling in analysis."""
    def error_function(x: int) -> int:
        if x == 0:
            raise ValueError("Zero not allowed")
        return x
    
    analyzer = WhatIfAnalyzer()
    report = analyzer.analyze_function(error_function)
    
    # Should catch and report the error
    assert any(not r.success and "Zero not allowed" in r.error for r in report.results)

def test_complex_types():
    """Test analysis with complex types."""
    def process_list(items: list) -> int:
        return sum(1 for x in items if x > 0)
    
    analyzer = WhatIfAnalyzer()
    report = analyzer.analyze_function(process_list)
    
    assert report.function_name == "process_list"
    assert len(report.results) > 0

def test_optional_parameters():
    """Test analysis with optional parameters."""
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"
    
    analyzer = WhatIfAnalyzer()
    report = analyzer.analyze_function(greet)
    
    assert report.function_name == "greet"
    assert len(report.results) > 0
    assert all(r.success for r in report.results)  # Should handle all cases

def test_none_handling():
    """Test analysis with None values."""
    def safe_divide(a: float, b: float) -> float:
        if a is None or b is None:
            return 0.0
        return a / b
    
    analyzer = WhatIfAnalyzer()
    report = analyzer.analyze_function(safe_divide)
    
    # Should handle None values without errors
    assert all(r.success for r in report.results)

def test_large_numbers():
    """Test analysis with large numbers."""
    def check_range(n: int) -> bool:
        return -1000 <= n <= 1000
    
    analyzer = WhatIfAnalyzer()
    report = analyzer.analyze_function(check_range)
    
    # Should find cases outside the range
    assert any(not r.success for r in report.results) 