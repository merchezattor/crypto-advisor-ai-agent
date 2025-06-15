"""
Crypto Advisor - An AI-powered market analysis agent for cryptocurrency insights.

This package provides tools for analyzing cryptocurrency markets using LangChain
and various data providers.
"""

__version__ = "0.1.0"

# Ensure compatibility with libraries expecting `numpy.NaN` alias removed in NumPy 2.0+
import numpy as np

# NumPy 2.0 removed the `NaN` constant. Some third-party packages (e.g. pandas_ta)
# still perform `from numpy import NaN`.  Re-introduce this alias early so that the
# import does not break during test discovery or runtime.
if not hasattr(np, "NaN"):
    np.NaN = np.nan  # type: ignore[attr-defined]

# ---------------------------------------------------------------------------

__all__: list[str] = ["__version__"]
