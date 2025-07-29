"""
Framework-specific integration examples.

This example demonstrates how to enable Arc tracing for specific
frameworks and shows the difference between the old and new approaches.
"""

import logging
from arc_tracing import enable_arc_tracing

# Configure logging to see integration activity  
logging.basicConfig(level=logging.INFO)

def demonstrate_specific_framework_integration():
    """Show how to enable specific framework integrations."""
    
    print("=== Framework-Specific Integration Example ===\n")
    
    # Enable only specific frameworks
    print("1. Enabling only OpenAI Agents SDK and LangGraph...")
    results = enable_arc_tracing(["openai_agents", "langgraph"])
    
    for framework, success in results.items():
        if success:
            print(f"✓ {framework} integration active")
        else:
            print(f"✗ {framework} not available or failed")
    print()
    
    # Show individual integration control
    print("2. Individual integration control:")
    from arc_tracing.integrations import openai_agents, langgraph, llamaindex
    
    # Check what's available
    print(f"OpenAI Agents SDK available: {openai_agents.is_available()}")
    print(f"LangGraph available: {langgraph.is_available()}")  
    print(f"LlamaIndex available: {llamaindex.is_available()}")
    print()
    
    # Enable LlamaIndex specifically if available
    if llamaindex.is_available():
        print("3. Enabling LlamaIndex integration specifically...")
        success = llamaindex.enable()
        print(f"LlamaIndex integration: {'✓ Success' if success else '✗ Failed'}")
    else:
        print("3. LlamaIndex not available - skipping")
    print()

def demonstrate_integration_benefits():
    """Show the benefits of the integration approach."""
    
    print("=== Integration Approach Benefits ===\n")
    
    print("OLD APPROACH (Monkey Patching):")
    print("❌ Heavy - modifies framework internals")
    print("❌ Brittle - breaks with framework updates") 
    print("❌ Conflicts - interferes with existing tracing")
    print("❌ Performance - overhead on every function call")
    print("❌ Complex - hard to debug and maintain")
    print()
    
    print("NEW APPROACH (Integration Adapters):")
    print("✅ Lightweight - hooks into existing tracing")
    print("✅ Robust - survives framework updates")
    print("✅ Compatible - extends rather than replaces")
    print("✅ Fast - zero overhead when not tracing")
    print("✅ Clear - transparent and debuggable")
    print()
    
    print("FRAMEWORK SUPPORT:")
    print("🚀 OpenAI Agents SDK - hooks into built-in tracing")
    print("🚀 LangGraph - extends LangSmith observability") 
    print("🚀 LlamaIndex - registers with observability system")
    print("📚 Legacy frameworks - gradual migration to adapters")
    print()

def demonstrate_production_ready():
    """Show production-ready features."""
    
    print("=== Production-Ready Features ===\n")
    
    # Graceful degradation
    print("1. Graceful degradation:")
    print("   - Works even if Arc platform is unavailable")
    print("   - Continues if framework is not installed") 
    print("   - Fails safely without breaking agent execution")
    print()
    
    # Performance characteristics
    print("2. Performance characteristics:")
    print("   - Zero overhead when tracing is disabled")
    print("   - Minimal overhead when tracing is enabled") 
    print("   - Leverages optimized built-in tracing systems")
    print("   - Batched export to Arc platform")
    print()
    
    # Developer experience
    print("3. Developer experience:")
    print("   - Single line to enable: enable_arc_tracing()")
    print("   - Framework auto-detection")
    print("   - Clear integration status reporting")
    print("   - Easy cleanup with disable_arc_tracing()")
    print()

if __name__ == "__main__":
    demonstrate_specific_framework_integration()
    print()
    demonstrate_integration_benefits()
    print()
    demonstrate_production_ready()