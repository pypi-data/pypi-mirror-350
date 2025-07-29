"""
Tests for the WhatIF Analyzer CLI.
"""

import os
import sys
from pathlib import Path
import pytest
from click.testing import CliRunner

from whatif_analyzer.cli import cli

@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()

@pytest.fixture
def example_file(tmp_path):
    """Create a temporary example file."""
    file_path = tmp_path / "example.py"
    file_path.write_text("""
def add(a: int, b: int) -> int:
    return a + b
""")
    return file_path

def test_cli_help(runner):
    """Test CLI help command."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "WhatIF Analyzer" in result.output

def test_analyze_file(runner, example_file):
    """Test analyzing a Python file."""
    result = runner.invoke(cli, ["analyze", str(example_file)])
    assert result.exit_code == 0
    assert "WhatIF Analysis Report" in result.output

def test_analyze_with_options(runner, example_file):
    """Test analyzing with CLI options."""
    result = runner.invoke(cli, [
        "analyze",
        str(example_file),
        "--enable-fuzzing",
        "--max-fuzz-cases", "10",
        "--timeout", "5",
        "--verbose"
    ])
    assert result.exit_code == 0
    assert "WhatIF Analysis Report" in result.output

def test_analyze_nonexistent_file(runner):
    """Test analyzing a nonexistent file."""
    result = runner.invoke(cli, ["analyze", "nonexistent.py"])
    assert result.exit_code == 1
    assert "Error" in result.output

def test_analyze_invalid_module(runner):
    """Test analyzing an invalid module."""
    result = runner.invoke(cli, ["analyze", "invalid.module"])
    assert result.exit_code == 1
    assert "Error" in result.output

def test_analyze_function_path(runner, example_file):
    """Test analyzing a specific function."""
    result = runner.invoke(cli, [
        "analyze",
        f"{example_file}:add"
    ])
    assert result.exit_code == 0
    assert "WhatIF Analysis Report" in result.output

def test_analyze_invalid_function(runner, example_file):
    """Test analyzing an invalid function."""
    result = runner.invoke(cli, [
        "analyze",
        f"{example_file}:nonexistent"
    ])
    assert result.exit_code == 1
    assert "Error" in result.output

def test_analyze_module_with_multiple_functions(tmp_path, runner):
    """Test analyzing a module with multiple functions."""
    file_path = tmp_path / "multi_func.py"
    file_path.write_text("""
def add(a: int, b: int) -> int:
    return a + b

def subtract(a: int, b: int) -> int:
    return a - b
""")
    
    result = runner.invoke(cli, ["analyze", str(file_path)])
    assert result.exit_code == 0
    assert "WhatIF Analysis Report" in result.output

def test_analyze_with_custom_edge_cases(tmp_path, runner):
    """Test analyzing with custom edge cases."""
    file_path = tmp_path / "custom_cases.py"
    file_path.write_text("""
def check_number(n: int) -> bool:
    return n > 0
""")
    
    result = runner.invoke(cli, [
        "analyze",
        str(file_path),
        "--verbose"
    ])
    assert result.exit_code == 0
    assert "WhatIF Analysis Report" in result.output

def test_analyze_with_timeout(tmp_path, runner):
    """Test analyzing with a timeout."""
    file_path = tmp_path / "slow_func.py"
    file_path.write_text("""
import time

def slow_function(x: int) -> int:
    time.sleep(0.1)
    return x * 2
""")
    
    result = runner.invoke(cli, [
        "analyze",
        str(file_path),
        "--timeout", "1"
    ])
    assert result.exit_code == 0
    assert "WhatIF Analysis Report" in result.output 