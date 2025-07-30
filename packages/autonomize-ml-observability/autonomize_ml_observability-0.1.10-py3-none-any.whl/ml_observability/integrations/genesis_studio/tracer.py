"""
Genesis Studio tracer for ML Observability.

This module provides a custom tracer implementation for Genesis Studio that integrates with
ML Observability to track agent execution, LLM calls, and tool usage without requiring
direct MLflow imports in the Genesis Studio service.
"""
import os
import uuid
from typing import Any, Dict, List, Optional, Union

from ml_observability.observability.tracing import AgentTracer, AgentSpanType
from ml_observability.observability.cost_tracking import CostTracker
from ml_observability.utils import setup_logger

logger = setup_logger(__name__)

# Mapping between Genesis Studio trace types and ML Observability span types
SPAN_TYPE_MAPPING = {
    "agent": AgentSpanType.AGENT,
    "chain": AgentSpanType.STEP,
    "llm": AgentSpanType.LLM,
    "tool": AgentSpanType.TOOL,
    "retriever": AgentSpanType.RETRIEVER,
    "chat_memory": AgentSpanType.STEP,
    "document_transformer": AgentSpanType.STEP,
    "embedding": AgentSpanType.STEP,
    "prompt": AgentSpanType.STEP,
    "text_splitter": AgentSpanType.STEP,
}

class MLObservabilityTracer:
    """
    Tracer that integrates Genesis Studio with ML Observability.
    
    This tracer implements the BaseTracer interface expected by Genesis Studio's TracingService
    and connects it to ML Observability's AgentTracer and CostTracker.
    
    It handles:
    - Creating and managing traces for agent runs
    - Tracking individual steps within an agent run
    - Associating costs with LLM calls
    - Supporting Genesis Studio's event-based system
    - Providing LangChain callbacks for integration
    
    Example:
        ```python
        from ml_observability.integrations.genesis_studio import MLObservabilityTracer
        
        # Initialize the tracer
        tracer = MLObservabilityTracer()
        
        # Add it to the tracing service
        tracing_service._tracers["ml_observability"] = tracer
        ```
    """
    
    def __init__(self):
        """Initialize the tracer."""
        self._agent_tracer = AgentTracer()
        self._cost_tracker = CostTracker()
        self._spans = {}  # Map Genesis Studio trace/span IDs to ML Observability span IDs
        self._active_spans = {}  # Track active spans for LangChain callbacks
        self.ready = True
    
    def add_trace(self, trace_id: str, trace_name: str, trace_type: str, 
                 inputs: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None, 
                 vertex: Any = None) -> None:
        """
        Start a new trace.
        
        Args:
            trace_id: Unique identifier for the trace in Genesis Studio
            trace_name: Name of the trace
            trace_type: Type of the trace (agent, chain, etc.)
            inputs: Input data for the trace
            metadata: Additional metadata
            vertex: Genesis Studio vertex object (optional)
        """
        try:
            # Create a name for the MLflow run
            run_name = os.getenv("MLFLOW_RUN_NAME", trace_name)
            
            # Start a new trace in AgentTracer
            with self._agent_tracer.start_trace(name=run_name) as mlflow_run_id:
                # Map the Genesis Studio trace_id to the MLflow run_id and agent_tracer trace_id
                agent_tracer_trace_id = self._agent_tracer.current_trace_id
                self._spans[trace_id] = {
                    "mlflow_run_id": mlflow_run_id,
                    "agent_tracer_trace_id": agent_tracer_trace_id,
                    "type": trace_type
                }
                
                # Log inputs as attributes
                if inputs:
                    sanitized_inputs = self._sanitize_inputs(inputs)
                    self._agent_tracer.log_attributes(
                        trace_id=agent_tracer_trace_id,
                        attributes={"inputs": sanitized_inputs}
                    )
                
                # Log metadata as attributes
                if metadata:
                    sanitized_metadata = self._sanitize_inputs(metadata)
                    self._agent_tracer.log_attributes(
                        trace_id=agent_tracer_trace_id,
                        attributes={"metadata": sanitized_metadata}
                    )
                
                # Log vertex info if provided
                if vertex:
                    vertex_info = {
                        "id": getattr(vertex, "id", "unknown"),
                        "type": getattr(vertex, "type", "unknown"),
                        "name": getattr(vertex, "name", "unknown")
                    }
                    self._agent_tracer.log_attributes(
                        trace_id=agent_tracer_trace_id,
                        attributes={"vertex": vertex_info}
                    )
                
                logger.debug(f"Started trace {trace_id} ({trace_name}) with MLflow run ID {mlflow_run_id}")
        except Exception as e:
            logger.exception(f"Error starting trace {trace_id}: {e}")
    
    def end_trace(self, trace_id: str, trace_name: str, outputs: Optional[Dict[str, Any]] = None, 
                 error: Optional[Exception] = None, logs: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        End a trace.
        
        Args:
            trace_id: Unique identifier for the trace in Genesis Studio
            trace_name: Name of the trace
            outputs: Output data from the trace
            error: Exception if the trace ended with an error
            logs: Logs collected during the trace
        """
        try:
            if trace_id not in self._spans:
                logger.warning(f"Attempted to end unknown trace: {trace_id}")
                return
                
            span_info = self._spans[trace_id]
            agent_tracer_trace_id = span_info.get("agent_tracer_trace_id")
            
            # Log outputs as attributes
            if outputs:
                sanitized_outputs = self._sanitize_inputs(outputs)
                self._agent_tracer.log_attributes(
                    trace_id=agent_tracer_trace_id,
                    attributes={"outputs": sanitized_outputs}
                )
            
            # Log error if present
            if error:
                self._agent_tracer.log_attributes(
                    trace_id=agent_tracer_trace_id,
                    attributes={"error": str(error), "error_type": type(error).__name__}
                )
            
            # Log any additional logs
            if logs:
                self._agent_tracer.log_attributes(
                    trace_id=agent_tracer_trace_id,
                    attributes={"logs": logs}
                )
            
            # End the trace in AgentTracer
            self._agent_tracer.end_trace(agent_tracer_trace_id)
            
            # Clean up
            del self._spans[trace_id]
            logger.debug(f"Ended trace {trace_id} ({trace_name})")
        except Exception as e:
            logger.exception(f"Error ending trace {trace_id}: {e}")
    
    def create_span(self, trace_id: str, name: str, span_type: str, 
                   inputs: Optional[Dict[str, Any]] = None, 
                   metadata: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Create a span within a trace.
        
        Args:
            trace_id: Unique identifier for the parent trace in Genesis Studio
            name: Name of the span
            span_type: Type of the span (agent, llm, tool, etc.)
            inputs: Input data for the span
            metadata: Additional metadata
            
        Returns:
            str: Unique identifier for the span in Genesis Studio
        """
        try:
            if trace_id not in self._spans:
                logger.warning(f"Attempted to create span in unknown trace: {trace_id}")
                return None
                
            span_info = self._spans[trace_id]
            mlflow_run_id = span_info.get("mlflow_run_id")
            
            # Map Genesis Studio span type to ML Observability span type
            ml_obs_span_type = SPAN_TYPE_MAPPING.get(span_type, AgentSpanType.STEP)
            
            # Sanitize inputs for logging
            sanitized_inputs = self._sanitize_inputs(inputs) if inputs else None
            
            # Start a span in AgentTracer
            agent_tracer_span_id = self._agent_tracer.start_span(
                name=name,
                span_type=ml_obs_span_type,
                inputs=sanitized_inputs,
                attributes=metadata
            )
            
            # Generate a unique ID for the Genesis Studio sub-span
            genesis_studio_sub_span_id = f"{trace_id}_{name}_{uuid.uuid4()}"
            
            # Map the Genesis Studio sub-span ID to the AgentTracer span ID
            self._spans[genesis_studio_sub_span_id] = {
                "agent_tracer_span_id": agent_tracer_span_id,
                "mlflow_run_id": mlflow_run_id,
                "type": span_type
            }
            
            logger.debug(f"Created span {genesis_studio_sub_span_id} ({name}) of type {span_type}")
            return genesis_studio_sub_span_id
        except Exception as e:
            logger.exception(f"Error creating span in trace {trace_id}: {e}")
            return None
    
    def end_span(self, span_id: str, outputs: Optional[Dict[str, Any]] = None, 
                error: Optional[Exception] = None) -> None:
        """
        End a span.
        
        Args:
            span_id: Unique identifier for the span in Genesis Studio
            outputs: Output data from the span
            error: Exception if the span ended with an error
        """
        try:
            if span_id not in self._spans:
                logger.warning(f"Attempted to end unknown span: {span_id}")
                return
                
            span_info = self._spans[span_id]
            agent_tracer_span_id = span_info.get("agent_tracer_span_id")
            
            # Sanitize outputs for logging
            sanitized_outputs = self._sanitize_inputs(outputs) if outputs else None
            
            # End the span in AgentTracer
            self._agent_tracer.end_span(
                agent_tracer_span_id,
                outputs=sanitized_outputs,
                error=error
            )
            
            # Clean up
            del self._spans[span_id]
            logger.debug(f"Ended span {span_id}")
        except Exception as e:
            logger.exception(f"Error ending span {span_id}: {e}")
    
    def create_agent_span(self, trace_id: str, name: str, 
                         inputs: Optional[Dict[str, Any]] = None, 
                         metadata: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Create an agent span.
        
        Args:
            trace_id: Unique identifier for the parent trace in Genesis Studio
            name: Name of the span
            inputs: Input data for the span
            metadata: Additional metadata
            
        Returns:
            str: Unique identifier for the span in Genesis Studio
        """
        return self.create_span(trace_id, name, "agent", inputs, metadata)
    
    def get_langchain_callback(self):
        """
        Get a LangChain callback handler that integrates with ML Observability.
        
        Returns:
            MLObservabilityCallbackHandler: A callback handler for LangChain
        """
        from ml_observability.integrations.langchain.callbacks import MLObservabilityCallbackHandler
        
        # Create a callback handler with the current run name
        callback = MLObservabilityCallbackHandler(
            run_name=os.getenv("MLFLOW_RUN_NAME", "genesis-studio-run"),
            agent_tracing=True
        )
        
        return callback
    
    def monitor_llm_client(self, client):
        """
        Monitor an LLM client for cost tracking.
        
        Args:
            client: The LLM client to monitor
        """
        from ml_observability.observability.monitor import monitor
        
        # Detect client type
        client_name = client.__class__.__name__.lower()
        client_module = client.__class__.__module__.lower()
        
        # Determine provider
        provider = None
        if "azure" in client_name or "azure" in client_module:
            provider = "azure_openai"
        elif "openai" in client_name or "openai" in client_module:
            provider = "openai"
        elif "anthropic" in client_name or "anthropic" in client_module:
            provider = "anthropic"
        
        # Monitor the client
        if provider:
            monitor(client, provider=provider)
            logger.debug(f"Monitoring enabled for {provider} client")
        else:
            logger.warning(f"Unable to determine provider for client: {client.__class__.__name__}")
    
    def _sanitize_inputs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize inputs for logging.
        
        Args:
            data: Input data to sanitize
            
        Returns:
            Dict[str, Any]: Sanitized data
        """
        if not data:
            return {}
            
        result = {}
        for key, value in data.items():
            # Skip API keys and sensitive information
            if "api_key" in key.lower() or "secret" in key.lower() or "password" in key.lower():
                result[key] = "********"
            # Truncate large values
            elif isinstance(value, str) and len(value) > 1000:
                result[key] = value[:1000] + "... [truncated]"
            # Handle nested dictionaries
            elif isinstance(value, dict):
                result[key] = self._sanitize_inputs(value)
            # Handle lists
            elif isinstance(value, list) and len(value) > 0:
                if isinstance(value[0], dict):
                    result[key] = [self._sanitize_inputs(item) if isinstance(item, dict) else item for item in value[:10]]
                    if len(value) > 10:
                        result[key].append("... [truncated]")
                else:
                    result[key] = value[:10]
                    if len(value) > 10:
                        result[key].append("... [truncated]")
            else:
                result[key] = value
        return result
    
    def _sanitize_mlflow_key(self, key: str) -> str:
        """
        Sanitize keys for MLflow compatibility.
        
        Args:
            key: Key to sanitize
            
        Returns:
            str: Sanitized key
        """
        import re
        # MLflow only allows alphanumerics, underscores, dashes, periods, spaces, colons, and slashes
        return re.sub(r'[^a-zA-Z0-9_\-\.\s:/]', '_', str(key))
