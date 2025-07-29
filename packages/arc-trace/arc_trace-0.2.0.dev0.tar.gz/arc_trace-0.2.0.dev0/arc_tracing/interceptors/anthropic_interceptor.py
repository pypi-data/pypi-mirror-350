"""Anthropic API interceptor for universal framework coverage."""

import logging
from typing import Any, Dict, Optional, Tuple
from arc_tracing.interceptors.base import BaseInterceptor

logger = logging.getLogger("arc_tracing")

class AnthropicInterceptor(BaseInterceptor):
    """
    Interceptor for Anthropic API calls.
    
    This interceptor captures Anthropic API calls regardless of which framework
    is making them (LangChain, LlamaIndex, direct calls, etc.).
    """
    
    def __init__(self):
        super().__init__("anthropic")
    
    def is_available(self) -> bool:
        """Check if Anthropic client is available."""
        try:
            import anthropic
            return True
        except ImportError:
            return False
    
    def _setup_interception(self) -> bool:
        """Set up Anthropic API call interception."""
        try:
            import anthropic
            
            # Patch the main Anthropic client
            if hasattr(anthropic, 'Anthropic'):
                # Patch client methods
                original_init = anthropic.Anthropic.__init__
                def traced_init(instance, *args, **kwargs):
                    result = original_init(instance, *args, **kwargs)
                    # Patch methods on client instances
                    if hasattr(instance, 'messages') and hasattr(instance.messages, 'create'):
                        self._patch_method(instance.messages, 'create', 'messages_create')
                    if hasattr(instance, 'completions') and hasattr(instance.completions, 'create'):
                        self._patch_method(instance.completions, 'create', 'completions_create')
                    return result
                
                anthropic.Anthropic.__init__ = traced_init
                self._original_methods['Anthropic.__init__'] = original_init
                
                # Also patch any existing default client instances
                try:
                    client = anthropic.Anthropic()
                    if hasattr(client, 'messages') and hasattr(client.messages, 'create'):
                        self._patch_method(client.messages, 'create', 'messages_create')
                    if hasattr(client, 'completions') and hasattr(client.completions, 'create'):
                        self._patch_method(client.completions, 'create', 'completions_create')
                except Exception:
                    pass  # Client creation might fail without API key
            
            # Also try to patch legacy module-level functions
            if hasattr(anthropic, 'completions') and hasattr(anthropic.completions, 'create'):
                self._patch_method(anthropic.completions, 'create', 'completions_create')
            
            logger.info("Successfully set up Anthropic API interception")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup Anthropic API interception: {e}")
            return False
    
    def _patch_method(self, obj: Any, method_name: str, trace_name: str) -> None:
        """Patch a specific method with tracing."""
        if hasattr(obj, method_name):
            original_method = getattr(obj, method_name)
            traced_method = self._create_traced_method(original_method, trace_name)
            setattr(obj, method_name, traced_method)
            self._original_methods[f"{obj.__class__.__name__}.{method_name}"] = original_method
    
    def _teardown_interception(self) -> None:
        """Clean up Anthropic API interception."""
        try:
            # Restore original methods
            for method_path, original_method in self._original_methods.items():
                if '.' in method_path:
                    class_name, method_name = method_path.rsplit('.', 1)
                    if class_name == 'Anthropic' and method_name == '__init__':
                        import anthropic
                        anthropic.Anthropic.__init__ = original_method
            
            self._original_methods.clear()
            
        except Exception as e:
            logger.error(f"Error during Anthropic API interception teardown: {e}")
    
    def extract_system_prompt(self, call_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
        """
        Extract system prompt from Anthropic API call data.
        
        Args:
            call_data: Anthropic API call data
            
        Returns:
            Tuple of (prompt_text, template_variables, prompt_source) or None if no prompt found
        """
        try:
            prompt_text = None
            template_vars = None
            
            # Extract from kwargs
            kwargs = call_data.get("kwargs", {})
            
            # Method 1: Extract from messages array (Messages API)
            messages = kwargs.get("messages", [])
            if messages and isinstance(messages, list):
                for message in messages:
                    if isinstance(message, dict) and message.get("role") == "system":
                        prompt_text = message.get("content")
                        break
            
            # Method 2: Extract from system parameter (Messages API)
            if not prompt_text:
                system = kwargs.get("system")
                if isinstance(system, str) and system.strip():
                    prompt_text = system.strip()
            
            # Method 3: Extract from prompt parameter (Legacy Completions API)
            if not prompt_text:
                prompt = kwargs.get("prompt")
                if isinstance(prompt, str):
                    # Check if this looks like a system prompt
                    # Anthropic often uses specific formats
                    if "Human:" in prompt and "Assistant:" in prompt:
                        # Extract the part before the first "Human:" as system context
                        human_index = prompt.find("Human:")
                        if human_index > 0:
                            potential_system = prompt[:human_index].strip()
                            if potential_system:
                                prompt_text = potential_system
                    else:
                        # Simple heuristic for instruction-like content
                        instruction_indicators = [
                            "you are", "act as", "your role", "instructions:",
                            "system:", "respond as", "behave as", "you should"
                        ]
                        if any(indicator in prompt.lower() for indicator in instruction_indicators):
                            prompt_text = prompt
            
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
            
            # Method 5: Extract from tool/function context
            if not prompt_text and "tools" in kwargs:
                tools = kwargs.get("tools", [])
                if tools and isinstance(tools, list):
                    # Sometimes system prompts are embedded in tool usage context
                    tool_descriptions = []
                    for tool in tools:
                        if isinstance(tool, dict):
                            description = tool.get("description", "")
                            if description:
                                tool_descriptions.append(description)
                    
                    if tool_descriptions:
                        prompt_text = f"Assistant with access to tools: {', '.join(tool_descriptions[:3])}"
                        if len(tool_descriptions) > 3:
                            prompt_text += f" (and {len(tool_descriptions) - 3} more)"
            
            if prompt_text and isinstance(prompt_text, str) and prompt_text.strip():
                return (prompt_text.strip(), template_vars, "anthropic_api")
                
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting system prompt from Anthropic API call: {e}")
            return None
    
    def _extract_response_data(self, result: Any) -> Dict[str, Any]:
        """Extract data from Anthropic API response."""
        response_data = {"response_type": type(result).__name__}
        
        try:
            # Handle different response formats
            if hasattr(result, 'model_dump'):
                # Pydantic v2
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
            
            # Extract content from response
            content = None
            if "content" in data:
                if isinstance(data["content"], list) and data["content"]:
                    # Messages API response
                    first_content = data["content"][0]
                    if isinstance(first_content, dict) and "text" in first_content:
                        content = first_content["text"]
                elif isinstance(data["content"], str):
                    content = data["content"]
            elif "completion" in data:
                # Legacy completions API
                content = data["completion"]
            
            if content:
                # Truncate long responses
                if len(content) > 1000:
                    response_data["response_content"] = content[:1000] + "...[TRUNCATED]"
                else:
                    response_data["response_content"] = content
                    
        except Exception as e:
            logger.warning(f"Error extracting Anthropic response data: {e}")
        
        return response_data
    
    def _sanitize_kwargs(self, kwargs: dict) -> Dict[str, Any]:
        """Sanitize Anthropic-specific keyword arguments."""
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
            elif key in ["api_key", "auth_token"]:
                # Mask sensitive data
                sanitized[key] = "[MASKED]"
            elif key == "system" and isinstance(value, str) and len(value) > 500:
                # Truncate long system prompts for logging
                sanitized[key] = value[:500] + "...[TRUNCATED]"
            else:
                sanitized[key] = self._sanitize_value(value)
        
        return sanitized