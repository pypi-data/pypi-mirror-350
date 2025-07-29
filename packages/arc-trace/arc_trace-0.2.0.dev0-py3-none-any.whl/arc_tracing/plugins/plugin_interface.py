"""Plugin interface for community-driven integrations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

class PluginInterface(ABC):
    """
    Base interface for Arc Tracing SDK plugins.
    
    This interface follows the NVIDIA AIQ plugin pattern with entry points
    and decorators for easy community-driven extension.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name (should be unique)."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass
    
    @property 
    @abstractmethod
    def framework(self) -> str:
        """Target framework name (e.g., 'agno', 'crewai', 'semantic_kernel')."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the target framework is available."""
        pass
    
    @abstractmethod
    def setup(self) -> bool:
        """Set up the plugin integration."""
        pass
    
    @abstractmethod
    def teardown(self) -> None:
        """Clean up the plugin integration.""" 
        pass

class PromptExtractorPlugin(PluginInterface):
    """
    Specialized plugin interface for system prompt extraction.
    
    This is the most common plugin type - extracting system prompts
    from framework-specific trace data.
    """
    
    @abstractmethod
    def extract_system_prompt(self, trace_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
        """
        Extract system prompt from framework-specific trace data.
        
        Args:
            trace_data: Framework-specific trace data
            
        Returns:
            Tuple of (prompt_text, template_variables, prompt_source) or None if no prompt found
        """
        pass
    
    @abstractmethod
    def detect_framework_usage(self, trace_data: Dict[str, Any]) -> bool:
        """
        Detect if this trace data comes from the target framework.
        
        Args:
            trace_data: Trace data to analyze
            
        Returns:
            True if this plugin should handle this trace data
        """
        pass
    
    def get_supported_trace_types(self) -> List[str]:
        """
        Get list of trace types this plugin supports.
        
        Returns:
            List of trace type identifiers
        """
        return ["generic"]
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get plugin metadata for registration and discovery.
        
        Returns:
            Dictionary with plugin metadata
        """
        return {
            "name": self.name,
            "version": self.version,
            "framework": self.framework,
            "type": "prompt_extractor",
            "supported_trace_types": self.get_supported_trace_types(),
            "description": getattr(self, 'description', f"Prompt extractor for {self.framework}"),
            "author": getattr(self, 'author', "Community"),
            "homepage": getattr(self, 'homepage', None),
        }

# Decorator for easy plugin registration
def prompt_extractor_plugin(name: str, framework: str, version: str = "1.0.0"):
    """
    Decorator to register a function as a prompt extractor plugin.
    
    This provides a simple way for community members to create plugins
    without implementing the full interface.
    
    Args:
        name: Plugin name
        framework: Target framework name
        version: Plugin version
        
    Example:
        @prompt_extractor_plugin("agno_extractor", "agno")
        def extract_agno_prompt(trace_data):
            # Check if this is agno trace data
            if not trace_data.get("framework") == "agno":
                return None
                
            # Extract prompt from agno-specific format
            system_prompt = trace_data.get("agent", {}).get("system_prompt")
            if system_prompt:
                return (system_prompt, None, "agno")
            return None
    """
    def decorator(func):
        class FunctionPlugin(PromptExtractorPlugin):
            @property
            def name(self) -> str:
                return name
            
            @property
            def version(self) -> str:
                return version
            
            @property
            def framework(self) -> str:
                return framework
            
            def is_available(self) -> bool:
                # Try to import the framework
                try:
                    __import__(framework)
                    return True
                except ImportError:
                    return False
            
            def setup(self) -> bool:
                return True  # Function-based plugins don't need setup
            
            def teardown(self) -> None:
                pass  # Function-based plugins don't need teardown
            
            def extract_system_prompt(self, trace_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
                return func(trace_data)
            
            def detect_framework_usage(self, trace_data: Dict[str, Any]) -> bool:
                # Simple detection based on framework field
                return trace_data.get("framework") == framework
        
        # Create plugin instance and register it
        plugin_instance = FunctionPlugin()
        
        # Add plugin metadata to function for discovery
        func._arc_plugin = plugin_instance
        func._arc_plugin_metadata = plugin_instance.get_metadata()
        
        return func
    
    return decorator

# Built-in example plugins for common frameworks
@prompt_extractor_plugin("agno_extractor", "agno", "1.0.0")
def extract_agno_prompt(trace_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
    """
    Example plugin for Agno framework.
    
    This serves as a template for community-contributed plugins.
    """
    try:
        # Check if this is agno trace data
        if trace_data.get("framework") != "agno":
            return None
        
        # Method 1: Extract from agent configuration
        agent_config = trace_data.get("agent", {})
        if isinstance(agent_config, dict):
            system_prompt = (
                agent_config.get("system_prompt") or
                agent_config.get("instructions") or
                agent_config.get("persona")
            )
            if system_prompt:
                template_vars = agent_config.get("template_vars")
                return (system_prompt, template_vars, "agno")
        
        # Method 2: Extract from session data
        session_data = trace_data.get("session", {})
        if isinstance(session_data, dict):
            system_prompt = session_data.get("system_message")
            if system_prompt:
                return (system_prompt, None, "agno")
        
        # Method 3: Extract from knowledge base context
        knowledge = trace_data.get("knowledge", {})
        if isinstance(knowledge, dict):
            context = knowledge.get("context")
            if context and isinstance(context, str) and len(context) > 50:
                return (f"Knowledge-based agent with context: {context[:200]}...", None, "agno")
        
        return None
        
    except Exception:
        return None

@prompt_extractor_plugin("crewai_extractor", "crewai", "1.0.0") 
def extract_crewai_prompt(trace_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
    """
    Example plugin for CrewAI framework.
    """
    try:
        # Check if this is CrewAI trace data
        if trace_data.get("framework") != "crewai":
            return None
        
        # Method 1: Extract from agent definition
        agent_data = trace_data.get("agent", {})
        if isinstance(agent_data, dict):
            backstory = agent_data.get("backstory")
            role = agent_data.get("role")
            goal = agent_data.get("goal")
            
            if backstory or role or goal:
                prompt_parts = []
                if role:
                    prompt_parts.append(f"Role: {role}")
                if goal:
                    prompt_parts.append(f"Goal: {goal}")
                if backstory:
                    prompt_parts.append(f"Backstory: {backstory}")
                
                system_prompt = "\n".join(prompt_parts)
                return (system_prompt, None, "crewai")
        
        # Method 2: Extract from crew configuration
        crew_data = trace_data.get("crew", {})
        if isinstance(crew_data, dict):
            process = crew_data.get("process")
            if process:
                return (f"CrewAI agent in {process} process", None, "crewai")
        
        return None
        
    except Exception:
        return None