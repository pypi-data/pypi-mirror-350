"""
Command-line interface for WhatIF Analyzer.
"""

import importlib
import inspect
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from whatif_analyzer.analyzer import WhatIfAnalyzer, AnalyzerConfig

console = Console()

@click.group()
def cli():
    """WhatIF Analyzer - Analyze functions with what-if scenarios."""
    pass

@cli.command()
@click.argument('target', type=str)
@click.option('--enable-fuzzing/--no-fuzzing', default=True, help='Enable/disable fuzzing')
@click.option('--max-fuzz-cases', type=int, default=50, help='Maximum number of fuzzing cases')
@click.option('--timeout', type=int, default=5, help='Analysis timeout in seconds')
@click.option('--verbose/--quiet', default=False, help='Enable verbose output')
def analyze(target: str, enable_fuzzing: bool, max_fuzz_cases: int, timeout: int, verbose: bool):
    """
    Analyze a function or module.
    
    TARGET can be either:
    - A Python file path (e.g., path/to/file.py)
    - A module path (e.g., module.submodule)
    - A function path (e.g., module.submodule:function_name)
    """
    try:
        # Parse the target
        if ':' in target:
            # Function path
            module_path, function_name = target.rsplit(':', 1)
            func = _import_function(module_path, function_name)
        else:
            # File or module path
            if target.endswith('.py'):
                # Python file
                func = _import_from_file(target)
            else:
                # Module path
                func = _import_module(target)
        
        # Create analyzer configuration
        config = AnalyzerConfig(
            enable_fuzzing=enable_fuzzing,
            max_fuzz_cases=max_fuzz_cases,
            timeout_seconds=timeout,
            verbose=verbose
        )
        
        # Run analysis
        analyzer = WhatIfAnalyzer(config)
        report = analyzer.analyze_function(func)
        
        # Print report
        console.print(report)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)

def _import_function(module_path: str, function_name: str) -> callable:
    """Import a function from a module."""
    try:
        module = importlib.import_module(module_path)
        func = getattr(module, function_name)
        if not callable(func):
            raise ValueError(f"{function_name} is not a function")
        return func
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Could not import function {function_name} from {module_path}: {e}")

def _import_from_file(file_path: str) -> callable:
    """Import a function from a Python file."""
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")
        
        # Add the file's directory to sys.path
        sys.path.insert(0, str(file_path.parent))
        
        # Import the module
        module_name = file_path.stem
        module = importlib.import_module(module_name)
        
        # Find the first function in the module
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and not name.startswith('_'):
                return obj
        
        raise ValueError(f"No functions found in {file_path}")
    except Exception as e:
        raise ValueError(f"Error importing from file {file_path}: {e}")

def _import_module(module_path: str) -> callable:
    """Import a module and return its main function."""
    try:
        module = importlib.import_module(module_path)
        
        # Find the first function in the module
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and not name.startswith('_'):
                return obj
        
        raise ValueError(f"No functions found in module {module_path}")
    except ImportError as e:
        raise ValueError(f"Could not import module {module_path}: {e}")

def main():
    """Entry point for the CLI."""
    cli() 