"""
Basic usage examples for WhatIF Analyzer.
"""

from whatif_analyzer import analyze, WhatIfAnalyzer, EdgeCase

# Example 1: Using the decorator
@analyze
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    return a / b

# Example 2: Using the analyzer directly
def process_string(s: str, max_length: int = 10) -> str:
    """Process a string with a maximum length."""
    if not s:
        return ""
    return s.strip()[:max_length]

# Example 3: Using custom edge cases
def check_number(n: int) -> bool:
    """Check if a number is positive and even."""
    return n > 0 and n % 2 == 0

# Example 4: Complex function with multiple parameters
def calculate_statistics(
    numbers: list,
    min_value: float = 0.0,
    max_value: float = 100.0
) -> dict:
    """Calculate statistics for a list of numbers."""
    if not numbers:
        return {
            "count": 0,
            "average": 0.0,
            "min": min_value,
            "max": max_value
        }
    
    valid_numbers = [
        n for n in numbers
        if min_value <= n <= max_value
    ]
    
    if not valid_numbers:
        return {
            "count": 0,
            "average": 0.0,
            "min": min_value,
            "max": max_value
        }
    
    return {
        "count": len(valid_numbers),
        "average": sum(valid_numbers) / len(valid_numbers),
        "min": min(valid_numbers),
        "max": max(valid_numbers)
    }

def main():
    """Run the examples."""
    # Example 1: The decorator will automatically analyze the function
    print("Example 1: Using the decorator")
    result = divide(10, 2)
    print(f"Result: {result}\n")
    
    # Example 2: Using the analyzer directly
    print("Example 2: Using the analyzer directly")
    analyzer = WhatIfAnalyzer()
    report = analyzer.analyze_function(process_string)
    print(report)
    print()
    
    # Example 3: Using custom edge cases
    print("Example 3: Using custom edge cases")
    custom_cases = [
        EdgeCase("special_value", 42),
        EdgeCase("boundary", 0),
        EdgeCase("negative_even", -2)
    ]
    report = analyzer.analyze_function(check_number, custom_edge_cases=custom_cases)
    print(report)
    print()
    
    # Example 4: Complex function
    print("Example 4: Complex function")
    report = analyzer.analyze_function(calculate_statistics)
    print(report)

if __name__ == "__main__":
    main() 