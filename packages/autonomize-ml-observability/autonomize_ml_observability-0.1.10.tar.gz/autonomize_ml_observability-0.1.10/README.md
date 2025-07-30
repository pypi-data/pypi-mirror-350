# Autonomize ML Observability SDK

A comprehensive SDK for monitoring, tracing, and tracking costs for LLM applications with MLflow integration.

## Features

- **LLM Monitoring**: Automatically monitor OpenAI, Anthropic, and other LLM provider API calls
- **Cost Tracking**: Track token usage and costs across different models and providers
- **MLflow Integration**: Log all LLM interactions to MLflow for experiment tracking
- **Enhanced Agent Tracing**: Monitor and track agent interactions with LangChain and custom agent implementations
- **Visualization**: Generate cost dashboards and usage charts
- **Async Support**: Works with both synchronous and asynchronous API calls
- **Extensible**: Support for multiple LLM providers with a consistent interface

## Installation

Install the package using pip:

```bash
pip install autonomize-ml-observability
```

### With Provider-Specific Dependencies

```bash
# For OpenAI support
pip install "autonomize-ml-observability[openai]"

# For Anthropic support
pip install "autonomize-ml-observability[anthropic]"

# For both OpenAI and Anthropic
pip install "autonomize-ml-observability[openai,anthropic]"
```

## Quick Start

### Basic Usage with OpenAI

```python
import os
from openai import OpenAI
from ml_observability import monitor

# Set environment variables for authentication
os.environ["MODELHUB_BASE_URL"] = "https://your-modelhub-url.com"
os.environ["MODELHUB_CLIENT_ID"] = "your-client-id"
os.environ["MODELHUB_CLIENT_SECRET"] = "your-client-secret"
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Create OpenAI client
client = OpenAI()

# Enable monitoring (provider is auto-detected)
monitor(client)

# Use the client as normal - monitoring happens automatically
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is machine learning?"}
    ]
)

print(response.choices[0].message.content)
```

### Using with Anthropic

```python
import os
import anthropic
from ml_observability import monitor

# Set environment variables
os.environ["MODELHUB_BASE_URL"] = "https://your-modelhub-url.com"
os.environ["MODELHUB_CLIENT_ID"] = "your-client-id"
os.environ["MODELHUB_CLIENT_SECRET"] = "your-client-secret"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key"

# Create Anthropic client
client = anthropic.Anthropic()

# Enable monitoring with explicit provider specification
monitor(client, provider="anthropic")

# Use the client normally
response = client.messages.create(
    model="claude-3-sonnet-20250219",
    messages=[
        {"role": "user", "content": "What is machine learning?"}
    ]
)

print(response.content[0].text)
```

## Detailed Examples

### Monitoring OpenAI API Calls

This example demonstrates basic monitoring setup for OpenAI, cost tracking, and MLflow integration:

```python
import os
import time
from openai import OpenAI
from ml_observability import monitor, identify

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-api-key"

# Set Modelhub credentials
os.environ["MODELHUB_BASE_URL"] = "https://your-modelhub-url.com"
os.environ["MODELHUB_CLIENT_ID"] = "your-client-id"
os.environ["MODELHUB_CLIENT_SECRET"] = "your-client-secret"
os.environ["EXPERIMENT_NAME"] = "openai-monitoring-demo"

# Initialize the OpenAI client
client = OpenAI()

# Enable monitoring on the OpenAI client
monitor(client)

# Function that uses the monitored client
def ask_question(question: str, model: str = "gpt-3.5-turbo"):
    """Ask a question to the LLM model and return the response."""
    # Use identify to set user properties (optional)
    with identify({"user_id": "user-123", "session_id": "session-456"}):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content

# Test with a few questions
def main():
    questions = [
        "What is machine learning?",
        "Explain the concept of MLOps",
        "What are the benefits of monitoring LLM usage?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        start_time = time.time()
        answer = ask_question(question)
        duration = time.time() - start_time
        print(f"Answer: {answer}")
        print(f"Response time: {duration:.2f} seconds")
        time.sleep(1)

if __name__ == "__main__":
    main()
```

### Custom Cost Tracking

This example shows how to set up custom cost rates for different models and generate cost visualizations:

```python
import os
import json
import time
from openai import OpenAI
from ml_observability import monitor, initialize
from ml_observability.observability.cost_tracking import CostTracker
from ml_observability.visualization import log_cost_visualizations_to_mlflow, generate_cost_dashboard
import mlflow

# Set credentials
os.environ["OPENAI_API_KEY"] = "your-api-key"
os.environ["MODELHUB_BASE_URL"] = "https://your-modelhub-url.com"
os.environ["MODELHUB_CLIENT_ID"] = "your-client-id"
os.environ["MODELHUB_CLIENT_SECRET"] = "your-client-secret"
os.environ["EXPERIMENT_NAME"] = "cost-tracking-demo"

# Define custom cost rates for models ($/1K tokens)
custom_cost_rates = {
    "gpt-4o": {"input": 5.0, "output": 15.0},
    "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
    "claude-3-sonnet": {"input": 3.0, "output": 15.0},
    "my-custom-model": {"input": 0.25, "output": 0.75}  # Custom model rate
}

# Initialize with custom cost rates
initialize(cost_rates=custom_cost_rates, experiment_name="cost-tracking-demo")

# Create OpenAI client
client = OpenAI()
monitor(client)

# Get a reference to the cost tracker
cost_tracker = CostTracker(cost_rates=custom_cost_rates)

def simulate_api_calls():
    """Simulate a series of API calls to different models."""
    models = ["gpt-3.5-turbo", "gpt-4o", "claude-3-sonnet", "my-custom-model"]
    questions = [
        "What is the capital of France?",
        "Write a short poem about artificial intelligence",
        "Explain quantum computing in simple terms",
        "What are the main challenges in natural language processing?"
    ]
    
    with mlflow.start_run(run_name="cost_tracking_example") as run:
        for i, (model, question) in enumerate(zip(models, questions)):
            print(f"Calling {model} with question: {question[:30]}...")
            
            # Simulate different token usages
            input_tokens = len(question.split()) * (i + 1) * 2
            output_tokens = (i + 1) * 50
            
            if model.startswith("gpt"):
                # For OpenAI models, use the monitored client
                response = client.chat.completions.create(
                    model=model if not model == "my-custom-model" else "gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": question}
                    ],
                    max_tokens=output_tokens
                )
                print(f"Response: {response.choices[0].message.content[:50]}...")
            else:
                # For custom models or other providers, manually track costs
                cost_tracker.track_cost(
                    model_name=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    provider="custom" if model == "my-custom-model" else "anthropic",
                    metadata={"question": question}
                )
                print(f"Simulated response for {model}...")
            
            time.sleep(1)
        
        # Generate cost summary
        summary = cost_tracker.get_cost_summary()
        print("\nCost Summary:")
        print(json.dumps(summary, indent=2))
        
        # Log cost summary to MLflow
        cost_tracker.log_cost_summary_to_mlflow(run.info.run_id)
        
        # Generate and log visualizations
        log_cost_visualizations_to_mlflow(cost_tracker.tracked_costs, run.info.run_id)
        
        # Generate dashboard (optional)
        dashboard_path = generate_cost_dashboard(cost_tracker.tracked_costs)
        print(f"\nDashboard generated at: {dashboard_path}")

if __name__ == "__main__":
    simulate_api_calls()
```

### Agent Tracing with ModelHub

The SDK now provides enhanced tracing capabilities for agent workflows, with direct integration to ModelHub:

```python
from ml_observability.observability import (
    initialize,
    monitor,
    agent,
    agent_step,
    tool as obs_tool,
    span,
    AgentSpanType,
    get_tracer
)
from ml_observability.core.credential import ModelhubCredential

# Initialize with ModelHub credentials
credential = ModelhubCredential(
    modelhub_url=os.getenv("MODELHUB_BASE_URL"),
    client_id=os.getenv("MODELHUB_CLIENT_ID"),
    client_secret=os.getenv("MODELHUB_CLIENT_SECRET")
)
initialize(experiment_name="agent-tracing-example", credential=credential)

# Monitor an LLM client
monitor(azure_client, provider="azure_openai")

# Define a tool with automatic tracing
@obs_tool(name="search_data")
def search_data(query: str) -> str:
    """Search for data related to the query."""
    # Tool implementation
    return f"Found information about {query}..."

# Define an LLM call with automatic tracing
@agent_step(name="azure_openai_call", step_type=AgentSpanType.LLM)
def azure_openai_call(prompt: str) -> Dict[str, Any]:
    """Make a call to Azure OpenAI."""
    # LLM call implementation
    return {"content": "Response from LLM", "total_tokens": 50}

# Define your agent with automatic tracing
@agent(name="simple_agent")
def run_agent(query: str) -> str:
    """Run a simple agent that uses search and an LLM to answer questions."""
    
    with span("agent_execution", AgentSpanType.AGENT, inputs={"query": query}) as agent_span:
        # Step 1: Agent planning
        with span("agent_planning", AgentSpanType.STEP, inputs={"query": query}) as planning_span:
            planning_span.set_outputs({"decision": "search_data"})
        
        # Step 2: Execute search tool
        search_result = search_data(query)
        
        # Step 3: Use LLM to process search result
        prompt = f"Based on this information: {search_result}, answer: {query}"
        llm_result = azure_openai_call(prompt)
        
        # Step 4: Process results
        with span("process_results", AgentSpanType.STEP) as process_span:
            processed_result = f"PROCESSED RESULT: {llm_result['content']}"
            process_span.set_outputs({"formatted_results": processed_result})
        
        # Set outputs for the agent span
        agent_span.set_outputs({
            "search_result": search_result,
            "llm_response": llm_result["content"],
            "processed_result": processed_result,
            "total_tokens": llm_result["total_tokens"]
        })
    
    return processed_result
```

### Custom Run Names

You can set custom run names for your agent executions using environment variables:

```bash
MLFLOW_RUN_NAME="my-custom-run-name" python examples/observability/app/langchain_agent_example.py
```

### Monitoring Anthropic with Decorators

This example demonstrates how to set up monitoring for Anthropic's Claude models and use the agent and tool decorator patterns:

```python
import os
import time
import anthropic
from ml_observability import monitor, agent, tool

# Set your Anthropic API key
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key"

# Set Modelhub credentials
os.environ["MODELHUB_BASE_URL"] = "https://your-modelhub-url.com"
os.environ["MODELHUB_CLIENT_ID"] = "your-client-id"
os.environ["MODELHUB_CLIENT_SECRET"] = "your-client-secret"
os.environ["EXPERIMENT_NAME"] = "anthropic-monitoring-demo"

# Initialize the Anthropic client
client = anthropic.Anthropic()

# Enable monitoring (the provider will be auto-detected)
monitor(client, provider="anthropic")

# Decorator for tracking an agent function
@agent(name="content_generator", tags={"type": "content_generation"})
def generate_content(prompt, model="claude-3-sonnet-20250219"):
    """Generate content using Claude with automatic tracking."""
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text

# Decorator for tracking a tool function
@tool(name="text_summarizer")
def summarize_text(text, model="claude-3-haiku"):
    """Summarize text using Claude with automatic tracking."""
    prompt = f"Please summarize the following text concisely:\n\n{text}"
    response = client.messages.create(
        model=model,
        max_tokens=300,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text

def main():
    # Example text to summarize
    long_text = """
    Machine learning (ML) is a subset of artificial intelligence (AI) that focuses on developing 
    systems that learn or improve performance based on the data they consume. ML algorithms build 
    mathematical models based on sample data, known as training data, to make predictions or decisions 
    without being explicitly programmed to do so. These algorithms identify patterns in observed data, 
    build models that explain the world, and make predictions from seemingly chaotic information.
    
    There are three main types of machine learning: supervised learning, unsupervised learning, and 
    reinforcement learning. In supervised learning, the algorithm is provided with labeled training 
    data and the desired output. In unsupervised learning, the algorithm is given unlabeled data and 
    must find patterns and relationships on its own. Reinforcement learning involves an agent that 
    learns to make decisions by taking actions in an environment to maximize a reward.
    
    MLOps (Machine Learning Operations) is the practice of collaboration and communication between 
    data scientists and operations professionals to help manage the production ML lifecycle. It aims 
    to standardize and streamline the continuous delivery of high-performing models in production by 
    automating and monitoring all steps of system construction.
    """
    
    print("Generating content...")
    content = generate_content("Write a short blog post about the future of AI and automation")
    print(f"Generated content: {content[:100]}...\n")
    
    print("Summarizing text...")
    summary = summarize_text(long_text)
    print(f"Summary: {summary}")

if __name__ == "__main__":
    main()
```

### Async OpenAI Example

This example demonstrates how to use the SDK with asynchronous API calls:

```python
import os
import asyncio
import time
from datetime import datetime
import json
from openai import AsyncOpenAI
from ml_observability import monitor
from ml_observability.visualization import generate_cost_summary_charts

# Set credentials
os.environ["OPENAI_API_KEY"] = "your-api-key"
os.environ["MODELHUB_BASE_URL"] = "https://your-modelhub-url.com"
os.environ["MODELHUB_CLIENT_ID"] = "your-client-id" 
os.environ["MODELHUB_CLIENT_SECRET"] = "your-client-secret"
os.environ["EXPERIMENT_NAME"] = "async-openai-demo"

# Initialize the AsyncOpenAI client
client = AsyncOpenAI()

# Enable monitoring on the AsyncOpenAI client
monitor(client)

async def ask_question(question: str, model: str = "gpt-3.5-turbo"):
    """Ask a question to the LLM model asynchronously."""
    start_time = time.time()
    
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        max_tokens=150
    )
    
    duration = time.time() - start_time
    result = {
        "question": question,
        "answer": response.choices[0].message.content,
        "model": model,
        "duration": duration,
        "timestamp": datetime.now().isoformat(),
        "tokens": {
            "prompt": response.usage.prompt_tokens,
            "completion": response.usage.completion_tokens,
            "total": response.usage.total_tokens
        }
    }
    return result

async def process_batch(questions, model="gpt-3.5-turbo"):
    """Process a batch of questions concurrently."""
    tasks = [ask_question(question, model) for question in questions]
    return await asyncio.gather(*tasks)

async def main():
    # Define questions
    questions = [
        "What is machine learning?",
        "Explain the concept of MLOps",
        "What are the benefits of monitoring LLM usage?"
    ]
    
    # Process questions concurrently
    results = await process_batch(questions)
    
    # Print results
    for result in results:
        print(f"\nQuestion: {result['question']}")
        print(f"Answer: {result['answer']}")
        print(f"Duration: {result['duration']:.2f} seconds")
        print(f"Tokens: {result['tokens']['total']} ({result['tokens']['prompt']} prompt, {result['tokens']['completion']} completion)")

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

### Setting Up Credentials

The SDK supports different authentication methods:

```python
from ml_observability.core.credential import ModelhubCredential

# Using environment variables (recommended)
# Set MODELHUB_BASE_URL, MODELHUB_CLIENT_ID, MODELHUB_CLIENT_SECRET
credential = ModelhubCredential()

# Or explicitly
credential = ModelhubCredential(
    modelhub_url="https://your-modelhub-url.com",
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Using direct token (not recommended for production)
credential = ModelhubCredential(token="your-jwt-token")

# Initialize ML Observability with ModelHub credentials
from ml_observability.observability import initialize

initialize(experiment_name="my-experiment", credential=credential)
```

### Custom Cost Rates

Configure custom cost rates for different models:

```python
from ml_observability.observability.cost_tracking import CostTracker

# Define custom cost rates ($ per 1K tokens)
custom_rates = {
    "gpt-4o": {"input": 5.0, "output": 15.0},
    "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
    "claude-3-opus": {"input": 15.0, "output": 75.0},
    "my-custom-model": {"input": 0.25, "output": 0.75}
}

# Initialize cost tracker with custom rates
cost_tracker = CostTracker(cost_rates=custom_rates)
```

## Advanced Features

### Step-by-Step Tracing

The enhanced agent tracing capabilities allow you to:

- Create hierarchical traces of agent executions
- Track individual steps within an agent run
- Associate costs with specific steps
- Visualize the execution flow in ModelHub
- Set custom run names for easier identification

### Cost Tracking per Step

The SDK now supports detailed cost tracking for each step in an agent workflow:

```python
from ml_observability.observability.cost_tracking import CostTracker

cost_tracker = CostTracker()

# Track cost for a specific step
cost_tracker.track_cost_for_step(
    model_name="gpt-4o",
    input_tokens=150,
    output_tokens=50,
    step_name="planning",
    step_id="step-123",
    trace_id="trace-456"
)
```

## Examples

Check out the complete examples in the `examples/observability/app` directory, including:

- `langchain_agent_example.py`: A complete example of integrating ModelHub with a LangChain-style agent

## License

Proprietary © Autonomize.ai