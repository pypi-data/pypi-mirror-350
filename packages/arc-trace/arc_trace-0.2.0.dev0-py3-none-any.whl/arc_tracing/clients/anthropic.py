"""Anthropic client wrapper with built-in tracing."""

import logging
import importlib
from typing import Any, Dict, Optional, List, Union

from opentelemetry import trace

# Configure logger
logger = logging.getLogger("arc_tracing")

# Initialize tracer
tracer = trace.get_tracer("arc_tracing.clients.anthropic")

class Anthropic:
    """
    Wrapper for the Anthropic client with built-in tracing.
    
    This is a drop-in replacement for the standard Anthropic client
    that automatically adds tracing to all API calls.
    
    Example:
        >>> from arc_tracing.clients import Anthropic
        >>> client = Anthropic(api_key="your-api-key")  # Same constructor as anthropic.Anthropic
        >>> # Use exactly like the regular Anthropic client
        >>> message = client.messages.create(
        ...     model="claude-3-sonnet-20240229",
        ...     messages=[{"role": "user", "content": "Hello"}],
        ...     max_tokens=1000
        ... )
    """
    
    def __init__(self, *args: Any, **kwargs: Any):
        """
        Initialize the Anthropic client wrapper.
        
        Args:
            *args: Positional arguments to pass to the Anthropic client.
            **kwargs: Keyword arguments to pass to the Anthropic client.
        
        Raises:
            ImportError: If Anthropic is not installed.
        """
        try:
            import anthropic
            self._anthropic_module = anthropic
            self._client = anthropic.Anthropic(*args, **kwargs)
            self._setup_proxy()
        except ImportError:
            raise ImportError(
                "Anthropic package is required for the Anthropic client wrapper. "
                "Install it with `pip install anthropic`."
            )
    
    def _setup_proxy(self) -> None:
        """Set up the API proxy for different client components."""
        # Proxy for messages
        self.messages = AnthropicMessagesProxy(self._client.messages)
        
        # For any components not explicitly proxied, return the original
        self._original_client = self._client
    
    def __getattr__(self, name: str) -> Any:
        """Pass through any other attributes to the original client."""
        return getattr(self._original_client, name)


class AnthropicMessagesProxy:
    """Proxy for Anthropic messages API."""
    
    def __init__(self, messages_client: Any):
        """Initialize with the original messages client."""
        self._messages_client = messages_client
    
    def create(self, *args: Any, **kwargs: Any) -> Any:
        """
        Create a message with tracing.
        
        Args:
            *args: Positional arguments for the messages API.
            **kwargs: Keyword arguments for the messages API.
            
        Returns:
            The API response.
        """
        # Start tracing span
        with tracer.start_as_current_span(
            "anthropic.messages.create",
            attributes={
                "arc_tracing.component": "anthropic.messages",
                "arc_tracing.client": "arc_tracing.anthropic",
            }
        ) as span:
            # Record request details
            if "model" in kwargs:
                span.set_attribute("arc_tracing.anthropic.model", kwargs["model"])
            
            if "system" in kwargs:
                span.set_attribute("arc_tracing.anthropic.system", kwargs["system"])
            
            if "messages" in kwargs:
                try:
                    # Extract and record user message
                    messages = kwargs["messages"]
                    for msg in messages:
                        if isinstance(msg, dict) and msg.get("role") == "user":
                            if "content" in msg:
                                content = msg["content"]
                                if isinstance(content, str):
                                    span.set_attribute("arc_tracing.anthropic.user_message", content)
                                elif isinstance(content, list):
                                    # Handle content blocks
                                    for block in content:
                                        if isinstance(block, dict) and block.get("type") == "text":
                                            span.set_attribute("arc_tracing.anthropic.user_message", block.get("text", ""))
                                            break
                except Exception as e:
                    logger.debug(f"Error extracting Anthropic messages: {e}")
            
            # Execute the API call
            try:
                result = self._messages_client.create(*args, **kwargs)
                
                # Record response data
                if hasattr(result, "content") and result.content:
                    for block in result.content:
                        if hasattr(block, "text") and block.text:
                            span.set_attribute("arc_tracing.anthropic.response", block.text)
                            break
                
                if hasattr(result, "usage"):
                    if hasattr(result.usage, "input_tokens"):
                        span.set_attribute("arc_tracing.anthropic.input_tokens", result.usage.input_tokens)
                    if hasattr(result.usage, "output_tokens"):
                        span.set_attribute("arc_tracing.anthropic.output_tokens", result.usage.output_tokens)
                
                return result
            
            except Exception as e:
                # Record exception
                span.record_exception(e)
                raise
    
    def __getattr__(self, name: str) -> Any:
        """Pass through any other attributes."""
        return getattr(self._messages_client, name)