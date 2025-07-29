"""Base integration class for Arc Tracing SDK."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple
from arc_tracing.config import get_config

logger = logging.getLogger("arc_tracing")

class BaseIntegration(ABC):
    """
    Base class for all framework integrations.
    
    This class provides the common interface and functionality for
    integrating with different AI frameworks in a lightweight manner.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.enabled = False
        self.config = get_config()
        self._original_handlers = {}
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the framework is available for integration."""
        pass
    
    @abstractmethod
    def _setup_integration(self) -> bool:
        """Set up the integration with the framework."""
        pass
    
    @abstractmethod
    def _teardown_integration(self) -> None:
        """Clean up the integration."""
        pass
    
    @abstractmethod
    def extract_system_prompt(self, trace_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
        """
        Extract system prompt from framework-specific trace data.
        
        Args:
            trace_data: Framework-specific trace data
            
        Returns:
            Tuple of (prompt_text, template_variables, prompt_source) or None if no prompt found.
            - prompt_text: The actual system prompt content
            - template_variables: Dictionary of template variables if templated, None otherwise
            - prompt_source: Source identifier (e.g., "openai_agents", "langgraph", "direct_api")
        """
        pass
    
    def enable(self) -> bool:
        """
        Enable the integration if the framework is available.
        
        Returns:
            True if integration was successfully enabled, False otherwise.
        """
        if self.enabled:
            logger.debug(f"{self.name} integration already enabled")
            return True
            
        if not self.is_available():
            logger.debug(f"{self.name} framework not available, skipping integration")
            return False
        
        try:
            success = self._setup_integration()
            if success:
                self.enabled = True
                logger.info(f"Successfully enabled {self.name} integration")
            else:
                logger.warning(f"Failed to enable {self.name} integration")
            return success
        except Exception as e:
            logger.error(f"Error enabling {self.name} integration: {e}")
            return False
    
    def disable(self) -> None:
        """Disable the integration and clean up."""
        if not self.enabled:
            return
            
        try:
            self._teardown_integration()
            self.enabled = False
            logger.info(f"Disabled {self.name} integration")
        except Exception as e:
            logger.error(f"Error disabling {self.name} integration: {e}")
    
    def format_trace_for_arc(self, trace_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert framework-specific trace data to Arc format.
        
        Args:
            trace_data: Original trace data from the framework
            
        Returns:
            Formatted trace data for Arc platform
        """
        # Base formatting - subclasses can override
        arc_trace = {
            "framework": self.name,
            "timestamp": trace_data.get("timestamp"),
            "trace_id": trace_data.get("trace_id"),
            "span_id": trace_data.get("span_id"),
            "operation": trace_data.get("operation_name", "unknown"),
            "metadata": {
                "sdk_version": "0.1.0",
                "integration_type": "adapter",
                "original_format": self.name
            }
        }
        
        # Add Arc-specific attributes
        if self.config.project_id:
            arc_trace["project_id"] = self.config.project_id
        if self.config.agent_id:
            arc_trace["agent_id"] = self.config.agent_id
        
        # Extract and add system prompt if enabled
        if self.config.get("trace.capture_prompts", True):
            prompt_data = self.extract_system_prompt(trace_data)
            
            # Fallback to plugin system if no prompt found
            if not prompt_data:
                try:
                    from arc_tracing.plugins import get_plugin_manager
                    plugin_manager = get_plugin_manager()
                    prompt_data = plugin_manager.extract_prompt_with_plugins(trace_data)
                except Exception as e:
                    logger.warning(f"Plugin system failed to extract prompt: {e}")
            
            if prompt_data:
                prompt_text, template_vars, prompt_source = prompt_data
                
                # Sanitize prompt before adding to trace
                sanitized_prompt = self._sanitize_prompt(prompt_text)
                
                arc_trace["system_prompt"] = sanitized_prompt
                arc_trace["prompt_source"] = prompt_source
                arc_trace["prompt_extraction_method"] = "automatic"
                
                if template_vars:
                    arc_trace["prompt_template_vars"] = template_vars
                    
                # Add to metadata for backend compatibility
                arc_trace["metadata"]["system_prompt"] = sanitized_prompt
                arc_trace["metadata"]["prompt_source"] = prompt_source
                arc_trace["metadata"]["prompt_template_vars"] = template_vars
            
        return arc_trace
    
    def send_to_arc(self, trace_data: Dict[str, Any]) -> None:
        """
        Send trace data to Arc platform.
        
        Args:
            trace_data: Formatted trace data for Arc
        """
        try:
            # Format for Arc platform
            arc_trace = self.format_trace_for_arc(trace_data)
            
            # Use existing Arc exporter
            from arc_tracing.exporters.arc_exporter import ArcExporter
            exporter = ArcExporter()
            
            # Convert to span-like object for exporter compatibility
            # This is a lightweight wrapper to reuse existing export logic
            mock_span = MockSpan(arc_trace)
            exporter.export([mock_span])
            
        except Exception as e:
            logger.error(f"Error sending {self.name} trace to Arc: {e}")
    
    def _sanitize_prompt(self, prompt_text: str) -> str:
        """
        Sanitize prompt text for privacy and security.
        
        Args:
            prompt_text: Raw prompt text to sanitize
            
        Returns:
            Sanitized prompt text
        """
        try:
            from arc_tracing.utils.prompt_sanitizer import sanitize_prompt
            return sanitize_prompt(prompt_text, self.config)
        except ImportError:
            # Fallback sanitization if utils not available
            logger.warning("Prompt sanitizer not available, using basic truncation")
            max_length = self.config.get("trace.prompt_privacy.max_length", 2000)
            if len(prompt_text) > max_length:
                return prompt_text[:max_length] + "...[TRUNCATED]"
            return prompt_text

class MockSpan:
    """Lightweight span wrapper for Arc exporter compatibility."""
    
    def __init__(self, trace_data: Dict[str, Any]):
        self.name = trace_data.get("operation", "unknown")
        self.context = MockContext(
            trace_data.get("trace_id", "unknown"),
            trace_data.get("span_id", "unknown")
        )
        self.parent = None
        self.start_time = trace_data.get("start_time", 0)
        self.end_time = trace_data.get("end_time", 0)
        self.status = MockStatus()
        
        # Build attributes from trace data including prompt information
        self.attributes = trace_data.get("attributes", {}).copy()
        
        # Add prompt-related attributes if present
        if "system_prompt" in trace_data:
            self.attributes["arc_tracing.agent.system_prompt"] = trace_data["system_prompt"]
        if "prompt_source" in trace_data:
            self.attributes["arc_tracing.agent.prompt_source"] = trace_data["prompt_source"]
        if "prompt_template_vars" in trace_data:
            import json
            self.attributes["arc_tracing.agent.prompt_template_vars"] = json.dumps(trace_data["prompt_template_vars"])
        if "prompt_extraction_method" in trace_data:
            self.attributes["arc_tracing.agent.prompt_extraction_method"] = trace_data["prompt_extraction_method"]
        
        # Add standard Arc tracing attributes
        if "framework" in trace_data:
            self.attributes["arc_tracing.framework"] = trace_data["framework"]
        if "project_id" in trace_data:
            self.attributes["arc_tracing.project_id"] = trace_data["project_id"]
        if "agent_id" in trace_data:
            self.attributes["arc_tracing.agent_id"] = trace_data["agent_id"]
            
        self.events = trace_data.get("events", [])
        self.links = trace_data.get("links", [])

class MockContext:
    """Mock context for span compatibility."""
    
    def __init__(self, trace_id: str, span_id: str):
        self.trace_id = trace_id
        self.span_id = span_id
        self.is_remote = False

class MockStatus:
    """Mock status for span compatibility."""
    
    def __init__(self):
        self.status_code = 0  # OK
        self.description = None