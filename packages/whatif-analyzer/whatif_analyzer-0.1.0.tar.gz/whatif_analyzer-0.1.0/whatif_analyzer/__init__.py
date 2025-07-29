"""
WhatIF Analyzer - A Python package for analyzing functions with what-if scenarios.
"""

from whatif_analyzer.analyzer import WhatIfAnalyzer, analyze
from whatif_analyzer.edge_cases import EdgeCase
from whatif_analyzer.report import AnalysisReport

__version__ = "0.1.0"
__all__ = ["WhatIfAnalyzer", "analyze", "EdgeCase", "AnalysisReport"] 