"""
Example demonstrating the Arc Tracing SDK with fallback export mechanisms.

This example shows how to use the trace_agent decorator with fallback
export mechanisms enabled:
1. First attempt to send traces to the Arc API endpoint
2. If that fails, try direct MongoDB Atlas insertion
3. As a final fallback, save to local file

Usage:
    python example_fallback.py [--endpoint URL] [--api-key KEY]
"""

import argparse
import logging
import os
import time
from typing import Dict, Any

from arc_tracing import trace_agent
from arc_tracing.exporters import ArcExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("fallback_example")

def setup_tracing(endpoint: str = None, api_key: str = None) -> None:
    """Set up tracing with fallback export mechanisms."""
    # Create tracer provider
    tracer_provider = TracerProvider()
    
    # Create exporter with fallback mechanisms enabled
    exporter = ArcExporter(
        endpoint=endpoint,
        api_key=api_key,
        debug_mode=True,
        auth_method="header",
        auth_header_name="X-API-Key",
        fallback=True  # Enable fallback to MongoDB and local file
    )
    
    # Add exporter to tracer provider
    tracer_provider.add_span_processor(SimpleSpanProcessor(exporter))
    
    # Set global tracer provider
    trace.set_tracer_provider(tracer_provider)
    
    logger.info(f"Tracing initialized with endpoint: {endpoint or 'default'}")

# Simulate LLM call
def fake_llm_call(prompt: str) -> Dict[str, Any]:
    """Simulate an LLM API call."""
    logger.info(f"Calling LLM with prompt: {prompt}")
    time.sleep(0.5)  # Simulate API latency
    
    return {
        "id": "chatcmpl-123",
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

# Test agent function decorated with trace_agent
@trace_agent
def test_agent(query: str) -> str:
    """Example agent function that will be traced."""
    logger.info(f"Agent received query: {query}")
    
    # Add a span to represent some processing step
    tracer = trace.get_tracer("example_agent")
    with tracer.start_as_current_span("processing") as span:
        span.set_attribute("query.length", len(query))
        span.set_attribute("query.type", "text")
        
        # Simulate some processing
        logger.info("Processing query...")
        time.sleep(0.2)
    
    # Make a simulated LLM API call
    with tracer.start_as_current_span("llm.call") as span:
        span.set_attribute("llm.model", "gpt-4")
        span.set_attribute("llm.prompt", query)
        
        response = fake_llm_call(query)
        
        span.set_attribute("llm.usage.total_tokens", response["usage"]["total_tokens"])
        span.set_attribute("llm.response", response["choices"][0]["message"]["content"])
    
    # Post-processing
    with tracer.start_as_current_span("post_processing") as span:
        logger.info("Post-processing response...")
        time.sleep(0.1)
        
        final_response = response["choices"][0]["message"]["content"]
        span.set_attribute("response.length", len(final_response))
    
    return final_response

def main():
    """Run the example."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Arc Tracing SDK Fallback Example")
    parser.add_argument(
        "--endpoint", 
        default=os.environ.get("ARC_ENDPOINT", "http://localhost:8000/api/v1/traces"),
        help="API endpoint for the Arc platform"
    )
    parser.add_argument(
        "--api-key", 
        default=os.environ.get("ARC_API_KEY", "dev_arc_rewardlab_key"),
        help="API key for the Arc platform"
    )
    parser.add_argument(
        "--query",
        default="What is the purpose of machine learning?",
        help="Query to send to the test agent"
    )
    args = parser.parse_args()
    
    # Initialize tracing
    setup_tracing(args.endpoint, args.api_key)
    
    # Run the test agent
    try:
        logger.info(f"Running test agent with query: {args.query}")
        result = test_agent(args.query)
        
        # Print the result
        print("\n===== AGENT RESULT =====")
        print(f"Query: {args.query}")
        print(f"Response: {result}")
        print("========================\n")
        
        print("Trace data was sent to:")
        print(f"  Primary: {args.endpoint}")
        print("  Fallback: MongoDB Atlas (arc_rewardlab.traces)")
        print("  Fallback: Local files (./arc_traces)")
        
    except Exception as e:
        logger.error(f"Error running test agent: {e}")
        raise

if __name__ == "__main__":
    main()