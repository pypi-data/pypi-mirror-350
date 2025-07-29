"""
Advanced usage examples for WhatIF Analyzer.
"""

import json
from dataclasses import dataclass
from typing import List, Optional, Union

from whatif_analyzer import WhatIfAnalyzer, EdgeCase, analyze

# Example 1: Class with methods
@dataclass
class User:
    """Represents a user in the system."""
    name: str
    age: int
    email: Optional[str] = None
    preferences: Optional[dict] = None
    
    def validate(self) -> bool:
        """Validate user data."""
        if not self.name or len(self.name) < 2:
            return False
        if self.age < 0 or self.age > 150:
            return False
        if self.email and '@' not in self.email:
            return False
        return True
    
    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "preferences": self.preferences or {}
        }

# Example 2: Function with complex type hints
def process_data(
    data: Union[List[dict], dict],
    schema: Optional[dict] = None,
    strict: bool = True
) -> dict:
    """
    Process data according to a schema.
    
    Args:
        data: Input data (list of dicts or single dict)
        schema: Optional schema to validate against
        strict: Whether to enforce strict validation
        
    Returns:
        Processed data as a dictionary
    """
    if not data:
        return {"error": "No data provided"}
    
    if schema and strict:
        # Validate against schema
        if isinstance(data, list):
            for item in data:
                if not all(k in item for k in schema.get("required", [])):
                    return {"error": "Missing required fields"}
        else:
            if not all(k in data for k in schema.get("required", [])):
                return {"error": "Missing required fields"}
    
    # Process the data
    if isinstance(data, list):
        return {
            "count": len(data),
            "items": data,
            "processed": True
        }
    else:
        return {
            "item": data,
            "processed": True
        }

# Example 3: Function with custom edge cases
def analyze_user_data(user_data: dict) -> dict:
    """
    Analyze user data and generate insights.
    
    Args:
        user_data: Dictionary containing user data
        
    Returns:
        Dictionary with analysis results
    """
    if not user_data:
        return {"error": "No data provided"}
    
    # Extract relevant fields
    age = user_data.get("age", 0)
    activity = user_data.get("activity_level", "unknown")
    preferences = user_data.get("preferences", {})
    
    # Generate insights
    insights = {
        "age_group": "senior" if age > 65 else "adult" if age > 18 else "minor",
        "activity_category": activity.lower(),
        "preference_count": len(preferences)
    }
    
    # Add recommendations
    if age < 18:
        insights["recommendations"] = ["parental_guidance"]
    elif age > 65:
        insights["recommendations"] = ["senior_support"]
    
    return insights

def main():
    """Run the advanced examples."""
    analyzer = WhatIfAnalyzer()
    
    # Example 1: Analyze class methods
    print("Example 1: Analyzing class methods")
    user = User("John Doe", 30)
    report = analyzer.analyze_function(user.validate)
    print(report)
    print()
    
    # Example 2: Analyze function with complex types
    print("Example 2: Analyzing function with complex types")
    schema = {
        "required": ["name", "age"],
        "optional": ["email", "preferences"]
    }
    report = analyzer.analyze_function(
        process_data,
        custom_edge_cases=[
            EdgeCase("empty_list", []),
            EdgeCase("invalid_schema", {"invalid": "schema"}),
            EdgeCase("missing_required", {"name": "John"})
        ]
    )
    print(report)
    print()
    
    # Example 3: Analyze function with custom edge cases
    print("Example 3: Analyzing function with custom edge cases")
    custom_cases = [
        EdgeCase("empty_data", {}),
        EdgeCase("minimal_data", {"age": 25}),
        EdgeCase("complete_data", {
            "age": 30,
            "activity_level": "high",
            "preferences": {"theme": "dark", "notifications": True}
        }),
        EdgeCase("invalid_age", {"age": -1}),
        EdgeCase("senior_user", {"age": 70, "activity_level": "low"})
    ]
    report = analyzer.analyze_function(
        analyze_user_data,
        custom_edge_cases=custom_cases
    )
    print(report)

if __name__ == "__main__":
    main() 