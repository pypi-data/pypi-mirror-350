"""Integration test for backend connectivity."""

import os
import sys
import logging
import argparse
import time
from typing import Optional

# Add parent directory to path to import from arc_tracing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from arc_tracing import trace_agent
from arc_tracing.exporters import ArcExporter, ConsoleExporter, LocalFileExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# Set urllib3 to debug level to see HTTP request details
logging.getLogger("urllib3").setLevel(logging.DEBUG)
# Set requests to debug level
logging.getLogger("requests").setLevel(logging.DEBUG)
# Our main logger
logger = logging.getLogger("backend_integration_test")

# Test LLM API call (simulated)
def fake_llm_call(prompt: str) -> str:
    """Simulate an LLM API call."""
    logger.info(f"Simulating LLM call with prompt: {prompt}")
    time.sleep(0.5)  # Simulate API latency
    return f"This is a simulated response to: {prompt}"

# Test agent using trace_agent decorator
@trace_agent
def test_agent(query: str) -> str:
    """Simple test agent to verify tracing."""
    logger.info(f"Test agent received query: {query}")
    
    # Get current span to add input/output for proper trace formatting
    current_span = trace.get_current_span()
    current_span.set_attribute("arc_tracing.agent.input", query)
    current_span.set_attribute("arc_tracing.agent.frameworks", "integration_test")
    
    # Get a tracer for more detailed spans
    tracer = trace.get_tracer("test_agent")
    
    # Simulate some processing with a span
    with tracer.start_as_current_span("processing") as span:
        span.set_attribute("step.type", "agent_action")
        logger.info("Processing query...")
        time.sleep(0.2)
    
    # Simulate a call to an LLM API with a span
    with tracer.start_as_current_span("llm.call") as span:
        span.set_attribute("step.type", "llm_call")
        span.set_attribute("llm.model", "gpt-4")
        span.set_attribute("llm.prompt", query)
        
        # Call the LLM
        response = fake_llm_call(query)
        
        # Add response and metrics
        span.set_attribute("llm.response", response)
        span.set_attribute("metrics.tokens.prompt", len(query.split()))
        span.set_attribute("metrics.tokens.completion", len(response.split()))
        span.set_attribute("metrics.tokens.total", len(query.split()) + len(response.split()))
    
    # Simulate a tool call with a span
    with tracer.start_as_current_span("tool.search") as span:
        span.set_attribute("step.type", "tool_call")
        span.set_attribute("tool.name", "search_tool")
        span.set_attribute("tool.input", query)
        span.set_attribute("tool.output", "This is simulated search result data")
        logger.info("Making tool call...")
        time.sleep(0.15)
    
    # Simulate some post-processing with a span
    with tracer.start_as_current_span("post_processing") as span:
        span.set_attribute("step.type", "agent_action")
        logger.info("Post-processing response...")
        time.sleep(0.2)
        
        # Add signals for analysis
        span.set_attribute("signals.relevance", 0.95)
        span.set_attribute("signals.accuracy", 0.88)
    
    # Set the final output for proper trace formatting
    current_span.set_attribute("arc_tracing.agent.result", response)
    
    # Add global metrics
    current_span.set_attribute("metrics.total_duration_ms", 550)
    
    return response

def setup_tracing(
    backend_url: str, 
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    local_export: bool = True,
    export_dir: Optional[str] = None,
    insecure: bool = False,
    auth_method: str = "header",
    auth_header: str = "X-API-Key",
    timeout: int = 30,
    max_retries: int = 2
) -> None:
    """Set up tracing with both console and backend exporters."""
    # Create tracer provider
    tracer_provider = TracerProvider()
    
    # Always add console exporter for debugging
    console_exporter = ConsoleExporter()
    tracer_provider.add_span_processor(SimpleSpanProcessor(console_exporter))
    
    # Add backend exporter if URL is provided
    if backend_url:
        logger.info(f"Setting up backend exporter with URL: {backend_url}")
        logger.info(f"Using auth method: {auth_method}, header: {auth_header}")
        arc_exporter = ArcExporter(
            endpoint=backend_url,
            api_key=api_key or "dev_arc_rewardlab_key",
            project_id=project_id,
            agent_id=agent_id,
            debug_mode=True,  # Enable debug mode for troubleshooting
            verify_ssl=not insecure,  # Disable SSL verification if insecure flag is set
            auth_method=auth_method,
            auth_header_name=auth_header,
            timeout=timeout,
            max_retries=max_retries,
            local_fallback=local_export  # Enable local file fallback
        )
        tracer_provider.add_span_processor(SimpleSpanProcessor(arc_exporter))
    
    # Add local file exporter if requested
    if local_export:
        logger.info(f"Setting up local file exporter with dir: {export_dir or './arc_traces'}")
        local_exporter = LocalFileExporter(export_dir=export_dir)
        tracer_provider.add_span_processor(SimpleSpanProcessor(local_exporter))
    
    # Set global tracer provider
    trace.set_tracer_provider(tracer_provider)

def main() -> None:
    """Run the integration test."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Backend integration test")
    parser.add_argument(
        "--backend-url", 
        default="http://localhost:8000/api/v1/traces/",
        help="URL of the backend traces endpoint"
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable SSL verification for testing"
    )
    parser.add_argument(
        "--auth-method",
        default="header",
        choices=["bearer", "basic", "header", "none"],
        help="Authentication method to use"
    )
    parser.add_argument(
        "--auth-header",
        default="X-API-Key",
        help="Name of the authentication header"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Connection timeout in seconds"
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Number of retries on connection failure"
    )
    parser.add_argument(
        "--no-local-export",
        action="store_true",
        help="Disable local file fallback"
    )
    parser.add_argument(
        "--project-id",
        help="Project ID for trace metadata"
    )
    parser.add_argument(
        "--agent-id",
        help="Agent ID for trace metadata"
    )
    parser.add_argument(
        "--api-key", 
        help="API key for authentication"
    )
    parser.add_argument(
        "--local-export",
        action="store_true",
        help="Also export traces to local files"
    )
    parser.add_argument(
        "--export-dir",
        help="Directory for local trace export"
    )
    parser.add_argument(
        "--query",
        default="Test query for local backend integration",
        help="Query to use for the test agent"
    )
    args = parser.parse_args()
    
    # Set up tracing
    setup_tracing(
        backend_url=args.backend_url,
        api_key=args.api_key,
        project_id=args.project_id,
        agent_id=args.agent_id,
        local_export=args.local_export and not args.no_local_export,
        export_dir=args.export_dir,
        insecure=args.insecure,
        auth_method=args.auth_method,
        auth_header=args.auth_header,
        timeout=args.timeout,
        max_retries=args.retries
    )
    
    # Run the test
    try:
        logger.info("Running test agent...")
        result = test_agent(args.query)
        
        print("\n========== TEST RESULTS ==========")
        print(f"Query: {args.query}")
        print(f"Response: {result}")
        print("\nTrace should have been sent to:")
        print(f"  Backend URL: {args.backend_url}")
        if args.local_export:
            print(f"  Local directory: {args.export_dir or './arc_traces'}")
        print("\nNext steps:")
        print("1. Check your backend server logs to verify the trace was received")
        print("2. Verify the trace was stored in the backend database")
        if args.local_export:
            print(f"3. Check local trace files in {args.export_dir or './arc_traces'}")
        print("=====================================\n")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

if __name__ == "__main__":
    main()