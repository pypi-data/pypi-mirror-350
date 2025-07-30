"""
This module provides monitoring capabilities for Azure OpenAI clients.

It includes functionality for wrapping Azure OpenAI clients to track costs,
log parameters, and manage MLflow runs.
"""
import logging
import os
import time
import uuid
from typing import Any, Dict, Optional

import mlflow

from ml_observability.observability.cost_tracking import CostTracker
from ml_observability.utils import setup_logger

logger = setup_logger(__name__)

def wrap_azure_openai(client):
    """
    Wraps an Azure OpenAI client to enable monitoring and logging capabilities.
    
    This function intercepts the client's completion creation methods (both synchronous
    and asynchronous) to track costs, log parameters, and manage MLflow runs.
    
    Args:
        client: An instance of the Azure OpenAI client to be wrapped.
        
    Returns:
        None. The function modifies the client instance in-place by wrapping its methods.
    """
    # Store original methods
    original_completions_create = getattr(client.completions, "create", None)
    original_chat_completions_create = getattr(client.chat.completions, "create", None)
    original_chat_completions_acreate = getattr(client.chat.completions, "acreate", None)
    
    # Get the global cost tracker
    from ml_observability.observability.monitor import _cost_tracker
    
    # Wrap completions.create
    if original_completions_create:
        def wrapped_completions_create(*args, **kwargs):
            # Start MLflow run if needed
            active_run = mlflow.active_run()
            started_run = False
            if not active_run:
                started_run = True
                run_name = os.getenv("MLFLOW_RUN_NAME", f"azure-openai-{uuid.uuid4()}")
                run = mlflow.start_run(run_name=run_name)
            else:
                run = active_run
                
            try:
                # Track start time
                start_time = time.time()
                
                # Call original method
                result = original_completions_create(*args, **kwargs)
                
                # Calculate duration
                duration = time.time() - start_time
                
                # Extract token usage
                prompt_tokens = getattr(result, "usage", {}).get("prompt_tokens", 0)
                completion_tokens = getattr(result, "usage", {}).get("completion_tokens", 0)
                
                # Track cost
                model_name = kwargs.get("model", "unknown")
                _cost_tracker.track_cost(
                    model_name=model_name,
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    run_id=run.info.run_id,
                    provider="Azure OpenAI"
                )
                
                # Log parameters and metrics
                mlflow.log_param("model", model_name)
                mlflow.log_param("api_type", "azure")
                mlflow.log_metric("duration_seconds", duration)
                mlflow.log_metric("prompt_tokens", prompt_tokens)
                mlflow.log_metric("completion_tokens", completion_tokens)
                
                return result
            finally:
                if started_run:
                    mlflow.end_run()
                    
        client.completions.create = wrapped_completions_create
    
    # Wrap chat.completions.create
    if original_chat_completions_create:
        def wrapped_chat_completions_create(*args, **kwargs):
            # Start MLflow run if needed
            active_run = mlflow.active_run()
            started_run = False
            if not active_run:
                started_run = True
                run_name = os.getenv("MLFLOW_RUN_NAME", f"azure-openai-chat-{uuid.uuid4()}")
                run = mlflow.start_run(run_name=run_name)
            else:
                run = active_run
                
            try:
                # Track start time
                start_time = time.time()
                
                # Call original method
                result = original_chat_completions_create(*args, **kwargs)
                
                # Calculate duration
                duration = time.time() - start_time
                
                # Extract token usage
                prompt_tokens = getattr(result, "usage", {}).get("prompt_tokens", 0)
                completion_tokens = getattr(result, "usage", {}).get("completion_tokens", 0)
                
                # Track cost
                model_name = kwargs.get("model", "unknown")
                _cost_tracker.track_cost(
                    model_name=model_name,
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    run_id=run.info.run_id,
                    provider="Azure OpenAI"
                )
                
                # Log parameters and metrics
                mlflow.log_param("model", model_name)
                mlflow.log_param("api_type", "azure")
                mlflow.log_metric("duration_seconds", duration)
                mlflow.log_metric("prompt_tokens", prompt_tokens)
                mlflow.log_metric("completion_tokens", completion_tokens)
                
                return result
            finally:
                if started_run:
                    mlflow.end_run()
                    
        client.chat.completions.create = wrapped_chat_completions_create
    
    # Wrap chat.completions.acreate (async)
    if original_chat_completions_acreate:
        async def wrapped_chat_completions_acreate(*args, **kwargs):
            # Start MLflow run if needed
            active_run = mlflow.active_run()
            started_run = False
            if not active_run:
                started_run = True
                run_name = os.getenv("MLFLOW_RUN_NAME", f"azure-openai-chat-async-{uuid.uuid4()}")
                run = mlflow.start_run(run_name=run_name)
            else:
                run = active_run
                
            try:
                # Track start time
                start_time = time.time()
                
                # Call original method
                result = await original_chat_completions_acreate(*args, **kwargs)
                
                # Calculate duration
                duration = time.time() - start_time
                
                # Extract token usage
                prompt_tokens = getattr(result, "usage", {}).get("prompt_tokens", 0)
                completion_tokens = getattr(result, "usage", {}).get("completion_tokens", 0)
                
                # Track cost
                model_name = kwargs.get("model", "unknown")
                _cost_tracker.track_cost(
                    model_name=model_name,
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    run_id=run.info.run_id,
                    provider="Azure OpenAI"
                )
                
                # Log parameters and metrics
                mlflow.log_param("model", model_name)
                mlflow.log_param("api_type", "azure")
                mlflow.log_metric("duration_seconds", duration)
                mlflow.log_metric("prompt_tokens", prompt_tokens)
                mlflow.log_metric("completion_tokens", completion_tokens)
                
                return result
            finally:
                if started_run:
                    mlflow.end_run()
                    
        client.chat.completions.acreate = wrapped_chat_completions_acreate
    
    logger.debug("Monitoring enabled for Azure OpenAI client.")
