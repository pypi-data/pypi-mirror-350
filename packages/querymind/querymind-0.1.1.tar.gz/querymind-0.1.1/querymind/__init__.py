"""
AI-Pandas-Query - Ask Your Data in English
"""

__version__ = "0.1.0"

from .core import AIQuery, AIQueryError, DataFrameError, CodeExecutionError

__all__ = ["AIQuery", "AIQueryError", "DataFrameError", "CodeExecutionError"] 