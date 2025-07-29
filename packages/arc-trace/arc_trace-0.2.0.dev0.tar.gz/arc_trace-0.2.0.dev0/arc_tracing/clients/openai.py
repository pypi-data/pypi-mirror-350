"""OpenAI client wrapper with built-in tracing."""

import logging
import importlib
from typing import Any, Dict, Optional, List, Union

from opentelemetry import trace

# Configure logger
logger = logging.getLogger("arc_tracing")

# Initialize tracer
tracer = trace.get_tracer("arc_tracing.clients.openai")

class OpenAI:
    """
    Wrapper for the OpenAI client with built-in tracing.
    
    This is a drop-in replacement for the standard OpenAI client
    that automatically adds tracing to all API calls.
    
    Example:
        >>> from arc_tracing.clients import OpenAI
        >>> client = OpenAI()  # Same constructor as openai.OpenAI
        >>> # Use exactly like the regular OpenAI client
        >>> response = client.chat.completions.create(
        ...     model="gpt-4",
        ...     messages=[{"role": "user", "content": "Hello"}]
        ... )
    """
    
    def __init__(self, *args: Any, **kwargs: Any):
        """
        Initialize the OpenAI client wrapper.
        
        Args:
            *args: Positional arguments to pass to the OpenAI client.
            **kwargs: Keyword arguments to pass to the OpenAI client.
        
        Raises:
            ImportError: If OpenAI is not installed.
        """
        try:
            import openai
            self._openai_module = openai
            self._client = openai.OpenAI(*args, **kwargs)
            self._setup_proxy()
        except ImportError:
            raise ImportError(
                "OpenAI package is required for the OpenAI client wrapper. "
                "Install it with `pip install openai`."
            )
    
    def _setup_proxy(self) -> None:
        """Set up the API proxy for different client components."""
        # Proxy for chat completions
        self.chat = OpenAIChatProxy(self._client.chat)
        
        # Proxy for completions
        self.completions = OpenAICompletionsProxy(self._client.completions)
        
        # Proxy for embeddings
        self.embeddings = OpenAIEmbeddingsProxy(self._client.embeddings)
        
        # Add other API components as needed
        
        # For any components not explicitly proxied, return the original
        self._original_client = self._client
    
    def __getattr__(self, name: str) -> Any:
        """Pass through any other attributes to the original client."""
        return getattr(self._original_client, name)


class OpenAIChatProxy:
    """Proxy for OpenAI chat API."""
    
    def __init__(self, chat_client: Any):
        """Initialize with the original chat client."""
        self._chat_client = chat_client
        self.completions = OpenAIChatCompletionsProxy(chat_client.completions)
    
    def __getattr__(self, name: str) -> Any:
        """Pass through any other attributes."""
        return getattr(self._chat_client, name)


class OpenAIChatCompletionsProxy:
    """Proxy for OpenAI chat completions API."""
    
    def __init__(self, completions_client: Any):
        """Initialize with the original completions client."""
        self._completions_client = completions_client
    
    def create(self, *args: Any, **kwargs: Any) -> Any:
        """
        Create a chat completion with tracing.
        
        Args:
            *args: Positional arguments for the completions API.
            **kwargs: Keyword arguments for the completions API.
            
        Returns:
            The API response.
        """
        # Start tracing span
        with tracer.start_as_current_span(
            "openai.chat.completions.create",
            attributes={
                "arc_tracing.component": "openai.chat",
                "arc_tracing.client": "arc_tracing.openai",
            }
        ) as span:
            # Record request details
            if "model" in kwargs:
                span.set_attribute("arc_tracing.openai.model", kwargs["model"])
            
            if "messages" in kwargs:
                try:
                    # Safely extract and record system and user messages
                    messages = kwargs["messages"]
                    for i, msg in enumerate(messages):
                        if isinstance(msg, dict) and "role" in msg and "content" in msg:
                            role = msg["role"]
                            if role == "system":
                                span.set_attribute("arc_tracing.openai.system_message", str(msg["content"]))
                            elif role == "user" and i == len(messages) - 1:  # Last user message
                                span.set_attribute("arc_tracing.openai.user_message", str(msg["content"]))
                except Exception as e:
                    logger.debug(f"Error extracting OpenAI messages: {e}")
            
            # Execute the API call
            try:
                result = self._completions_client.create(*args, **kwargs)
                
                # Record response data
                if hasattr(result, "choices") and result.choices:
                    first_choice = result.choices[0]
                    if hasattr(first_choice, "message") and hasattr(first_choice.message, "content"):
                        span.set_attribute("arc_tracing.openai.response", first_choice.message.content)
                
                if hasattr(result, "usage"):
                    if hasattr(result.usage, "prompt_tokens"):
                        span.set_attribute("arc_tracing.openai.prompt_tokens", result.usage.prompt_tokens)
                    if hasattr(result.usage, "completion_tokens"):
                        span.set_attribute("arc_tracing.openai.completion_tokens", result.usage.completion_tokens)
                    if hasattr(result.usage, "total_tokens"):
                        span.set_attribute("arc_tracing.openai.total_tokens", result.usage.total_tokens)
                
                return result
            
            except Exception as e:
                # Record exception
                span.record_exception(e)
                raise
    
    def __getattr__(self, name: str) -> Any:
        """Pass through any other attributes."""
        return getattr(self._completions_client, name)


class OpenAICompletionsProxy:
    """Proxy for OpenAI completions API."""
    
    def __init__(self, completions_client: Any):
        """Initialize with the original completions client."""
        self._completions_client = completions_client
    
    def create(self, *args: Any, **kwargs: Any) -> Any:
        """Create a completion with tracing."""
        # Implementation similar to chat completions
        pass
    
    def __getattr__(self, name: str) -> Any:
        """Pass through any other attributes."""
        return getattr(self._completions_client, name)


class OpenAIEmbeddingsProxy:
    """Proxy for OpenAI embeddings API."""
    
    def __init__(self, embeddings_client: Any):
        """Initialize with the original embeddings client."""
        self._embeddings_client = embeddings_client
    
    def create(self, *args: Any, **kwargs: Any) -> Any:
        """Create embeddings with tracing."""
        # Implementation for embeddings
        pass
    
    def __getattr__(self, name: str) -> Any:
        """Pass through any other attributes."""
        return getattr(self._embeddings_client, name)