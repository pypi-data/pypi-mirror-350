"""
Report generation module for WhatIF Analyzer.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

@dataclass
class TestResult:
    """Represents the result of a single test case."""
    edge_case: Any
    success: bool
    error: Optional[str]
    output: Any

@dataclass
class AnalysisReport:
    """Represents the complete analysis report for a function."""
    function_name: str
    parameter_types: Dict[str, Type]
    results: List[TestResult]
    
    def __str__(self) -> str:
        """Generate a string representation of the report."""
        console = Console()
        with console.capture() as capture:
            self._print_report(console)
        return capture.get()
    
    def _print_report(self, console: Console) -> None:
        """Print the report using rich formatting."""
        # Print header
        console.print(Panel(
            f"[bold blue]WhatIF Analysis Report[/bold blue]\n"
            f"[bold]Function:[/bold] {self.function_name}",
            title="Analysis Results",
            border_style="blue"
        ))
        
        # Print parameter types
        console.print("\n[bold]Parameter Types:[/bold]")
        param_table = Table(show_header=True, header_style="bold")
        param_table.add_column("Parameter")
        param_table.add_column("Type")
        
        for param, type_ in self.parameter_types.items():
            param_table.add_row(param, str(type_))
        
        console.print(param_table)
        
        # Print test results
        console.print("\n[bold]Test Results:[/bold]")
        results_table = Table(show_header=True, header_style="bold")
        results_table.add_column("Edge Case")
        results_table.add_column("Status")
        results_table.add_column("Details")
        
        for result in self.results:
            status = "[green]✓[/green]" if result.success else "[red]✗[/red]"
            details = result.error if not result.success else str(result.output)
            results_table.add_row(
                str(result.edge_case.name),
                status,
                details
            )
        
        console.print(results_table)
        
        # Print summary
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - passed_tests
        
        console.print("\n[bold]Summary:[/bold]")
        console.print(f"Total Tests: {total_tests}")
        console.print(f"Passed: [green]{passed_tests}[/green]")
        console.print(f"Failed: [red]{failed_tests}[/red]")
        
        # Print recommendations if there are failures
        if failed_tests > 0:
            console.print("\n[bold]Recommendations:[/bold]")
            for result in self.results:
                if not result.success:
                    console.print(f"- Handle case: {result.edge_case.name}")
                    if result.error:
                        console.print(f"  Error: {result.error}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the report to a dictionary."""
        return {
            "function_name": self.function_name,
            "parameter_types": {
                name: str(type_) for name, type_ in self.parameter_types.items()
            },
            "results": [
                {
                    "edge_case": {
                        "name": result.edge_case.name,
                        "value": str(result.edge_case.value)
                    },
                    "success": result.success,
                    "error": result.error,
                    "output": str(result.output) if result.output is not None else None
                }
                for result in self.results
            ]
        } 