"""
Test the ArcExporter with the updated backend specifications.

This script creates a simple trace and sends it to the backend using the
ArcExporter, with the new simplified API format:

1. Base URL: http://localhost:8000
2. Endpoint: /api/v1/traces/
3. Minimal payload: {"input": "question", "output": "answer"}
4. Headers: Either X-API-Key: dev_arc_rewardlab_key or X-Test-Mode: true
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
logger = logging.getLogger("arc_exporter_test")

def setup_tracing(
    endpoint="http://localhost:8000/api/v1/traces/",
    use_test_mode=True
):
    """Set up tracing with the updated backend requirements."""
    # Create tracer provider
    tracer_provider = TracerProvider()
    
    # Create headers dictionary
    headers = {}
    if use_test_mode:
        headers["X-Test-Mode"] = "true"
    
    # Create exporter for backend
    exporter = ArcExporter(
        endpoint=endpoint,
        api_key="dev_arc_rewardlab_key",
        project_id=str(uuid.uuid4()),  # Generate random project_id
        agent_id=str(uuid.uuid4()),    # Generate random agent_id
        auth_method="header",
        auth_header_name="X-API-Key",
        extra_headers=headers,         # Add X-Test-Mode header if requested
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
    """Create a simple test trace with the minimal required fields."""
    # Get a tracer
    tracer = trace.get_tracer("arc_exporter_test")
    
    # Create a root span for the conversation
    with tracer.start_as_current_span("agent.conversation") as conversation:
        # Add required input/output fields - these will be extracted for the trace
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
    """Run the test with the updated backend specifications."""
    try:
        # First check if a server is reachable
        import requests
        try:
            logger.info("Checking if backend server is reachable...")
            response = requests.get("http://localhost:8000/", timeout=2)
            server_available = response.status_code == 200
            logger.info(f"Server status: {'Available' if server_available else 'Unavailable'}")
        except:
            server_available = False
            logger.warning("Backend server is not reachable - will use local fallback")
        
        # Set up tracing - will use local fallback if server is unreachable
        exporter = setup_tracing(use_test_mode=True)
        
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
            if files:
                latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(trace_dir, f)))
                logger.info(f"Trace saved to: {os.path.join(trace_dir, latest_file)}")
                
                # Show file stats
                file_path = os.path.join(trace_dir, latest_file)
                file_size = os.path.getsize(file_path)
                logger.info(f"Trace file size: {file_size} bytes")
                
                # Count traces in file
                with open(file_path, 'r') as f:
                    line_count = sum(1 for _ in f)
                    logger.info(f"Trace file contains {line_count} spans")
        
        # Shut down exporter
        exporter.shutdown()
        
        # Print summary based on server availability
        if server_available:
            logger.info("Test completed - trace sent to backend server and local storage")
        else:
            logger.info("Test completed - trace saved to local storage (backend not available)")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")

if __name__ == "__main__":
    main()