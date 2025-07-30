"""
Genesis Studio integration for ML Observability.

This module provides integration with Genesis Studio service, enabling tracing
and monitoring of Genesis Studio agent execution without direct MLflow imports.
"""

from ml_observability.integrations.genesis_studio.tracer import MLObservabilityTracer

__all__ = ["MLObservabilityTracer"]
