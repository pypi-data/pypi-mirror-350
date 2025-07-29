"""
Example demonstrating integration with the Arc RewardLab backend.

This example shows how to properly configure the SDK to work with the Arc
RewardLab backend, including authentication and trace formatting.

Features demonstrated:
- Configuration for backend endpoint
- X-API-Key authentication
- Trace format that matches the TraceCreate model
- Local file fallback for offline use
- Manual batch upload of traces
"""

import argparse
import json
import logging
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from arc_tracing import trace_agent
from arc_tracing.exporters import ArcExporter, BatchUploader
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("integration_example")

def setup_tracing(
    endpoint: str = "http://localhost:8000/api/v1/traces",
    api_key: str = "dev_arc_rewardlab_key",
    project_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    debug_mode: bool = True,
) -> None:
    """
    Set up tracing with proper UUID handling for project and agent IDs.
    
    If project_id or agent_id are not provided or not in UUID format,
    they will be converted to valid UUIDs.
    """
    # Handle UUIDs for project and agent IDs
    if project_id and not is_valid_uuid(project_id):
        project_id = str(uuid.uuid5(uuid.NAMESPACE_OID, project_id))
        logger.info(f"Converted project_id to UUID: {project_id}")
        
    if agent_id and not is_valid_uuid(agent_id):
        agent_id = str(uuid.uuid5(uuid.NAMESPACE_OID, agent_id))
        logger.info(f"Converted agent_id to UUID: {agent_id}")
        
    if not project_id:
        # Default project ID as UUID
        project_id = "123e4567-e89b-12d3-a456-426614174000"
        
    if not agent_id:
        # Default agent ID as UUID
        agent_id = "123e4567-e89b-12d3-a456-426614174001"
    """Set up tracing with proper backend integration."""
    # Create tracer provider
    tracer_provider = TracerProvider()
    
    # Create exporter for Arc RewardLab backend
    arc_exporter = ArcExporter(
        endpoint=endpoint,
        api_key=api_key,
        project_id=project_id,
        agent_id=agent_id,
        debug_mode=debug_mode,
        auth_method="header",
        auth_header_name="X-API-Key",
        local_fallback=True  # Enable local file fallback
    )
    
    # Add exporter to tracer provider
    tracer_provider.add_span_processor(SimpleSpanProcessor(arc_exporter))
    
    # Set global tracer provider
    trace.set_tracer_provider(tracer_provider)
    
    logger.info(f"Tracing initialized with endpoint: {endpoint}")
    logger.info(f"Using project_id: {project_id}, agent_id: {agent_id}")

# Utility function to validate UUID format
def is_valid_uuid(uuid_string: str) -> bool:
    """
    Check if a string is a valid UUID.
    
    Args:
        uuid_string: The string to check
        
    Returns:
        True if the string is a valid UUID, False otherwise
    """
    try:
        uuid_obj = uuid.UUID(uuid_string)
        return str(uuid_obj) == uuid_string
    except (ValueError, AttributeError, TypeError):
        return False

# Simulate LLM call
def simulate_llm_call(prompt: str) -> Dict[str, Any]:
    """Simulate an LLM API call."""
    logger.info(f"Calling LLM with prompt: {prompt}")
    time.sleep(0.5)  # Simulate API latency
    
    # Return a structure similar to OpenAI response
    return {
        "id": "chatcmpl-123456",
        "model": "gpt-4",
        "usage": {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": 20,
            "total_tokens": len(prompt.split()) + 20
        },
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": f"This is a simulated response to: {prompt}"
                }
            }
        ]
    }

# Agent function with the trace_agent decorator
@trace_agent
def example_agent(query: str) -> str:
    """Example agent function that will be traced."""
    # Create a tracer for more detailed spans
    tracer = trace.get_tracer("example_agent")
    
    # Add query to attributes for proper trace_input capture
    current_span = trace.get_current_span()
    current_span.set_attribute("arc_tracing.agent.input", query)
    
    # Add span for processing step
    with tracer.start_as_current_span("processing") as span:
        span.set_attribute("step.type", "agent_action")  # Mark as agent action
        span.set_attribute("query.length", len(query))
        span.set_attribute("query.type", "text")
        
        # Add metadata
        span.set_attribute("metadata.framework", "example_framework")
        span.set_attribute("metadata.tags", json.dumps(["test", "example"]))
        
        # Simulate some processing
        logger.info("Processing query...")
        time.sleep(0.2)
    
    # Add span for LLM call
    with tracer.start_as_current_span("llm.call") as span:
        span.set_attribute("step.type", "llm_call")  # Explicitly mark as LLM call
        span.set_attribute("llm.model", "gpt-4")
        span.set_attribute("llm.prompt", query)
        
        # Make the simulated LLM API call
        start_time = time.time()
        response = simulate_llm_call(query)
        duration_ms = (time.time() - start_time) * 1000
        
        # Add metrics that will be captured in the trace
        span.set_attribute("metrics.tokens.prompt", response["usage"]["prompt_tokens"])
        span.set_attribute("metrics.tokens.completion", response["usage"]["completion_tokens"])
        span.set_attribute("metrics.tokens.total", response["usage"]["total_tokens"])
        span.set_attribute("metrics.response_time_ms", duration_ms)
        
        # Add cost estimate (optional)
        cost_per_token = 0.0001  # Example rate
        estimated_cost = response["usage"]["total_tokens"] * cost_per_token
        span.set_attribute("metrics.cost", estimated_cost)
        
        # Get the actual response text
        response_text = response["choices"][0]["message"]["content"]
        span.set_attribute("llm.response", response_text)
        
    # Add span for a tool call example
    with tracer.start_as_current_span("tool.call") as span:
        span.set_attribute("step.type", "tool_call")
        span.set_attribute("tool.name", "search_tool")
        span.set_attribute("tool.input", query)
        span.set_attribute("tool.output", "This is a simulated search result relevant to the query.")
        span.set_attribute("metrics.duration_ms", 250)
    
    # Add span for post-processing
    with tracer.start_as_current_span("post_processing") as span:
        span.set_attribute("step.type", "agent_action")  # Mark as agent action
        logger.info("Post-processing response...")
        time.sleep(0.1)
        
        # Add simulated signals for analysis
        span.set_attribute("signals.user_satisfaction", 0.95)
        span.set_attribute("signals.accuracy", 0.98)
        span.set_attribute("signals.efficiency", 0.85)
        
        # Add the final result to attributes for proper trace_output capture
        current_span.set_attribute("arc_tracing.agent.result", response_text)
        
    return response_text

def upload_local_traces(
    endpoint: str = "http://localhost:8000/api/v1/traces",
    api_key: str = "dev_arc_rewardlab_key",
    export_dir: str = "./arc_traces"
) -> None:
    """Upload locally stored traces to the backend."""
    if not os.path.exists(export_dir):
        logger.info(f"No local traces directory found at {export_dir}")
        return
    
    uploader = BatchUploader(
        export_dir=export_dir,
        endpoint=endpoint,
        api_key=api_key
    )
    
    trace_files = uploader.list_trace_files()
    if not trace_files:
        logger.info("No local trace files found")
        return
    
    logger.info(f"Found {len(trace_files)} trace files to upload")
    
    # Upload all trace files
    results = uploader.upload_all()
    
    # Print results
    successes = sum(1 for success in results.values() if success)
    logger.info(f"Uploaded {successes} of {len(results)} trace files")
    
    for file_path, success in results.items():
        logger.info(f"{os.path.basename(file_path)}: {'Success' if success else 'Failed'}")

def main():
    """Run the example."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Arc RewardLab Backend Integration Example")
    parser.add_argument(
        "--endpoint", 
        default=os.environ.get("ARC_ENDPOINT", "http://localhost:8000/api/v1/traces"),
        help="API endpoint for the Arc RewardLab backend"
    )
    parser.add_argument(
        "--api-key", 
        default=os.environ.get("ARC_API_KEY", "dev_arc_rewardlab_key"),
        help="API key for the Arc RewardLab backend"
    )
    parser.add_argument(
        "--project-id",
        default="123e4567-e89b-12d3-a456-426614174000",
        help="Project ID for trace metadata (UUID format recommended)"
    )
    parser.add_argument(
        "--agent-id",
        default="123e4567-e89b-12d3-a456-426614174001",
        help="Agent ID for trace metadata (UUID format recommended)"
    )
    parser.add_argument(
        "--query",
        default="What are the key challenges in modern AI development?",
        help="Query to send to the example agent"
    )
    parser.add_argument(
        "--upload-traces",
        action="store_true",
        help="Upload locally stored traces after running the example"
    )
    args = parser.parse_args()
    
    # Initialize tracing
    setup_tracing(
        endpoint=args.endpoint,
        api_key=args.api_key,
        project_id=args.project_id,
        agent_id=args.agent_id
    )
    
    # Run the example agent
    try:
        logger.info(f"Running example agent with query: {args.query}")
        result = example_agent(args.query)
        
        # Print the result
        print("\n===== AGENT RESULT =====")
        print(f"Query: {args.query}")
        print(f"Response: {result}")
        print("========================\n")
        
        print("Trace data was sent to:")
        print(f"  Backend API: {args.endpoint}")
        print("  Local fallback: ./arc_traces (if backend unavailable)")
        
    except Exception as e:
        logger.error(f"Error running example agent: {e}")
    
    # Optionally upload any local traces
    if args.upload_traces:
        logger.info("Uploading any locally stored traces...")
        upload_local_traces(
            endpoint=args.endpoint,
            api_key=args.api_key
        )

if __name__ == "__main__":
    main()