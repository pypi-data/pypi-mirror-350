"""
LangChain callback handler for ML Observability.

This module provides a callback handler for LangChain that integrates with
ML Observability to track agent executions, LLM calls, and tool usage.
"""

import os
import uuid
from typing import Any, Dict, List, Optional, Union

from langchain.callbacks.base import BaseCallbackHandler

from ml_observability.core.credential import ModelhubCredential
from ml_observability.observability.tracing import AgentTracer
from ml_observability.observability.cost_tracking import CostTracker


class MLObservabilityCallbackHandler(BaseCallbackHandler):
    """
    Callback handler for LangChain that integrates with ML Observability.
    
    This callback handler tracks agent executions, LLM calls, and tool usage
    in LangChain, and logs them to ML Observability for monitoring and analysis.
    It is designed to work seamlessly with LangFlow's event-based system.
    
    Example:
        ```python
        from langchain.agents import initialize_agent, Tool
        from langchain.llms import OpenAI
        from ml_observability.integrations.langchain.callbacks import MLObservabilityCallbackHandler
        
        # Create a callback handler
        callback = MLObservabilityCallbackHandler(
            experiment_name="my_experiment",
            agent_tracing=True
        )
        
        # Create an agent with the callback
        llm = OpenAI(temperature=0)
        tools = [...]
        agent = initialize_agent(
            tools, 
            llm, 
            agent="zero-shot-react-description", 
            callbacks=[callback]
        )
        
        # Run the agent
        agent.run("What is the weather in San Francisco?")
        ```
    """
    
    def __init__(
        self,
        experiment_name: Optional[str] = None,
        credential: Optional[ModelhubCredential] = None,
        agent_tracing: bool = True,
        run_name: Optional[str] = None,
    ):
        """
        Initialize the callback handler.
        
        Args:
            experiment_name: The name of the experiment to log to
            credential: Optional ModelhubCredential for authentication
            agent_tracing: Whether to enable agent tracing
            run_name: Optional name for the run
        """
        super().__init__()
        
        # Initialize agent tracer
        self.agent_tracer = AgentTracer() if agent_tracing else None
        
        # Initialize cost tracker
        self.cost_tracker = CostTracker()
        
        # Set experiment name and run name
        self.experiment_name = experiment_name or os.getenv("MLFLOW_EXPERIMENT_NAME", "langchain")
        self.run_name = run_name or os.getenv("MLFLOW_RUN_NAME", f"langchain-run-{uuid.uuid4()}")
        
        # Set credential
        self.credential = credential
        
        # Track active spans
        self._active_spans = {}
        self._active_chains = {}
        self._active_agents = {}
        self._active_tools = {}
        
        # Track parent-child relationships
        self._parent_map = {}
        
        # Track whether we're in an agent run
        self.in_agent_run = False
        
    def _get_span_id(self, run_id: str) -> str:
        """Get a span ID for a run."""
        return str(run_id)
    
    def _get_parent_span_id(self, run_id: str) -> Optional[str]:
        """Get the parent span ID for a run."""
        return self._parent_map.get(run_id)
    
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Called when an LLM starts running."""
        run_id = kwargs.get("run_id", str(uuid.uuid4()))
        parent_run_id = kwargs.get("parent_run_id")
        
        # Set parent-child relationship
        if parent_run_id:
            self._parent_map[run_id] = parent_run_id
            
        # Get span type and name
        span_type = "LLM"
        model_name = serialized.get("name", "unknown_model")
        span_name = f"llm_{model_name}"
        
        # Create inputs
        inputs = {
            "prompts": prompts,
            "model": model_name,
            **serialized
        }
        
        # Start span in agent tracer
        if self.agent_tracer:
            parent_span_id = self._get_parent_span_id(run_id)
            span_id = self.agent_tracer.start_span(
                name=span_name,
                span_type=span_type,
                parent_id=parent_span_id,
                attributes=inputs
            )
            self._active_spans[run_id] = span_id
    
    def on_llm_end(self, response, **kwargs: Any) -> None:
        """Called when an LLM ends running."""
        run_id = kwargs.get("run_id", "")
        
        # Get outputs
        outputs = {"response": response}
        
        # End span in agent tracer
        if self.agent_tracer and run_id in self._active_spans:
            span_id = self._active_spans[run_id]
            self.agent_tracer.end_span(span_id, attributes=outputs)
            del self._active_spans[run_id]
            
        # Track cost if available
        if hasattr(response, "llm_output") and response.llm_output:
            if "token_usage" in response.llm_output:
                token_usage = response.llm_output["token_usage"]
                model_name = kwargs.get("serialized", {}).get("name", "unknown_model")
                
                # Track cost
                self.cost_tracker.track_cost(
                    model_name=model_name,
                    input_tokens=token_usage.get("prompt_tokens", 0),
                    output_tokens=token_usage.get("completion_tokens", 0)
                )
    
    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        """Called when an LLM errors."""
        run_id = kwargs.get("run_id", "")
        
        # End span in agent tracer with error
        if self.agent_tracer and run_id in self._active_spans:
            span_id = self._active_spans[run_id]
            self.agent_tracer.end_span(span_id, error=error)
            del self._active_spans[run_id]
    
    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Called when a chain starts running."""
        run_id = kwargs.get("run_id", str(uuid.uuid4()))
        parent_run_id = kwargs.get("parent_run_id")
        
        # Set parent-child relationship
        if parent_run_id:
            self._parent_map[run_id] = parent_run_id
            
        # Get span type and name
        chain_type = serialized.get("name", "")
        is_agent = "Agent" in chain_type
        
        if is_agent:
            span_type = "AGENT"
            span_name = f"agent_{chain_type}"
            self.in_agent_run = True
            self._active_agents[run_id] = True
        else:
            span_type = "STEP"
            span_name = f"chain_{chain_type}"
            
        # Create inputs
        span_inputs = {
            "inputs": inputs,
            "chain_type": chain_type,
            **serialized
        }
        
        # Start span in agent tracer
        if self.agent_tracer:
            parent_span_id = self._get_parent_span_id(run_id)
            span_id = self.agent_tracer.start_span(
                name=span_name,
                span_type=span_type,
                parent_id=parent_span_id,
                attributes=span_inputs
            )
            self._active_spans[run_id] = span_id
            self._active_chains[run_id] = span_id
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Called when a chain ends running."""
        run_id = kwargs.get("run_id", "")
        
        # Check if this is an agent run
        is_agent = run_id in self._active_agents
        
        # End span in agent tracer
        if self.agent_tracer and run_id in self._active_spans:
            span_id = self._active_spans[run_id]
            self.agent_tracer.end_span(span_id, attributes=outputs)
            del self._active_spans[run_id]
            
            if run_id in self._active_chains:
                del self._active_chains[run_id]
                
            if is_agent:
                self.in_agent_run = False
                del self._active_agents[run_id]
    
    def on_chain_error(self, error: Exception, **kwargs: Any) -> None:
        """Called when a chain errors."""
        run_id = kwargs.get("run_id", "")
        
        # Check if this is an agent run
        is_agent = run_id in self._active_agents
        
        # End span in agent tracer with error
        if self.agent_tracer and run_id in self._active_spans:
            span_id = self._active_spans[run_id]
            self.agent_tracer.end_span(span_id, error=error)
            del self._active_spans[run_id]
            
            if run_id in self._active_chains:
                del self._active_chains[run_id]
                
            if is_agent:
                self.in_agent_run = False
                del self._active_agents[run_id]
    
    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Called when a tool starts running."""
        run_id = kwargs.get("run_id", str(uuid.uuid4()))
        parent_run_id = kwargs.get("parent_run_id")
        
        # Set parent-child relationship
        if parent_run_id:
            self._parent_map[run_id] = parent_run_id
            
        # Get span type and name
        span_type = "TOOL"
        tool_name = serialized.get("name", "unknown_tool")
        span_name = f"tool_{tool_name}"
        
        # Create inputs
        inputs = {
            "input": input_str,
            "tool_name": tool_name,
            **serialized
        }
        
        # Start span in agent tracer
        if self.agent_tracer:
            parent_span_id = self._get_parent_span_id(run_id)
            span_id = self.agent_tracer.start_span(
                name=span_name,
                span_type=span_type,
                parent_id=parent_span_id,
                attributes=inputs
            )
            self._active_spans[run_id] = span_id
            self._active_tools[run_id] = span_id
    
    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Called when a tool ends running."""
        run_id = kwargs.get("run_id", "")
        
        # End span in agent tracer
        if self.agent_tracer and run_id in self._active_spans:
            span_id = self._active_spans[run_id]
            self.agent_tracer.end_span(span_id, attributes={"output": output})
            del self._active_spans[run_id]
            
            if run_id in self._active_tools:
                del self._active_tools[run_id]
    
    def on_tool_error(self, error: Exception, **kwargs: Any) -> None:
        """Called when a tool errors."""
        run_id = kwargs.get("run_id", "")
        
        # End span in agent tracer with error
        if self.agent_tracer and run_id in self._active_spans:
            span_id = self._active_spans[run_id]
            self.agent_tracer.end_span(span_id, error=error)
            del self._active_spans[run_id]
            
            if run_id in self._active_tools:
                del self._active_tools[run_id]
    
    def on_text(self, text: str, **kwargs: Any) -> None:
        """Called when text is generated."""
        run_id = kwargs.get("run_id", "")
        
        # Log text as an attribute if we have an active span
        if self.agent_tracer and run_id in self._active_spans:
            span_id = self._active_spans[run_id]
            self.agent_tracer.log_span_attributes(span_id, {"generated_text": text})
    
    def on_agent_action(self, action, **kwargs: Any) -> Any:
        """Called when an agent takes an action.
        
        Args:
            action: The action taken by the agent (AgentAction object)
            **kwargs: Additional keyword arguments
        """
        run_id = kwargs.get("run_id", str(uuid.uuid4()))
        parent_run_id = kwargs.get("parent_run_id")
        
        # Set parent-child relationship
        if parent_run_id:
            self._parent_map[run_id] = parent_run_id
        
        # Extract action details
        tool = getattr(action, "tool", "unknown_tool")
        tool_input = getattr(action, "tool_input", "")
        log = getattr(action, "log", "")
        
        # Create inputs
        inputs = {
            "tool": tool,
            "tool_input": tool_input,
            "log": log,
        }
        
        # Start span in agent tracer
        if self.agent_tracer:
            parent_span_id = self._get_parent_span_id(run_id)
            span_id = self.agent_tracer.start_span(
                name=f"agent_action_{tool}",
                span_type="AGENT_ACTION",
                parent_span_id=parent_span_id,
                inputs=inputs
            )
            self._active_spans[run_id] = span_id
    
    def on_agent_finish(self, finish, **kwargs: Any) -> Any:
        """Called when an agent finishes execution.
        
        Args:
            finish: The finish object (AgentFinish)
            **kwargs: Additional keyword arguments
        """
        run_id = kwargs.get("run_id", "")
        
        # Extract finish details
        output = getattr(finish, "return_values", {})
        log = getattr(finish, "log", "")
        
        # Create outputs
        outputs = {
            "output": output,
            "log": log,
        }
        
        # End span in agent tracer
        if self.agent_tracer and run_id in self._active_spans:
            span_id = self._active_spans[run_id]
            self.agent_tracer.end_span(span_id, outputs=outputs)
            del self._active_spans[run_id]
