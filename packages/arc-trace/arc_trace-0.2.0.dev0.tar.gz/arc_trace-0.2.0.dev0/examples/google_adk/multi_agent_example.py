"""Example of tracing a Google ADK multi-agent system with Arc Tracing SDK."""

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

# Helpers for specialized tools
def search_web(query: str) -> str:
    """Searches the web for information about a topic."""
    # This is a mock implementation
    return f"Here are search results for '{query}': [Mock search results...]"

def format_report(content: str, style: str = "concise") -> str:
    """Formats content into a structured report."""
    # This is a mock implementation
    if style == "concise":
        return f"## Concise Report\n\n{content}\n\n[END OF REPORT]"
    else:
        return f"## Detailed Report\n\n{content}\n\n[END OF REPORT]"

# Decorated function using Google ADK multi-agent system
@trace_agent
def run_adk_multi_agent(query):
    """Run a Google ADK multi-agent system with the query."""
    if not ADK_AVAILABLE:
        return "Google ADK is not installed."
    
    if not os.environ.get("GOOGLE_API_KEY"):
        return "Error: GOOGLE_API_KEY environment variable not set"
    
    # Create specialized agents
    researcher = LlmAgent(
        name="Researcher",
        model="gemini-2.0-flash",
        description="Agent that searches for information and provides facts.",
        instruction="Search for accurate and relevant information.",
        tools=[search_web]
    )
    
    writer = LlmAgent(
        name="Writer",
        model="gemini-2.0-flash",
        description="Agent that creates well-formatted reports.",
        instruction="Create clear, concise, and well-structured reports.",
        tools=[format_report]
    )
    
    # Create coordinator agent
    coordinator = LlmAgent(
        name="Coordinator",
        model="gemini-2.0-flash",
        description="Agent that coordinates research and report writing.",
        instruction="""
        You manage a team of specialized agents to answer user queries.
        1. Send research tasks to the Researcher
        2. Send report formatting tasks to the Writer
        3. Combine their work into a comprehensive answer
        """,
        sub_agents=[researcher, writer]
    )
    
    # Process query with the coordinator
    response = coordinator.respond(query)
    
    return response

# Example usage
if __name__ == "__main__":
    if not ADK_AVAILABLE:
        print("Google ADK is not installed. Run 'pip install google-adk' to use this example.")
        sys.exit(1)
    
    # Get query from command line or use default
    query = sys.argv[1] if len(sys.argv) > 1 else "Create a report about climate change impacts."
    
    print(f"Query: {query}")
    print("-" * 50)
    
    response = run_adk_multi_agent(query)
    print(f"Response: {response}")
    print("-" * 50)
    print("Check the console output above for the trace information.")