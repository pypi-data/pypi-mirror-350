"""
Simple integration example demonstrating the new lightweight approach.

This example shows how easy it is to enable Arc tracing with the
integration-first approach that leverages existing tracing systems.
"""

import logging
from arc_tracing import enable_arc_tracing, trace_agent

# Configure logging to see integration activity
logging.basicConfig(level=logging.INFO)

def main():
    """Demonstrate simple Arc tracing integration."""
    
    print("=== Arc Tracing SDK - Integration Example ===\n")
    
    # 1. Enable Arc tracing for all available frameworks
    print("1. Enabling Arc tracing for all available frameworks...")
    results = enable_arc_tracing()
    
    print("Integration results:")
    for framework, success in results.items():
        status = "✓ Enabled" if success else "✗ Not available"
        print(f"  {framework}: {status}")
    print()
    
    # 2. Use the @trace_agent decorator as usual
    @trace_agent
    def simple_agent(query: str) -> str:
        """Simple agent function that will be traced."""
        print(f"Processing query: {query}")
        
        # Simulate some processing
        import time
        time.sleep(0.1)
        
        response = f"Processed: {query}"
        print(f"Response: {response}")
        return response
    
    # 3. Run the agent - tracing happens automatically
    print("2. Running traced agent...")
    result = simple_agent("What is the weather like today?")
    print(f"Agent result: {result}\n")
    
    # 4. Check integration status
    print("3. Integration status:")
    from arc_tracing.integrations import get_integration_status
    status = get_integration_status()
    
    for framework, info in status.items():
        available = "✓" if info["available"] else "✗"
        enabled = "✓" if info["enabled"] else "✗"
        print(f"  {framework}:")
        print(f"    Available: {available}")
        print(f"    Enabled: {enabled}")
    
    print("\n=== Integration Complete ===")
    print("Traces are being sent to Arc platform with minimal overhead!")

if __name__ == "__main__":
    main()