# Integration Examples - Lightweight Approach

This directory contains examples demonstrating the **new integration-first approach** that leverages existing tracing systems rather than monkey patching framework internals.

## 🎯 Integration Philosophy

### **Old Approach (Phase 1 - Deprecated)**
```python
# Heavy monkey patching
from arc_tracing.frameworks import openai_agents
openai_agents.patch()  # ❌ Modifies framework internals
```

### **New Approach (Phase 1.5 - Recommended)**
```python
# Lightweight integration adapters
from arc_tracing import enable_arc_tracing
enable_arc_tracing()  # ✅ Hooks into existing tracing
```

## 📁 Example Files

### **1. `simple_integration.py`**
- **Purpose**: Basic integration example
- **Shows**: Single-line enablement and status checking
- **Use Case**: Getting started with Arc tracing

### **2. `framework_specific.py`**
- **Purpose**: Framework-specific integration control
- **Shows**: Selective framework enablement and benefits
- **Use Case**: Fine-grained control over integrations

### **3. `migration_guide.py`**  
- **Purpose**: Migration from old to new approach
- **Shows**: Step-by-step migration process
- **Use Case**: Updating existing implementations

## 🚀 Quick Start

### **Enable All Frameworks**
```python
from arc_tracing import enable_arc_tracing, trace_agent

# Single line to enable all available frameworks
enable_arc_tracing()

@trace_agent
def my_agent(query: str) -> str:
    # Your agent code here
    return response
```

### **Enable Specific Frameworks**
```python
from arc_tracing import enable_arc_tracing

# Enable only specific frameworks
results = enable_arc_tracing(["openai_agents", "langgraph"])
print(results)  # {"openai_agents": True, "langgraph": False}
```

### **Individual Framework Control**
```python
from arc_tracing.integrations import openai_agents, langgraph

# Enable individual frameworks
openai_agents.enable()
langgraph.enable()

# Check status
print(f"OpenAI Agents: {openai_agents.enabled}")
print(f"LangGraph: {langgraph.enabled}")
```

## 🔧 Framework Integration Details

### **OpenAI Agents SDK**
- **Built-in Feature**: Comprehensive tracing with `add_trace_processor()`
- **Integration**: Hooks into existing processor pipeline
- **Benefits**: LLM calls, tool usage, handoffs automatically traced

### **LangGraph + LangSmith**
- **Built-in Feature**: LangSmith observability integration
- **Integration**: Extends LangSmith with Arc metadata
- **Benefits**: State graphs, node execution, edge transitions

### **LlamaIndex**
- **Built-in Feature**: Multiple observability backends supported
- **Integration**: Registers as additional handler via `set_global_handler()`
- **Benefits**: Compatible with Langfuse, MLflow, Phoenix, etc.

## ⚡ Performance Benefits

| Aspect | Old Approach | New Approach |
|--------|-------------|--------------|
| **Setup** | Heavy patching | Lightweight hooks |
| **Runtime** | Every call overhead | Zero overhead when disabled |
| **Compatibility** | Brittle to updates | Framework-update resilient |
| **Conflicts** | Interferes with built-in tracing | Extends existing tracing |
| **Debugging** | Complex stack traces | Clear trace paths |

## 🔄 Migration Guide

### **Step 1: Update Imports**
```python
# BEFORE
from arc_tracing.frameworks import openai_agents
openai_agents.patch()

# AFTER  
from arc_tracing import enable_arc_tracing
enable_arc_tracing()
```

### **Step 2: Keep Everything Else**
- ✅ `@trace_agent` decorator works exactly the same
- ✅ Trace data format unchanged
- ✅ Arc platform integration unchanged
- ✅ Configuration system unchanged

## 🎯 Use Cases

### **Development**
```python
# Quick setup for development
from arc_tracing import enable_arc_tracing
enable_arc_tracing()  # Auto-detects available frameworks
```

### **Production**
```python
# Explicit control for production
from arc_tracing import enable_arc_tracing

# Enable only frameworks you use
results = enable_arc_tracing(["openai_agents", "llamaindex"])

# Verify what's enabled
if not any(results.values()):
    raise RuntimeError("No Arc integrations enabled")
```

### **Testing**
```python
# Clean setup/teardown for tests
from arc_tracing.integrations import disable_arc_tracing

def setup_test():
    enable_arc_tracing(["openai_agents"])

def teardown_test():
    disable_arc_tracing()  # Clean state
```

## 🛡️ Production Considerations

### **Graceful Degradation**
- Works even if Arc platform is unavailable
- Continues if frameworks are not installed
- Fails safely without breaking agent execution

### **Performance**
- Zero overhead when tracing is disabled
- Leverages optimized built-in tracing systems
- Batched export to Arc platform

### **Monitoring**
```python
# Check integration health
from arc_tracing.integrations import get_integration_status

status = get_integration_status()
for framework, info in status.items():
    print(f"{framework}: available={info['available']}, enabled={info['enabled']}")
```

## 📈 Next Steps

1. **Run Examples**: Try each example to understand the integration approach
2. **Migrate Code**: Update existing implementations using the migration guide
3. **Test Integration**: Verify tracing works with your specific frameworks
4. **Monitor Status**: Use status functions to monitor integration health

The integration-first approach provides a **production-ready, lightweight, and scalable** foundation for Arc tracing across all modern AI frameworks.