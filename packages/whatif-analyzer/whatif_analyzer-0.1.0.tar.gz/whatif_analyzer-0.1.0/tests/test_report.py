"""
Tests for the report module.
"""

import pytest
from whatif_analyzer.report import TestResult, AnalysisReport
from whatif_analyzer.edge_cases import EdgeCase

def test_test_result_creation():
    """Test creating test results."""
    edge_case = EdgeCase("test", 42)
    
    # Successful result
    success_result = TestResult(
        edge_case=edge_case,
        success=True,
        error=None,
        output=42
    )
    assert success_result.edge_case == edge_case
    assert success_result.success is True
    assert success_result.error is None
    assert success_result.output == 42
    
    # Failed result
    error_result = TestResult(
        edge_case=edge_case,
        success=False,
        error="Test failed",
        output=None
    )
    assert error_result.edge_case == edge_case
    assert error_result.success is False
    assert error_result.error == "Test failed"
    assert error_result.output is None

def test_analysis_report_creation():
    """Test creating analysis reports."""
    edge_case = EdgeCase("test", 42)
    results = [
        TestResult(edge_case, True, None, 42),
        TestResult(edge_case, False, "Error", None)
    ]
    
    report = AnalysisReport(
        function_name="test_func",
        parameter_types={"x": int, "y": str},
        results=results
    )
    
    assert report.function_name == "test_func"
    assert report.parameter_types == {"x": int, "y": str}
    assert report.results == results

def test_analysis_report_str():
    """Test string representation of analysis reports."""
    edge_case = EdgeCase("test", 42)
    results = [
        TestResult(edge_case, True, None, 42),
        TestResult(edge_case, False, "Error", None)
    ]
    
    report = AnalysisReport(
        function_name="test_func",
        parameter_types={"x": int, "y": str},
        results=results
    )
    
    report_str = str(report)
    assert "WhatIF Analysis Report" in report_str
    assert "test_func" in report_str
    assert "x: int" in report_str
    assert "y: str" in report_str
    assert "test" in report_str
    assert "Error" in report_str

def test_analysis_report_to_dict():
    """Test converting analysis report to dictionary."""
    edge_case = EdgeCase("test", 42)
    results = [
        TestResult(edge_case, True, None, 42),
        TestResult(edge_case, False, "Error", None)
    ]
    
    report = AnalysisReport(
        function_name="test_func",
        parameter_types={"x": int, "y": str},
        results=results
    )
    
    report_dict = report.to_dict()
    assert report_dict["function_name"] == "test_func"
    assert report_dict["parameter_types"] == {"x": "int", "y": "str"}
    assert len(report_dict["results"]) == 2
    
    # Check first result
    assert report_dict["results"][0]["edge_case"]["name"] == "test"
    assert report_dict["results"][0]["success"] is True
    assert report_dict["results"][0]["error"] is None
    assert report_dict["results"][0]["output"] == "42"
    
    # Check second result
    assert report_dict["results"][1]["edge_case"]["name"] == "test"
    assert report_dict["results"][1]["success"] is False
    assert report_dict["results"][1]["error"] == "Error"
    assert report_dict["results"][1]["output"] is None

def test_analysis_report_with_multiple_results():
    """Test analysis report with multiple test results."""
    edge_cases = [
        EdgeCase("zero", 0),
        EdgeCase("positive", 42),
        EdgeCase("negative", -1)
    ]
    
    results = [
        TestResult(edge_cases[0], True, None, 0),
        TestResult(edge_cases[1], True, None, 42),
        TestResult(edge_cases[2], False, "Negative not allowed", None)
    ]
    
    report = AnalysisReport(
        function_name="test_func",
        parameter_types={"x": int},
        results=results
    )
    
    report_str = str(report)
    assert "zero" in report_str
    assert "positive" in report_str
    assert "negative" in report_str
    assert "Negative not allowed" in report_str

def test_analysis_report_with_complex_types():
    """Test analysis report with complex parameter types."""
    edge_case = EdgeCase("test", [1, 2, 3])
    results = [
        TestResult(edge_case, True, None, [1, 2, 3])
    ]
    
    report = AnalysisReport(
        function_name="test_func",
        parameter_types={
            "x": list,
            "y": dict,
            "z": str
        },
        results=results
    )
    
    report_str = str(report)
    assert "x: list" in report_str
    assert "y: dict" in report_str
    assert "z: str" in report_str

def test_analysis_report_with_none_values():
    """Test analysis report with None values."""
    edge_case = EdgeCase("test", None)
    results = [
        TestResult(edge_case, True, None, None)
    ]
    
    report = AnalysisReport(
        function_name="test_func",
        parameter_types={"x": type(None)},
        results=results
    )
    
    report_str = str(report)
    assert "x: NoneType" in report_str
    assert "None" in report_str

def test_analysis_report_with_exceptions():
    """Test analysis report with various exceptions."""
    edge_case = EdgeCase("test", 42)
    results = [
        TestResult(edge_case, False, "ValueError: Invalid value", None),
        TestResult(edge_case, False, "TypeError: Wrong type", None),
        TestResult(edge_case, False, "ZeroDivisionError: Division by zero", None)
    ]
    
    report = AnalysisReport(
        function_name="test_func",
        parameter_types={"x": int},
        results=results
    )
    
    report_str = str(report)
    assert "ValueError" in report_str
    assert "TypeError" in report_str
    assert "ZeroDivisionError" in report_str 