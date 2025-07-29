"""
Core analyzer module for WhatIF Analyzer.
"""

import functools
import inspect
import logging
import random
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

from whatif_analyzer.edge_cases import EdgeCase, generate_edge_cases
from whatif_analyzer.report import AnalysisReport, TestResult
from whatif_analyzer.type_inference import infer_parameter_types

logger = logging.getLogger(__name__)

@dataclass
class AnalyzerConfig:
    """Configuration for the WhatIF Analyzer."""
    enable_fuzzing: bool = True
    max_fuzz_cases: int = 50
    timeout_seconds: int = 5
    verbose: bool = False
    random_seed: Optional[int] = None

class WhatIfAnalyzer:
    """Main analyzer class for generating and running what-if scenarios."""
    
    def __init__(self, config: Optional[AnalyzerConfig] = None):
        """Initialize the analyzer with optional configuration."""
        self.config = config or AnalyzerConfig()
        if self.config.random_seed is not None:
            random.seed(self.config.random_seed)
        
        if self.config.verbose:
            logging.basicConfig(level=logging.INFO)
    
    def analyze_function(
        self,
        func: Callable,
        custom_edge_cases: Optional[List[EdgeCase]] = None,
    ) -> AnalysisReport:
        """
        Analyze a function by running it with various edge cases.
        
        Args:
            func: The function to analyze
            custom_edge_cases: Optional list of custom edge cases to test
            
        Returns:
            AnalysisReport containing the results of the analysis
        """
        # Get function signature and parameter types
        sig = inspect.signature(func)
        param_types = infer_parameter_types(func)
        
        # Generate edge cases for each parameter
        all_edge_cases = []
        for param_name, param_type in param_types.items():
            param_edge_cases = generate_edge_cases(param_type)
            all_edge_cases.append((param_name, param_edge_cases))
        
        # Add custom edge cases if provided
        if custom_edge_cases:
            all_edge_cases.extend(custom_edge_cases)
        
        # Run tests and collect results
        results: List[TestResult] = []
        start_time = time.time()
        
        for param_name, edge_cases in all_edge_cases:
            for edge_case in edge_cases:
                if time.time() - start_time > self.config.timeout_seconds:
                    logger.warning("Analysis timeout reached")
                    break
                
                try:
                    # Create test arguments
                    test_args = self._prepare_test_args(sig, param_name, edge_case)
                    
                    # Run the test
                    result = self._run_test(func, test_args, edge_case)
                    results.append(result)
                    
                except Exception as e:
                    logger.error(f"Error running test case: {e}")
                    results.append(TestResult(
                        edge_case=edge_case,
                        success=False,
                        error=str(e),
                        output=None
                    ))
        
        # Generate fuzzing cases if enabled
        if self.config.enable_fuzzing:
            fuzz_results = self._run_fuzzing(func, param_types)
            results.extend(fuzz_results)
        
        return AnalysisReport(
            function_name=func.__name__,
            parameter_types=param_types,
            results=results
        )
    
    def _prepare_test_args(
        self,
        sig: inspect.Signature,
        target_param: str,
        edge_case: EdgeCase
    ) -> Dict[str, Any]:
        """Prepare arguments for a test case."""
        args = {}
        for param_name, param in sig.parameters.items():
            if param_name == target_param:
                args[param_name] = edge_case.value
            else:
                # Use default value or a simple default based on type
                if param.default is not inspect.Parameter.empty:
                    args[param_name] = param.default
                else:
                    args[param_name] = self._get_default_value(param.annotation)
        return args
    
    def _get_default_value(self, annotation: Any) -> Any:
        """Get a sensible default value based on type annotation."""
        if annotation == int:
            return 0
        elif annotation == float:
            return 0.0
        elif annotation == str:
            return ""
        elif annotation == list:
            return []
        elif annotation == dict:
            return {}
        elif annotation == bool:
            return False
        return None
    
    def _run_test(
        self,
        func: Callable,
        args: Dict[str, Any],
        edge_case: EdgeCase
    ) -> TestResult:
        """Run a single test case."""
        try:
            output = func(**args)
            return TestResult(
                edge_case=edge_case,
                success=True,
                error=None,
                output=output
            )
        except Exception as e:
            return TestResult(
                edge_case=edge_case,
                success=False,
                error=str(e),
                output=None
            )
    
    def _run_fuzzing(
        self,
        func: Callable,
        param_types: Dict[str, Type]
    ) -> List[TestResult]:
        """Run fuzzing tests on the function."""
        results = []
        for _ in range(self.config.max_fuzz_cases):
            try:
                # Generate random arguments based on parameter types
                args = {
                    name: self._generate_random_value(type_)
                    for name, type_ in param_types.items()
                }
                
                # Run the test
                output = func(**args)
                results.append(TestResult(
                    edge_case=EdgeCase("fuzzing", None),
                    success=True,
                    error=None,
                    output=output
                ))
            except Exception as e:
                results.append(TestResult(
                    edge_case=EdgeCase("fuzzing", None),
                    success=False,
                    error=str(e),
                    output=None
                ))
        return results
    
    def _generate_random_value(self, type_: Type) -> Any:
        """Generate a random value of the given type."""
        if type_ == int:
            return random.randint(-1000, 1000)
        elif type_ == float:
            return random.uniform(-1000.0, 1000.0)
        elif type_ == str:
            length = random.randint(0, 20)
            return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))
        elif type_ == list:
            length = random.randint(0, 10)
            return [self._generate_random_value(int) for _ in range(length)]
        elif type_ == dict:
            length = random.randint(0, 5)
            return {
                self._generate_random_value(str): self._generate_random_value(int)
                for _ in range(length)
            }
        elif type_ == bool:
            return random.choice([True, False])
        return None

def analyze(
    func: Optional[Callable] = None,
    **config_kwargs
) -> Union[Callable, Any]:
    """
    Decorator for analyzing functions with what-if scenarios.
    
    Usage:
        @analyze
        def my_function(x: int, y: str) -> bool:
            return len(y) > x
            
        # Or with configuration:
        @analyze(enable_fuzzing=True, max_fuzz_cases=100)
        def another_function(a: float, b: float) -> float:
            return a / b
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            config = AnalyzerConfig(**config_kwargs)
            analyzer = WhatIfAnalyzer(config)
            report = analyzer.analyze_function(func)
            
            if config.verbose:
                print(report)
            
            return func(*args, **kwargs)
        return wrapper
    
    if func is None:
        return decorator
    return decorator(func) 