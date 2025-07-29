# Arc Tracing SDK Plugin Development Guide

The Arc Tracing SDK provides a lightweight, framework-agnostic architecture inspired by NVIDIA AIQ's plugin system. This guide shows you how to extend the SDK to support any AI framework through community-driven plugins.

## Plugin Architecture Overview

The Arc Tracing SDK uses a three-layer architecture for universal coverage:

1. **Built-in Integrations**: Modern frameworks (OpenAI Agents, LangGraph, LlamaIndex)
2. **API Interceptors**: Universal coverage via HTTP/API interception (OpenAI, Anthropic, Generic)
3. **Plugin System**: Community-driven extensions for any framework

## Quick Start: Creating a Plugin

### Option 1: Function-Based Plugin (Simplest)

```python
from arc_tracing.plugins import prompt_extractor_plugin

@prompt_extractor_plugin("my_framework_extractor", "my_framework", "1.0.0")
def extract_my_framework_prompt(trace_data):
    """Extract system prompt from my framework."""
    
    # Check if this trace is from your framework
    if trace_data.get("framework") != "my_framework":
        return None
    
    # Extract the system prompt from your framework's trace format
    system_prompt = trace_data.get("agent", {}).get("system_prompt")
    template_vars = trace_data.get("template_variables")
    
    if system_prompt:
        return (system_prompt, template_vars, "my_framework")
    
    return None
```

### Option 2: Class-Based Plugin (Full Control)

```python
from arc_tracing.plugins import PromptExtractorPlugin
from typing import Any, Dict, Optional, Tuple

class MyFrameworkPlugin(PromptExtractorPlugin):
    @property
    def name(self) -> str:
        return "my_framework_extractor"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def framework(self) -> str:
        return "my_framework"
    
    def is_available(self) -> bool:
        try:
            import my_framework
            return True
        except ImportError:
            return False
    
    def setup(self) -> bool:
        # Optional: Set up instrumentation
        return True
    
    def teardown(self) -> None:
        # Optional: Clean up
        pass
    
    def detect_framework_usage(self, trace_data: Dict[str, Any]) -> bool:
        # Detect if this trace comes from your framework
        return (
            trace_data.get("framework") == "my_framework" or
            "my_framework" in trace_data.get("metadata", {}).get("libraries", [])
        )
    
    def extract_system_prompt(self, trace_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
        # Your extraction logic here
        agent_config = trace_data.get("agent_config", {})
        
        system_prompt = (
            agent_config.get("system_prompt") or
            agent_config.get("instructions") or
            agent_config.get("persona")
        )
        
        if system_prompt:
            template_vars = agent_config.get("template_vars")
            return (system_prompt, template_vars, "my_framework")
        
        return None
```

## Framework-Specific Examples

### Agno (Phidata) Plugin

```python
@prompt_extractor_plugin("agno_extractor", "agno", "1.0.0")
def extract_agno_prompt(trace_data):
    """Extract system prompt from Agno framework."""
    if trace_data.get("framework") != "agno":
        return None
    
    # Method 1: From agent configuration
    agent = trace_data.get("agent", {})
    if isinstance(agent, dict):
        system_prompt = (
            agent.get("system_prompt") or
            agent.get("instructions") or
            agent.get("persona")
        )
        if system_prompt:
            return (system_prompt, agent.get("template_vars"), "agno")
    
    # Method 2: From session data
    session = trace_data.get("session", {})
    if isinstance(session, dict):
        system_message = session.get("system_message")
        if system_message:
            return (system_message, None, "agno")
    
    return None
```

### CrewAI Plugin

```python
@prompt_extractor_plugin("crewai_extractor", "crewai", "1.0.0")
def extract_crewai_prompt(trace_data):
    """Extract system prompt from CrewAI framework."""
    if trace_data.get("framework") != "crewai":
        return None
    
    # CrewAI uses role, goal, and backstory
    agent = trace_data.get("agent", {})
    if isinstance(agent, dict):
        role = agent.get("role")
        goal = agent.get("goal") 
        backstory = agent.get("backstory")
        
        if role or goal or backstory:
            prompt_parts = []
            if role:
                prompt_parts.append(f"Role: {role}")
            if goal:
                prompt_parts.append(f"Goal: {goal}")
            if backstory:
                prompt_parts.append(f"Backstory: {backstory}")
            
            system_prompt = "\n".join(prompt_parts)
            return (system_prompt, None, "crewai")
    
    return None
```

### AutoGen Plugin

```python
@prompt_extractor_plugin("autogen_extractor", "autogen", "1.0.0")
def extract_autogen_prompt(trace_data):
    """Extract system prompt from AutoGen framework."""
    if trace_data.get("framework") != "autogen":
        return None
    
    # AutoGen uses system_message in agent config
    agent_config = trace_data.get("agent_config", {})
    if isinstance(agent_config, dict):
        system_message = agent_config.get("system_message")
        if system_message:
            return (system_message, None, "autogen")
    
    # Check conversation history
    messages = trace_data.get("messages", [])
    if messages and isinstance(messages, list):
        for msg in messages:
            if isinstance(msg, dict) and msg.get("role") == "system":
                return (msg.get("content"), None, "autogen")
    
    return None
```

## Plugin Distribution

### Method 1: Entry Points (Recommended)

Add to your `setup.py` or `pyproject.toml`:

```toml
[project.entry-points."arc_tracing.plugins"]
my_framework = "my_package.plugins:MyFrameworkPlugin"
```

### Method 2: Local Installation

1. Create a plugin file in `~/.arc_tracing/plugins/my_plugin.py`
2. The SDK will automatically discover and load it

### Method 3: Package Installation

```python
# In your package's __init__.py
from arc_tracing.plugins import get_plugin_manager

# Register your plugin
plugin_manager = get_plugin_manager()
plugin_manager._register_plugin(MyFrameworkPlugin())
```

## Advanced Plugin Features

### Multiple Extraction Methods

```python
def extract_complex_framework_prompt(trace_data):
    # Try multiple extraction strategies
    
    # Strategy 1: From agent configuration
    if "agent_config" in trace_data:
        result = _extract_from_agent_config(trace_data["agent_config"])
        if result:
            return result
    
    # Strategy 2: From workflow definition
    if "workflow" in trace_data:
        result = _extract_from_workflow(trace_data["workflow"])
        if result:
            return result
    
    # Strategy 3: From conversation history
    if "conversation" in trace_data:
        result = _extract_from_conversation(trace_data["conversation"])
        if result:
            return result
    
    return None
```

### Template Variable Extraction

```python
def extract_with_templates(trace_data):
    system_prompt = trace_data.get("prompt_template")
    template_vars = trace_data.get("variables", {})
    
    if system_prompt and template_vars:
        return (system_prompt, template_vars, "my_framework")
    
    return None
```

### Framework Detection Heuristics

```python
def detect_framework_usage(self, trace_data):
    # Multiple detection methods
    
    # Method 1: Explicit framework field
    if trace_data.get("framework") == "my_framework":
        return True
    
    # Method 2: Check imported libraries
    libraries = trace_data.get("metadata", {}).get("libraries", [])
    if "my_framework" in libraries:
        return True
    
    # Method 3: Check trace structure
    if ("my_framework_agent" in trace_data or 
        "my_framework_config" in trace_data):
        return True
    
    # Method 4: Check for framework-specific fields
    required_fields = ["my_framework_version", "my_framework_agent_id"]
    if all(field in trace_data for field in required_fields):
        return True
    
    return False
```

## Testing Your Plugin

```python
def test_my_plugin():
    from arc_tracing.plugins import get_plugin_manager
    
    # Test plugin discovery
    plugin_manager = get_plugin_manager()
    plugin_manager.discover_plugins()
    
    # Test plugin is loaded
    plugin = plugin_manager.get_plugin("my_framework_extractor")
    assert plugin is not None
    
    # Test prompt extraction
    test_trace_data = {
        "framework": "my_framework",
        "agent": {
            "system_prompt": "You are a helpful assistant.",
            "template_vars": {"name": "test"}
        }
    }
    
    result = plugin.extract_system_prompt(test_trace_data)
    assert result is not None
    
    prompt_text, template_vars, source = result
    assert prompt_text == "You are a helpful assistant."
    assert template_vars == {"name": "test"}
    assert source == "my_framework"
```

## Plugin Best Practices

### 1. Robust Error Handling

```python
def extract_system_prompt(self, trace_data):
    try:
        # Your extraction logic
        return self._safe_extract(trace_data)
    except Exception as e:
        logger.warning(f"Plugin {self.name} failed: {e}")
        return None
```

### 2. Efficient Framework Detection

```python
def detect_framework_usage(self, trace_data):
    # Quick checks first
    if trace_data.get("framework") == "my_framework":
        return True
    
    # More expensive checks only if needed
    return self._deep_framework_analysis(trace_data)
```

### 3. Privacy-Aware Extraction

```python
def extract_system_prompt(self, trace_data):
    prompt = self._get_raw_prompt(trace_data)
    
    if prompt:
        # Plugin doesn't need to sanitize - SDK handles this
        return (prompt, template_vars, "my_framework")
    
    return None
```

### 4. Version Compatibility

```python
def is_available(self):
    try:
        import my_framework
        # Check version compatibility
        if hasattr(my_framework, '__version__'):
            version = my_framework.__version__
            return self._is_supported_version(version)
        return True
    except ImportError:
        return False
```

## Plugin Discovery

The SDK automatically discovers plugins from:

1. **Entry points**: `arc_tracing.plugins` group
2. **Local directories**: `~/.arc_tracing/plugins/`, `./arc_plugins/`, `./plugins/`
3. **Built-in plugins**: Included with the SDK

## Sharing Your Plugin

1. **GitHub**: Create a repository with your plugin
2. **PyPI**: Publish as a package with entry points
3. **Arc Community**: Submit to the official plugin registry
4. **Documentation**: Include usage examples and trace format specs

## Getting Help

- Check existing plugins in `arc_tracing/plugins/plugin_interface.py`
- Review framework-specific examples above
- Join the Arc community for plugin development support
- Test with the provided plugin testing utilities

The plugin system is designed to be as simple as possible while providing maximum flexibility. Start with a function-based plugin and upgrade to a class-based plugin as your needs grow!