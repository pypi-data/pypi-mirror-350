"""
This module provides monitoring and observability capabilities for LLM (Large Language Model) 
clients.
It includes functionality for cost tracking, MLflow integration, and client wrapping for various 
LLM providers like OpenAI, Azure OpenAI, and Anthropic.
"""
import os
import logging
from typing import Any, Dict, Optional, Union

import mlflow

from ml_observability.core import ModelhubCredential
from ml_observability.observability.cost_tracking import CostTracker
from ml_observability.core.mlflow_client import MLflowClient
from ml_observability.observability.tracing import (
    AgentSpanType,
    get_tracer,
    trace_agent,
    trace_step,
    span as tracing_span
)
from ml_observability.utils import setup_logger

logger = setup_logger(__name__)

# Global instances
_mlflow_client: Optional[MLflowClient] = None
_cost_tracker: CostTracker


def initialize(
    cost_rates: Optional[dict] = None,
    experiment_name: Optional[str] = None,
    credential: Optional[ModelhubCredential] = None,
):
    """
    Initialize the MLflowClient, Observability, and CostTracker.
    Must be called once at startup.

    Args:
        cost_rates (dict, optional): Dictionary of cost rates for different models
        experiment_name (str, optional): Name of the MLflow experiment
        credential (ModelhubCredential, optional): Modelhub credentials
    """
    global _mlflow_client, _cost_tracker
    
    # Check if MLFLOW_TRACKING_URI is set in environment
    mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    
    if mlflow_tracking_uri:
        # Use mlflow directly since tracking URI is already set
        logger.debug("Using MLflow directly with tracking URI: %s", mlflow_tracking_uri)
        _mlflow_client = None
    else:
        if not credential:
            # Create a ModelhubCredential instance using environment variables.
            credential = ModelhubCredential(
                modelhub_url=os.getenv("MODELHUB_BASE_URL"),
                client_id=os.getenv("MODELHUB_CLIENT_ID"),
                client_secret=os.getenv("MODELHUB_CLIENT_SECRET")
            )

        _mlflow_client = MLflowClient(
            credential=credential,
        )

    experiment_name = experiment_name or os.getenv("EXPERIMENT_NAME")
    if experiment_name:
        if _mlflow_client:
            _mlflow_client.set_experiment(experiment_name=experiment_name)
        else:
            mlflow.set_experiment(experiment_name)
    _cost_tracker = CostTracker(cost_rates=cost_rates)
    logger.debug("Observability system initialized.")


def monitor(
    client,
    provider: Optional[str] = None,
    cost_rates: Optional[dict] = None,
    experiment_name: Optional[str] = None,
    credential: Optional[ModelhubCredential] = None,
):
    """
    Enable monitoring on an LLM client.
    Supports multiple providers: 'openai', 'azure_openai', 'anthropic', etc.
    If provider is not provided, it is inferred from the client's module.

    Args:
        client: The LLM client to monitor
        provider (str, optional): The provider name (openai, azure_openai, anthropic)
        cost_rates (dict, optional): Dictionary of cost rates for different models
        experiment_name (str, optional): Name of the MLflow experiment
        credential (ModelhubCredential, optional): Modelhub credentials
    """
    initialize(
        cost_rates=cost_rates,
        experiment_name=experiment_name,
        credential=credential,
    )
    if provider is None:
        # Try checking the class name first.
        client_name = client.__class__.__name__.lower()
        if "azure" in client_name:
            provider = "azure_openai"
        elif "openai" in client_name:
            provider = "openai"
        elif "anthropic" in client_name:
            provider = "anthropic"
        else:
            # Fallback to module-based detection.
            mod = client.__class__.__module__.lower()
            if "openai" in mod and "azure" in mod:
                provider = "azure_openai"
            elif "openai" in mod:
                provider = "openai"
            elif "azure" in mod:
                provider = "azure_openai"
            elif "anthropic" in mod:
                provider = "anthropic"
            else:
                provider = "unknown"
                logger.warning(f"Could not determine provider for client {client.__class__.__name__}")

    logger.debug("Detected provider: %s", provider)

    if provider == "openai":
        wrap_openai(client)
    elif provider == "anthropic":
        wrap_anthropic(client)
    elif provider == "azure_openai":
        from ml_observability.observability.monitor_azure import wrap_azure_openai
        wrap_azure_openai(client)
    # TODO: Add support for other providers
    else:
        logger.warning(f"Monitoring not supported for provider: {provider}")


def wrap_openai(client):
    """
    Wraps an OpenAI client to enable monitoring and logging capabilities.
    
    This function intercepts the client's completion creation methods (both synchronous
    and asynchronous) to track costs, log parameters, and manage MLflow runs.

    Args:
        client: An instance of the OpenAI client to be wrapped.

    Returns:
        None. The function modifies the client instance in-place by wrapping its methods.
    """
    # Wrap synchronous completions.create
    if hasattr(client.chat, "completions") and hasattr(client.chat.completions, "create"):
        original_create = client.chat.completions.create

        def wrapped_create(*args, **kwargs):
            active = mlflow.active_run()
            logger.debug("Active run: %s", active)
            started_run = False
            if not active:
                run = mlflow.start_run(run_name="llm_call_auto")
                started_run = True
            else:
                run = active
            try:
                result = original_create(*args, **kwargs)
                logger.debug("result: %s", result)
                prompt_tokens = result.usage.prompt_tokens
                completion_tokens = result.usage.completion_tokens
                _cost_tracker.track_cost(
                    model_name=kwargs.get("model", "gpt-3.5-turbo"),
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    run_id=run.info.run_id
                )
                if _mlflow_client:
                    _mlflow_client.log_param("model", kwargs.get("model", "gpt-3.5-turbo"))
                else:
                    mlflow.log_param("model", kwargs.get("model", "gpt-3.5-turbo"))
                return result
            finally:
                if started_run:
                    mlflow.end_run()

        client.chat.completions.create = wrapped_create

    # Wrap asynchronous completions.create (create)
    if hasattr(client, "chat") and hasattr(client.chat, "completions"):
        # Check if the client is an AsyncOpenAI instance
        if hasattr(client.chat.completions, "create") and callable(
                client.chat.completions.create) and client.__class__.__name__ == "AsyncOpenAI":
            original_async_create = client.chat.completions.create

            async def wrapped_async_create(*args, **kwargs):
                active = mlflow.active_run()
                logger.debug("Active async run: %s", active)
                started_run = False
                if not active:
                    run = mlflow.start_run(run_name="async_llm_call_auto")
                    started_run = True
                else:
                    run = active

                try:
                    result = original_async_create(*args, **kwargs)
                    prompt_tokens = result.usage.prompt_tokens
                    completion_tokens = result.usage.completion_tokens
                    _cost_tracker.track_cost(
                        model_name=kwargs.get("model", "gpt-3.5-turbo"),
                        input_tokens=prompt_tokens,
                        output_tokens=completion_tokens,
                        run_id=run.info.run_id
                    )
                    if _mlflow_client:
                        _mlflow_client.log_param("model", kwargs.get("model", "gpt-3.5-turbo"))
                    else:
                        mlflow.log_param("model", kwargs.get("model", "gpt-3.5-turbo"))
                    return result
                finally:
                    if started_run:
                        mlflow.end_run()

            client.chat.completions.create = wrapped_async_create

    logger.debug("Monitoring enabled for OpenAI/AzureOpenAI client.")


def wrap_anthropic(client):
    """
    Wraps an Anthropic client to enable monitoring and logging capabilities.
    
    This function intercepts the client's message creation methods (both synchronous
    and asynchronous) to track costs, log parameters, and manage MLflow runs.

    Args:
        client: An instance of the Anthropic client to be wrapped.

    Returns:
        None. The function modifies the client instance in-place by wrapping its methods.
    """
    # Wrap synchronous messages.create.
    if hasattr(client, "messages") and hasattr(client.messages, "create"):
        original_create = client.messages.create

        def wrapped_create(*args, **kwargs):
            active = mlflow.active_run()
            started_run = False
            if not active:
                run = mlflow.start_run(run_name="llm_call_auto")
                started_run = True
            else:
                run = active
            try:
                result = original_create(*args, **kwargs)
                prompt_tokens = result.usage.input_tokens
                completion_tokens = result.usage.output_tokens
                _cost_tracker.track_cost(
                    model_name=kwargs.get("model", "anthropic-default"),
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    run_id=run.info.run_id
                )
                if _mlflow_client:
                    _mlflow_client.log_param("model", kwargs.get("model", "anthropic-default"))
                else:
                    mlflow.log_param("model", kwargs.get("model", "anthropic-default"))
                return result
            finally:
                if started_run:
                    mlflow.end_run()

        client.messages.create = wrapped_create

    # Wrap asynchronous messages.acreate if available.
    if hasattr(client, "messages") and hasattr(client.messages, "acreate"):
        original_acreate = client.messages.acreate

        async def wrapped_acreate(*args, **kwargs):
            active = mlflow.active_run()
            started_run = False
            if not active:
                run = mlflow.start_run(run_name="llm_call_auto")
                started_run = True
            else:
                run = active
            try:
                result = await original_acreate(*args, **kwargs)
                prompt_tokens = result.usage.input_tokens
                completion_tokens = result.usage.output_tokens
                _cost_tracker.track_cost(
                    model_name=kwargs.get("model", "anthropic-default"),
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    run_id=run.info.run_id
                )
                if _mlflow_client:
                    _mlflow_client.log_param("model", kwargs.get("model", "anthropic-default"))
                else:
                    mlflow.log_param("model", kwargs.get("model", "anthropic-default"))
                return result
            finally:
                if started_run:
                    mlflow.end_run()

        client.messages.acreate = wrapped_acreate

    logger.debug("Monitoring enabled for Anthropics client.")


def agent(name=None, attributes=None):
    """
    Decorator for agent functions.
    Automatically wraps the function execution in an MLflow run and trace.
    
    Args:
        name (Optional[str], optional): Name of the agent run. Defaults to the function name.
        attributes (Optional[Dict[str, Any]], optional): Attributes to associate with the agent run. Defaults to None.
            
    Returns:
        Callable: The decorated function
    """
    return trace_agent(name, attributes)


def tool(name=None, attributes=None):
    """
    Decorator for tool functions.
    Automatically wraps the function execution in a span with type TOOL.
    
    Args:
        name (Optional[str], optional): Name of the tool. Defaults to the function name.
        attributes (Optional[Dict[str, Any]], optional): Attributes to associate with the tool execution. Defaults to None.
            
    Returns:
        Callable: The decorated function
    """
    return trace_step(name, AgentSpanType.TOOL, attributes)


class Identify:
    """
    A simple context manager for setting user context (if needed).
    """

    def __init__(self, user_props=None):
        self.user_props = user_props

    def __enter__(self):
        # Set user context here if desired.
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clear user context.
        pass


def identify(user_props=None):
    """
    Creates and returns an Identify context manager for setting user context.
    
    Args:
        user_props (dict, optional): Dictionary containing user properties to be set
            during the context. Defaults to None.
    
    Returns:
        Identify: A context manager instance that handles user context.
    """
    return Identify(user_props)


def agent_step(name=None, step_type=AgentSpanType.STEP, attributes=None):
    """
    Decorator for individual steps within an agent.
    Automatically wraps the function execution in a span with the specified type.
    
    Args:
        name (Optional[str], optional): Name of the step. Defaults to the function name.
        step_type (Union[AgentSpanType, str], optional): Type of the step. Defaults to AgentSpanType.STEP.
        attributes (Optional[Dict[str, Any]], optional): Attributes to associate with the step. Defaults to None.
            
    Returns:
        Callable: The decorated function
    """
    return trace_step(name, step_type, attributes)


def span(name, span_type=AgentSpanType.STEP, inputs=None, attributes=None):
    """
    Context manager for creating a span within an agent run.
    
    Args:
        name (str): Name of the span
        span_type (Union[AgentSpanType, str], optional): Type of the span. Defaults to AgentSpanType.STEP.
        inputs (Optional[Dict[str, Any]], optional): Inputs to the span. Defaults to None.
        attributes (Optional[Dict[str, Any]], optional): Attributes to associate with the span. Defaults to None.
            
    Yields:
        mlflow.entities.Span: The MLflow span object
    """
    return tracing_span(name, span_type, inputs, attributes)
