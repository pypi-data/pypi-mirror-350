"""Example of tracing a Google ADK agent with Arc Tracing SDK."""

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

# Setup and imports for Google ADK
try:
    from google.adk.agents import Agent
    from google.adk.agents.llm_agent import LlmAgent
    from google.adk.tlms.gemini import GeminiTlm
    ADK_AVAILABLE = True
except ImportError:
    print("Google ADK is not installed. Run 'pip install google-adk' to use this example.")
    ADK_AVAILABLE = False

# Helpers for tool creation
def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city."""
    # This is a mock implementation
    return {
        "city": city,
        "temperature": "72°F",
        "condition": "Sunny",
        "humidity": "45%"
    }

def get_current_time(location: str) -> dict:
    """Returns the current time in a specified location."""
    # This is a mock implementation
    import datetime
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return {
        "location": location,
        "current_time": current_time,
        "timezone": "UTC"
    }

# Decorated function using Google ADK agent
@trace_agent
def run_adk_agent(query):
    """Run a simple Google ADK agent with the query."""
    if not ADK_AVAILABLE:
        return "Google ADK is not installed."
    
    if not os.environ.get("GOOGLE_API_KEY"):
        return "Error: GOOGLE_API_KEY environment variable not set"
    
    # Create a Google ADK agent
    agent = Agent(
        name="weather_time_agent",
        model="gemini-2.0-flash",
        description="Agent to answer questions about the time and weather in a city.",
        instruction="I can answer your questions about the time and weather in a city.",
        tools=[get_weather, get_current_time]
    )
    
    # Process query
    response = agent.respond(query)
    
    return response

# Example usage
if __name__ == "__main__":
    if not ADK_AVAILABLE:
        print("Google ADK is not installed. Run 'pip install google-adk' to use this example.")
        sys.exit(1)
    
    # Get query from command line or use default
    query = sys.argv[1] if len(sys.argv) > 1 else "What's the weather in New York?"
    
    print(f"Query: {query}")
    print("-" * 50)
    
    response = run_adk_agent(query)
    print(f"Response: {response}")
    print("-" * 50)
    print("Check the console output above for the trace information.")