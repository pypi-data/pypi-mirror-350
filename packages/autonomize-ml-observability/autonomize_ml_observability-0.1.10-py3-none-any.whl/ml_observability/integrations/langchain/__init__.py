"""
LangChain integration for ML Observability.

This package provides integration with LangChain for tracking agent executions,
LLM calls, and tool usage.
"""

from ml_observability.integrations.langchain.callbacks import MLObservabilityCallbackHandler

__all__ = ["MLObservabilityCallbackHandler"]
