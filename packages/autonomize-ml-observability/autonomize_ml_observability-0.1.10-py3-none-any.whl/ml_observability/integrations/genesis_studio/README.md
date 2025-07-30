# Genesis Studio Integration for ML Observability

This integration enables seamless tracing and monitoring of Genesis Studio agent executions using ML Observability. It provides a custom tracer implementation that connects Genesis Studio's tracing service with ML Observability's agent tracing capabilities.

## Features

- Hierarchical tracing of agent executions
- Detailed tracking of tool usage
- LLM call monitoring and cost tracking
- Error handling and logging
- Integration with LangChain callbacks

## Usage

### Basic Integration

```python
from ml_observability.integrations.genesis_studio import MLObservabilityTracer

# Initialize the tracer
tracer = MLObservabilityTracer()

# Add it to the Genesis Studio tracing service
tracing_service._tracers["ml_observability"] = tracer
```

### Monitoring LLM Clients

```python
# Monitor an OpenAI client
from openai import OpenAI
client = OpenAI(api_key="your-api-key")
tracer.monitor_llm_client(client)

# Monitor an Azure OpenAI client
from openai import AzureOpenAI
azure_client = AzureOpenAI(...)
tracer.monitor_llm_client(azure_client)
```

### Using LangChain Callbacks

```python
# Get a LangChain callback handler
callback = tracer.get_langchain_callback()

# Use it with LangChain agents
agent.run(input="...", callbacks=[callback])
```

## Environment Variables

The following environment variables can be used to configure the integration:

- `MLFLOW_RUN_NAME`: Custom name for MLflow runs (default: uses the trace name)
- `MLFLOW_TRACKING_URI`: URI for the MLflow tracking server
- `MLFLOW_EXPERIMENT_NAME`: Name of the MLflow experiment to use

## Requirements

- MLflow
- Genesis Studio
- Python 3.12+
