"""
Test script for verifying backend connectivity.

This script creates and sends a simple trace to the backend,
using proper error handling and the latest span_id formatting.

Usage:
    python test_backend_connection.py
"""

import time
import logging
import uuid
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from arc_tracing.exporters.arc_exporter import ArcExporter

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("test_backend")

def setup_tracing(
    endpoint="http://localhost:8000/api/v1/traces/",
    api_key="dev_arc_rewardlab_key"
):
    """Set up tracing with backend connection."""
    # Create tracer provider
    tracer_provider = TracerProvider()
    
    # Create exporter for backend
    exporter = ArcExporter(
        endpoint=endpoint,
        api_key=api_key,
        project_id=str(uuid.uuid4()),  # Generate random project_id
        agent_id=str(uuid.uuid4()),    # Generate random agent_id
        auth_method="header",
        auth_header_name="X-API-Key",
        debug_mode=True,               # Enable debug mode for detailed logging
        local_fallback=True            # Enable local file fallback
    )
    
    # Add exporter to tracer provider with batch processor for better performance
    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
    
    # Set global tracer provider
    trace.set_tracer_provider(tracer_provider)
    
    logger.info(f"Tracing initialized with endpoint: {endpoint}")
    return exporter

def create_test_trace():
    """Create a simple test trace with all required fields."""
    # Get a tracer
    tracer = trace.get_tracer("test_backend")
    
    # Create a root span for the conversation
    with tracer.start_as_current_span("agent.conversation") as conversation:
        # Add required input/output fields
        conversation.set_attribute("arc_tracing.agent.input", "What is machine learning?")
        conversation.set_attribute("arc_tracing.agent.frameworks", "test")
        
        # Add an LLM call span
        with tracer.start_as_current_span("llm.call") as span:
            # Mark as LLM call for proper formatting
            span.set_attribute("step.type", "llm_call")
            span.set_attribute("llm.model", "gpt-4")
            span.set_attribute("llm.prompt", "What is machine learning?")
            
            # Simulate API call
            logger.info("Simulating LLM call...")
            time.sleep(0.5)
            
            # Add response and metrics
            response = "Machine learning is a branch of artificial intelligence..."
            span.set_attribute("llm.response", response)
            span.set_attribute("metrics.tokens.prompt", 4)
            span.set_attribute("metrics.tokens.completion", 10)
            span.set_attribute("metrics.tokens.total", 14)
        
        # Add the final response
        conversation.set_attribute("arc_tracing.agent.result", response)
    
    logger.info("Test trace created and sent")

def main():
    """Run the backend connection test."""
    try:
        # Set up tracing
        exporter = setup_tracing()
        
        # Create and send test trace
        create_test_trace()
        
        # Force export completion and wait for background tasks
        logger.info("Waiting for trace export to complete...")
        time.sleep(2)
        
        # Check local trace files
        import os
        trace_dir = "./arc_traces"
        if os.path.exists(trace_dir):
            files = os.listdir(trace_dir)
            logger.info(f"Local trace files: {files}")
            
            # Check the most recent file
            if files:
                latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(trace_dir, f)))
                logger.info(f"Most recent trace file: {latest_file}")
                
                # Show trace file content
                with open(os.path.join(trace_dir, latest_file), 'r') as f:
                    content = f.read()
                    logger.info(f"Trace file content (first 200 chars): {content[:200]}...")
        
        # Shut down exporter
        exporter.shutdown()
        logger.info("Test completed successfully")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")

if __name__ == "__main__":
    main()