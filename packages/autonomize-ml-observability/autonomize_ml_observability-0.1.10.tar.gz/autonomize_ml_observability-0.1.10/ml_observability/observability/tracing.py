"""
This module provides tracing capabilities for agent workflows in ML applications.

It includes functionality for:
- Creating and managing traces for agent runs
- Tracking individual steps within an agent run
- Supporting different types of steps (LLM calls, tool executions, etc.)
- Integrating with MLflow for visualization and analysis
"""
import functools
import logging
import time
from contextlib import contextmanager
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

import mlflow
from mlflow.entities import SpanType

from ml_observability.utils import setup_logger

logger = setup_logger(__name__)

class AgentSpanType(str, Enum):
    """Enum for agent span types."""
    AGENT = "AGENT"
    STEP = "STEP"
    LLM = "LLM"
    TOOL = "TOOL"
    RETRIEVER = "RETRIEVER"
    CUSTOM = "CUSTOM"

class AgentTracer:
    """
    Manages tracing for agent workflows.
    
    This class provides functionality to:
    - Create and manage traces for agent runs
    - Track individual steps within an agent run
    - Associate costs with specific steps
    - Generate trace summaries and visualizations
    - Support nested spans and hierarchical tracing
    """
    
    def __init__(self):
        self.active_spans = {}
        self.current_trace_id = None
        self.parent_span_map = {}  # Maps span IDs to their parent span IDs
    
    @contextmanager
    def start_trace(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """Start a new trace for an agent run.
        
        Args:
            name (str): Name of the trace
            attributes (Optional[Dict[str, Any]], optional): Attributes to associate with the trace.
                
        Yields:
            str: The trace ID
        """
        with mlflow.start_run(run_name=name) as run:
            trace_id = run.info.run_id
            self.current_trace_id = trace_id
            
            # Log trace attributes
            if attributes:
                for key, value in attributes.items():
                    mlflow.set_tag(f"trace.{key}", value)
            
            mlflow.set_tag("trace.start_time", time.time())
            mlflow.set_tag("trace.type", "agent_run")
            
            try:
                yield trace_id
            finally:
                mlflow.set_tag("trace.end_time", time.time())
                self.current_trace_id = None
    
    @contextmanager
    def start_span(
        self, 
        name: str, 
        span_type: Union[AgentSpanType, str] = AgentSpanType.STEP,
        parent_span_id: Optional[str] = None,
        inputs: Optional[Dict[str, Any]] = None,
        attributes: Optional[Dict[str, Any]] = None
    ):
        """Start a new span within the current trace.
        
        Args:
            name (str): Name of the span
            span_type (Union[AgentSpanType, str], optional): Type of the span. Defaults to AgentSpanType.STEP.
            parent_span_id (Optional[str], optional): ID of the parent span. Defaults to None.
            inputs (Optional[Dict[str, Any]], optional): Inputs to the span. Defaults to None.
            attributes (Optional[Dict[str, Any]], optional): Attributes to associate with the span. Defaults to None.
                
        Yields:
            str: The span ID
        """
        if isinstance(span_type, AgentSpanType):
            span_type = span_type.value
            
        with mlflow.start_span(name=name, span_type=span_type) as span:
            span_id = span.span_id
            self.active_spans[span_id] = {
                "name": name,
                "type": span_type,
                "parent": parent_span_id,
                "start_time": time.time(),
                "attributes": attributes or {},
                "span": span
            }
            
            # Store parent relationship
            if parent_span_id:
                self.parent_span_map[span_id] = parent_span_id
            
            # Set inputs if provided
            if inputs:
                span.set_inputs(inputs)
                
            # Set attributes if provided
            if attributes:
                for key, value in attributes.items():
                    span.set_attribute(key, value)
            
            try:
                yield span_id
            finally:
                if span_id in self.active_spans:
                    self.active_spans[span_id]["end_time"] = time.time()
                    del self.active_spans[span_id]
                
    def log_attributes(self, trace_id: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None):
        """Log attributes for a trace or the current trace.
        
        Args:
            trace_id (Optional[str], optional): ID of the trace. Defaults to the current trace.
            attributes (Optional[Dict[str, Any]], optional): Attributes to log. Defaults to None.
        """
        if not attributes:
            return
            
        target_trace_id = trace_id or self.current_trace_id
        if not target_trace_id:
            logger.warning("No active trace to log attributes to")
            return
            
        # Log attributes to MLflow
        for key, value in attributes.items():
            mlflow.set_tag(f"trace.{key}", value)
    
    def log_span_attributes(self, span_id: str, attributes: Dict[str, Any]):
        """Log attributes for a span.
        
        Args:
            span_id (str): ID of the span
            attributes (Dict[str, Any]): Attributes to log
        """
        if not span_id or not attributes:
            return
            
        if span_id in self.active_spans:
            span_info = self.active_spans[span_id]
            span = span_info.get("span")
            if span:
                # Update the stored attributes
                span_info["attributes"].update(attributes)
                # Set attributes on the span
                for key, value in attributes.items():
                    span.set_attribute(key, value)
    
    def end_span(self, span_id: str, outputs: Optional[Dict[str, Any]] = None, error: Optional[Exception] = None):
        """End a span.
        
        Args:
            span_id (str): ID of the span
            outputs (Optional[Dict[str, Any]], optional): Output data from the span. Defaults to None.
            error (Optional[Exception], optional): Exception if the span ended with an error. Defaults to None.
        """
        if not span_id:
            return
            
        if span_id in self.active_spans:
            span_info = self.active_spans[span_id]
            span = span_info.get("span")
            
            if span:
                # Set outputs if provided
                if outputs:
                    try:
                        span.set_outputs(outputs)
                    except Exception as e:
                        logger.warning(f"Error setting outputs for span {span_id}: {e}")
                
                # Set error if present
                if error:
                    try:
                        span.set_status("ERROR", str(error))
                    except Exception as e:
                        logger.warning(f"Error setting error status for span {span_id}: {e}")
            
            # Record end time
            span_info["end_time"] = time.time()
            
            # Clean up
            del self.active_spans[span_id]
            if span_id in self.parent_span_map:
                del self.parent_span_map[span_id]
    
    def trace_function(
        self,
        name: Optional[str] = None,
        span_type: Union[AgentSpanType, str] = AgentSpanType.STEP,
        attributes: Optional[Dict[str, Any]] = None
    ):
        """Decorator to trace a function execution.
        
        Args:
            name (Optional[str], optional): Name of the span. Defaults to the function name.
            span_type (Union[AgentSpanType, str], optional): Type of the span. Defaults to AgentSpanType.STEP.
            attributes (Optional[Dict[str, Any]], optional): Attributes to associate with the span. Defaults to None.
                
        Returns:
            Callable: The decorated function
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                func_name = name or func.__name__
                
                # Create a safe representation of args and kwargs for logging
                safe_args = [str(arg)[:100] for arg in args]
                safe_kwargs = {k: str(v)[:100] for k, v in kwargs.items()}
                
                with self.start_span(
                    name=func_name,
                    span_type=span_type,
                    inputs={"args": safe_args, "kwargs": safe_kwargs},
                    attributes=attributes
                ) as span:
                    try:
                        result = func(*args, **kwargs)
                        # Create a safe representation of the result for logging
                        safe_result = str(result)[:100] if result is not None else None
                        span.set_outputs({"result": safe_result})
                        return result
                    except Exception as e:
                        span.set_status("ERROR", str(e))
                        raise
                        
            return wrapper
        return decorator

# Global instance
_agent_tracer = AgentTracer()

def get_tracer():
    """Get the global agent tracer instance."""
    return _agent_tracer

def trace_agent(name=None, attributes=None):
    """Decorator for tracing an entire agent run.
    
    Args:
        name (Optional[str], optional): Name of the trace. Defaults to the function name.
        attributes (Optional[Dict[str, Any]], optional): Attributes to associate with the trace. Defaults to None.
            
    Returns:
        Callable: The decorated function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            agent_name = name or func.__name__
            with _agent_tracer.start_trace(agent_name, attributes) as trace_id:
                return func(*args, **kwargs)
        return wrapper
    return decorator

def trace_step(name=None, step_type=AgentSpanType.STEP, attributes=None):
    """Decorator for tracing an individual step within an agent run.
    
    Args:
        name (Optional[str], optional): Name of the span. Defaults to the function name.
        step_type (Union[AgentSpanType, str], optional): Type of the step. Defaults to AgentSpanType.STEP.
        attributes (Optional[Dict[str, Any]], optional): Attributes to associate with the span. Defaults to None.
            
    Returns:
        Callable: The decorated function
    """
    return _agent_tracer.trace_function(name, step_type, attributes)

@contextmanager
def span(name, span_type=AgentSpanType.STEP, inputs=None, attributes=None):
    """Context manager for creating a span.
    
    Args:
        name (str): Name of the span
        span_type (Union[AgentSpanType, str], optional): Type of the span. Defaults to AgentSpanType.STEP.
        inputs (Optional[Dict[str, Any]], optional): Inputs to the span. Defaults to None.
        attributes (Optional[Dict[str, Any]], optional): Attributes to associate with the span. Defaults to None.
            
    Yields:
        str: The span ID
    """
    with _agent_tracer.start_span(name, span_type, inputs=inputs, attributes=attributes) as span_id:
        yield span_id
