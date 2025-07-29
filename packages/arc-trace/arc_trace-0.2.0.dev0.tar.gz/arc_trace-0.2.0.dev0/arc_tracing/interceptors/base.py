"""Base interceptor class for API interception."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Callable
from arc_tracing.config import get_config

logger = logging.getLogger("arc_tracing")

class BaseInterceptor(ABC):
    """
    Base class for API interceptors.
    
    Interceptors provide framework-agnostic tracing by capturing API calls
    at the HTTP/client level, regardless of which framework is making the calls.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.enabled = False
        self.config = get_config()
        self._original_methods = {}
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the target API client is available for interception."""
        pass
    
    @abstractmethod
    def _setup_interception(self) -> bool:
        """Set up API call interception."""
        pass
    
    @abstractmethod
    def _teardown_interception(self) -> None:
        """Clean up API call interception."""
        pass
    
    @abstractmethod
    def extract_system_prompt(self, call_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
        """
        Extract system prompt from API call data.
        
        Args:
            call_data: API call data (request/response)
            
        Returns:
            Tuple of (prompt_text, template_variables, prompt_source) or None if no prompt found
        """
        pass
    
    def enable(self) -> bool:
        """
        Enable API interception if the target client is available.
        
        Returns:
            True if interception was successfully enabled, False otherwise.
        """
        if self.enabled:
            logger.debug(f"{self.name} interceptor already enabled")
            return True
            
        if not self.is_available():
            logger.debug(f"{self.name} API client not available, skipping interception")
            return False
        
        try:
            success = self._setup_interception()
            if success:
                self.enabled = True
                logger.info(f"Successfully enabled {self.name} API interception")
            else:
                logger.warning(f"Failed to enable {self.name} API interception")
            return success
        except Exception as e:
            logger.error(f"Error enabling {self.name} API interception: {e}")
            return False
    
    def disable(self) -> None:
        """Disable API interception and clean up."""
        if not self.enabled:
            return
            
        try:
            self._teardown_interception()
            self.enabled = False
            logger.info(f"Disabled {self.name} API interception")
        except Exception as e:
            logger.error(f"Error disabling {self.name} API interception: {e}")
    
    def _create_traced_method(self, original_method: Callable, method_name: str) -> Callable:
        """
        Create a traced wrapper around an API method.
        
        Args:
            original_method: Original API method to wrap
            method_name: Name of the method for identification
            
        Returns:
            Wrapped method that captures trace data
        """
        def traced_method(*args, **kwargs):
            # Extract call data before execution
            call_data = self._extract_call_data(method_name, args, kwargs)
            
            try:
                # Execute original method
                result = original_method(*args, **kwargs)
                
                # Add response data
                call_data.update(self._extract_response_data(result))
                call_data["status"] = "success"
                
                # Send trace to Arc platform
                self._send_trace_to_arc(call_data)
                
                return result
                
            except Exception as e:
                # Add error information
                call_data["status"] = "error"
                call_data["error"] = str(e)
                
                # Send trace to Arc platform
                self._send_trace_to_arc(call_data)
                
                # Re-raise the exception
                raise
        
        return traced_method
    
    def _extract_call_data(self, method_name: str, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """
        Extract relevant data from API call arguments.
        
        Args:
            method_name: Name of the API method being called
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            Dictionary containing call data
        """
        import time
        
        return {
            "interceptor": self.name,
            "method": method_name,
            "timestamp": int(time.time() * 1_000_000_000),  # nanoseconds
            "args": self._sanitize_args(args),
            "kwargs": self._sanitize_kwargs(kwargs),
        }
    
    def _extract_response_data(self, result: Any) -> Dict[str, Any]:
        """
        Extract relevant data from API response.
        
        Args:
            result: API response object
            
        Returns:
            Dictionary containing response data
        """
        # Override in subclasses for API-specific response handling
        return {"response_type": type(result).__name__}
    
    def _sanitize_args(self, args: tuple) -> List[Any]:
        """Sanitize positional arguments for logging."""
        return [self._sanitize_value(arg) for arg in args]
    
    def _sanitize_kwargs(self, kwargs: dict) -> Dict[str, Any]:
        """Sanitize keyword arguments for logging."""
        return {k: self._sanitize_value(v) for k, v in kwargs.items()}
    
    def _sanitize_value(self, value: Any) -> Any:
        """Sanitize a single value for logging."""
        # Basic sanitization - override in subclasses for API-specific handling
        if isinstance(value, str) and len(value) > 500:
            return value[:500] + "...[TRUNCATED]"
        return value
    
    def _send_trace_to_arc(self, call_data: Dict[str, Any]) -> None:
        """
        Send API call trace to Arc platform.
        
        Args:
            call_data: Complete call and response data
        """
        try:
            # Extract system prompt if enabled
            prompt_data = None
            if self.config.get("trace.capture_prompts", True):
                prompt_data = self.extract_system_prompt(call_data)
            
            # Format for Arc platform
            arc_trace = self._format_trace_for_arc(call_data, prompt_data)
            
            # Use existing Arc exporter
            from arc_tracing.exporters.arc_exporter import ArcExporter
            from arc_tracing.integrations.base import MockSpan
            
            exporter = ArcExporter()
            mock_span = MockSpan(arc_trace)
            exporter.export([mock_span])
            
        except Exception as e:
            logger.error(f"Error sending {self.name} API trace to Arc: {e}")
    
    def _format_trace_for_arc(self, call_data: Dict[str, Any], prompt_data: Optional[Tuple[str, Optional[Dict[str, Any]], str]]) -> Dict[str, Any]:
        """
        Format API call data for Arc platform.
        
        Args:
            call_data: Raw API call data
            prompt_data: Extracted prompt data (if any)
            
        Returns:
            Formatted trace data for Arc platform
        """
        arc_trace = {
            "framework": "generic_api",
            "interceptor": self.name,
            "operation": f"{self.name}.{call_data.get('method', 'unknown')}",
            "timestamp": call_data.get("timestamp"),
            "trace_id": f"{self.name}_{call_data.get('timestamp')}",
            "span_id": f"span_{call_data.get('timestamp')}",
            "status": call_data.get("status", "unknown"),
            "metadata": {
                "sdk_version": "0.1.0",
                "integration_type": "api_interceptor",
                "method": call_data.get("method"),
                "interceptor": self.name,
            },
            "attributes": {
                f"arc_tracing.{self.name}.method": call_data.get("method"),
                f"arc_tracing.{self.name}.status": call_data.get("status"),
            }
        }
        
        # Add project/agent identification
        if self.config.project_id:
            arc_trace["project_id"] = self.config.project_id
            arc_trace["attributes"]["arc_tracing.project_id"] = self.config.project_id
        if self.config.agent_id:
            arc_trace["agent_id"] = self.config.agent_id
            arc_trace["attributes"]["arc_tracing.agent_id"] = self.config.agent_id
        
        # Add prompt data if extracted
        if prompt_data:
            prompt_text, template_vars, prompt_source = prompt_data
            
            # Sanitize prompt
            try:
                from arc_tracing.utils.prompt_sanitizer import sanitize_prompt
                sanitized_prompt = sanitize_prompt(prompt_text, self.config)
            except ImportError:
                # Fallback sanitization
                max_length = self.config.get("trace.prompt_privacy.max_length", 2000)
                if len(prompt_text) > max_length:
                    sanitized_prompt = prompt_text[:max_length] + "...[TRUNCATED]"
                else:
                    sanitized_prompt = prompt_text
            
            arc_trace.update({
                "system_prompt": sanitized_prompt,
                "prompt_source": prompt_source,
                "prompt_extraction_method": "api_interception",
            })
            
            if template_vars:
                arc_trace["prompt_template_vars"] = template_vars
            
            # Add to metadata for backend compatibility
            arc_trace["metadata"].update({
                "system_prompt": sanitized_prompt,
                "prompt_source": prompt_source,
                "prompt_template_vars": template_vars,
            })
            
            # Add to attributes for OpenTelemetry compatibility
            arc_trace["attributes"].update({
                "arc_tracing.agent.system_prompt": sanitized_prompt,
                "arc_tracing.agent.prompt_source": prompt_source,
                "arc_tracing.agent.prompt_extraction_method": "api_interception",
            })
        
        # Add error information if present
        if call_data.get("error"):
            arc_trace["error"] = call_data["error"]
            arc_trace["attributes"]["arc_tracing.error"] = call_data["error"]
        
        return arc_trace