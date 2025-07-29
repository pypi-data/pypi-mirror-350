"""OpenAI API interceptor for universal framework coverage."""

import logging
from typing import Any, Dict, Optional, Tuple
from arc_tracing.interceptors.base import BaseInterceptor

logger = logging.getLogger("arc_tracing")

class OpenAIInterceptor(BaseInterceptor):
    """
    Interceptor for OpenAI API calls.
    
    This interceptor captures OpenAI API calls regardless of which framework
    is making them (LangChain, LlamaIndex, direct calls, etc.).
    """
    
    def __init__(self):
        super().__init__("openai")
    
    def is_available(self) -> bool:
        """Check if OpenAI client is available."""
        try:
            import openai
            return True
        except ImportError:
            return False
    
    def _setup_interception(self) -> bool:
        """Set up OpenAI API call interception."""
        try:
            import openai
            
            # Intercept the main completion methods
            if hasattr(openai, 'ChatCompletion') and hasattr(openai.ChatCompletion, 'create'):
                # OpenAI v0.x
                self._patch_method(openai.ChatCompletion, 'create', 'chat_completions_create')
                
            if hasattr(openai, 'Completion') and hasattr(openai.Completion, 'create'):
                # OpenAI v0.x
                self._patch_method(openai.Completion, 'create', 'completions_create')
            
            # OpenAI v1.x client-based API
            try:
                from openai import OpenAI
                # Patch the default client's methods
                client = OpenAI()
                if hasattr(client, 'chat') and hasattr(client.chat, 'completions'):
                    self._patch_method(client.chat.completions, 'create', 'chat_completions_create')
                if hasattr(client, 'completions'):
                    self._patch_method(client.completions, 'create', 'completions_create')
                    
                # Also patch the client class constructor to catch new instances
                original_init = OpenAI.__init__
                def traced_init(instance, *args, **kwargs):
                    result = original_init(instance, *args, **kwargs)
                    # Patch methods on new client instances
                    if hasattr(instance, 'chat') and hasattr(instance.chat, 'completions'):
                        self._patch_method(instance.chat.completions, 'create', 'chat_completions_create')
                    if hasattr(instance, 'completions'):
                        self._patch_method(instance.completions, 'create', 'completions_create')
                    return result
                
                OpenAI.__init__ = traced_init
                self._original_methods['OpenAI.__init__'] = original_init
                
            except ImportError:
                pass  # v1.x not available
            
            logger.info("Successfully set up OpenAI API interception")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup OpenAI API interception: {e}")
            return False
    
    def _patch_method(self, obj: Any, method_name: str, trace_name: str) -> None:
        """Patch a specific method with tracing."""
        if hasattr(obj, method_name):
            original_method = getattr(obj, method_name)
            traced_method = self._create_traced_method(original_method, trace_name)
            setattr(obj, method_name, traced_method)
            self._original_methods[f"{obj.__class__.__name__}.{method_name}"] = original_method
    
    def _teardown_interception(self) -> None:
        """Clean up OpenAI API interception."""
        try:
            # Restore original methods
            for method_path, original_method in self._original_methods.items():
                if '.' in method_path:
                    class_name, method_name = method_path.rsplit('.', 1)
                    if class_name == 'OpenAI' and method_name == '__init__':
                        import openai
                        openai.OpenAI.__init__ = original_method
                # Note: For object instances, we can't easily restore without references
                # This is acceptable for development/testing scenarios
            
            self._original_methods.clear()
            
        except Exception as e:
            logger.error(f"Error during OpenAI API interception teardown: {e}")
    
    def extract_system_prompt(self, call_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
        """
        Extract system prompt from OpenAI API call data.
        
        Args:
            call_data: OpenAI API call data
            
        Returns:
            Tuple of (prompt_text, template_variables, prompt_source) or None if no prompt found
        """
        try:
            prompt_text = None
            template_vars = None
            
            # Extract from kwargs (most common case)
            kwargs = call_data.get("kwargs", {})
            
            # Method 1: Extract from messages array (Chat Completions)
            messages = kwargs.get("messages", [])
            if messages and isinstance(messages, list):
                for message in messages:
                    if isinstance(message, dict) and message.get("role") == "system":
                        prompt_text = message.get("content")
                        break
            
            # Method 2: Extract from prompt parameter (Legacy Completions)
            if not prompt_text:
                prompt = kwargs.get("prompt")
                if isinstance(prompt, str):
                    # Check if this looks like a system prompt
                    # Simple heuristic: contains instruction-like language
                    instruction_indicators = [
                        "you are", "act as", "your role", "instructions:",
                        "system:", "assistant:", "respond as", "behave as"
                    ]
                    if any(indicator in prompt.lower() for indicator in instruction_indicators):
                        prompt_text = prompt
            
            # Method 3: Extract from function calling context
            if not prompt_text and "functions" in kwargs:
                # Sometimes system prompts are embedded in function calling setup
                functions = kwargs.get("functions", [])
                if functions and isinstance(functions, list):
                    # Look for system-level function descriptions
                    for func in functions:
                        if isinstance(func, dict):
                            description = func.get("description", "")
                            if description and len(description) > 50:  # Substantial description
                                prompt_text = f"Function-calling assistant with tools: {description}"
                                break
            
            # Method 4: Extract from additional parameters
            if not prompt_text:
                # Check for custom system-related parameters
                system_fields = ["system_message", "system_prompt", "instructions"]
                for field in system_fields:
                    if field in kwargs:
                        value = kwargs[field]
                        if isinstance(value, str) and value.strip():
                            prompt_text = value.strip()
                            break
            
            # Method 5: Extract from response (for validation)
            response_data = call_data.get("response_data", {})
            if not prompt_text and isinstance(response_data, dict):
                # Sometimes the prompt is echoed back in debug info
                usage_data = response_data.get("usage", {})
                if usage_data and "prompt_tokens" in usage_data:
                    # If we have significant prompt tokens but no extracted prompt,
                    # flag this for manual review
                    prompt_tokens = usage_data.get("prompt_tokens", 0)
                    if prompt_tokens > 50:  # Substantial prompt
                        prompt_text = "[SYSTEM_PROMPT_DETECTED_BUT_NOT_EXTRACTED]"
            
            if prompt_text and isinstance(prompt_text, str) and prompt_text.strip():
                return (prompt_text.strip(), template_vars, "openai_api")
                
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting system prompt from OpenAI API call: {e}")
            return None
    
    def _extract_response_data(self, result: Any) -> Dict[str, Any]:
        """Extract data from OpenAI API response."""
        response_data = {"response_type": type(result).__name__}
        
        try:
            # Handle different response formats
            if hasattr(result, 'model_dump'):
                # Pydantic v2 (OpenAI v1.x)
                data = result.model_dump()
            elif hasattr(result, 'dict'):
                # Pydantic v1 or dict-like
                data = result.dict() if callable(result.dict) else result
            elif isinstance(result, dict):
                data = result
            else:
                return response_data
            
            # Extract useful information
            if "usage" in data:
                response_data["usage"] = data["usage"]
            if "model" in data:
                response_data["model"] = data["model"]
            if "choices" in data and data["choices"]:
                first_choice = data["choices"][0]
                if "message" in first_choice:
                    message = first_choice["message"]
                    response_data["response_role"] = message.get("role")
                    content = message.get("content", "")
                    # Truncate long responses
                    if len(content) > 1000:
                        response_data["response_content"] = content[:1000] + "...[TRUNCATED]"
                    else:
                        response_data["response_content"] = content
                elif "text" in first_choice:
                    text = first_choice["text"]
                    if len(text) > 1000:
                        response_data["response_content"] = text[:1000] + "...[TRUNCATED]"
                    else:
                        response_data["response_content"] = text
                        
        except Exception as e:
            logger.warning(f"Error extracting OpenAI response data: {e}")
        
        return response_data
    
    def _sanitize_kwargs(self, kwargs: dict) -> Dict[str, Any]:
        """Sanitize OpenAI-specific keyword arguments."""
        sanitized = {}
        
        for key, value in kwargs.items():
            if key == "messages" and isinstance(value, list):
                # Sanitize messages array
                sanitized_messages = []
                for msg in value:
                    if isinstance(msg, dict):
                        sanitized_msg = {"role": msg.get("role")}
                        content = msg.get("content", "")
                        if isinstance(content, str) and len(content) > 500:
                            sanitized_msg["content"] = content[:500] + "...[TRUNCATED]"
                        else:
                            sanitized_msg["content"] = content
                        sanitized_messages.append(sanitized_msg)
                sanitized[key] = sanitized_messages
            elif key in ["api_key", "organization"]:
                # Mask sensitive data
                sanitized[key] = "[MASKED]"
            else:
                sanitized[key] = self._sanitize_value(value)
        
        return sanitized