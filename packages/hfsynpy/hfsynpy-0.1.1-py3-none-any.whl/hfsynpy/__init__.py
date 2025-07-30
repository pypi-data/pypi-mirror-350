# This file marks the directory as a Python package.
__version__ = "0.1.1"
__author__ = "Dominik Mair"
__description__ = "Synthesis and analysis tools for high frequency components (microstrip transmission lines)."

from .hfsynpy import MicrostripAnalysisResult, MicrostripSynthesisResult

__all__ = ["MicrostripAnalysisResult", "MicrostripSynthesisResult"]
