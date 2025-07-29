"""Example of tracing an Agno agent with Arc Tracing SDK."""

import os
import sys

# Add parent directory to path to import from arc_tracing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from arc_tracing import trace_agent
from arc_tracing.exporters import ConsoleExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Set up tracing with console exporter for this example
tracer_provider = TracerProvider()
console_exporter = ConsoleExporter()
tracer_provider.add_span_processor(SimpleSpanProcessor(console_exporter))
trace.set_tracer_provider(tracer_provider)

# Setup and imports for Agno
try:
    from agno.agent import Agent
    from agno.models.openai import OpenAI
    AGNO_AVAILABLE = True
except ImportError:
    print("Agno is not installed. Run 'pip install agno' to use this example.")
    AGNO_AVAILABLE = False

# Decorated function using Agno agent
@trace_agent
def run_agno_agent(prompt):
    """Run a simple Agno agent with the prompt."""
    if not AGNO_AVAILABLE:
        return "Agno is not installed."
    
    if not os.environ.get("OPENAI_API_KEY"):
        return "Error: OPENAI_API_KEY environment variable not set"
    
    # Create an Agno agent with OpenAI model
    agent = Agent(
        model=OpenAI(id="gpt-4o"),
        description="You are a helpful assistant that provides clear and concise answers.",
        instructions=["Always cite your sources if referring to specific information.", 
                     "Keep your responses brief and to the point."],
        markdown=True
    )
    
    # Generate response
    response = agent.generate_response(prompt)
    
    return response

# Example usage
if __name__ == "__main__":
    if not AGNO_AVAILABLE:
        print("Agno is not installed. Run 'pip install agno' to use this example.")
        sys.exit(1)
    
    # Get prompt from command line or use default
    prompt = sys.argv[1] if len(sys.argv) > 1 else "What is machine learning?"
    
    print(f"Prompt: {prompt}")
    print("-" * 50)
    
    response = run_agno_agent(prompt)
    print(f"Response: {response}")
    print("-" * 50)
    print("Check the console output above for the trace information.")