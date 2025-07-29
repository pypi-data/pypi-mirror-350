"""Example of tracing OpenAI API calls directly."""

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

# Traced function using OpenAI API directly
@trace_agent
def generate_response(prompt):
    """Generate a response using OpenAI."""
    try:
        import openai
        
        # Check for API key
        if not os.environ.get("OPENAI_API_KEY"):
            return "Error: OPENAI_API_KEY environment variable not set"
        
        # Initialize client
        client = openai.OpenAI()
        
        # Generate response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        
        # Return generated text
        return response.choices[0].message.content
    except ImportError:
        return "Error: OpenAI package not installed. Run 'pip install openai'"
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Get prompt from command line or use default
    prompt = sys.argv[1] if len(sys.argv) > 1 else "What is machine learning?"
    
    print(f"Prompt: {prompt}")
    print("-" * 50)
    
    response = generate_response(prompt)
    print(f"Response: {response}")
    print("-" * 50)
    print("Check the console output above for the trace information.")