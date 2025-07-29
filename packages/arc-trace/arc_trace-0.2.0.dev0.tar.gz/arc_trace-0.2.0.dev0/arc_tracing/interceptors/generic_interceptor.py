"""Generic HTTP interceptor for catching other API providers."""

import logging
from typing import Any, Dict, Optional, Tuple
from arc_tracing.interceptors.base import BaseInterceptor

logger = logging.getLogger("arc_tracing")

class GenericInterceptor(BaseInterceptor):
    """
    Generic interceptor for HTTP requests to AI service providers.
    
    This interceptor can capture requests to other AI APIs that don't have
    specific interceptors, providing universal coverage for any HTTP-based
    AI service.
    """
    
    def __init__(self):
        super().__init__("generic_http")
    
    def is_available(self) -> bool:
        """Check if HTTP libraries are available for interception."""
        try:
            import requests
            return True
        except ImportError:
            try:
                import httpx
                return True
            except ImportError:
                return False
    
    def _setup_interception(self) -> bool:
        """Set up generic HTTP interception for AI APIs."""
        try:
            success = False
            
            # Try to patch requests library
            try:
                import requests
                self._patch_requests()
                success = True
            except ImportError:
                pass
            
            # Try to patch httpx library
            try:
                import httpx
                self._patch_httpx()
                success = True
            except ImportError:
                pass
            
            if success:
                logger.info("Successfully set up generic HTTP API interception")
            else:
                logger.warning("No HTTP libraries available for generic interception")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to setup generic HTTP interception: {e}")
            return False
    
    def _patch_requests(self) -> None:
        """Patch requests library for AI API detection."""
        import requests
        
        original_post = requests.post
        original_request = requests.request
        
        def traced_post(*args, **kwargs):
            if self._is_ai_api_call(args, kwargs):
                call_data = self._extract_call_data("requests.post", args, kwargs)
                try:
                    result = original_post(*args, **kwargs)
                    call_data.update(self._extract_response_data(result))
                    call_data["status"] = "success"
                    self._send_trace_to_arc(call_data)
                    return result
                except Exception as e:
                    call_data["status"] = "error"
                    call_data["error"] = str(e)
                    self._send_trace_to_arc(call_data)
                    raise
            else:
                return original_post(*args, **kwargs)
        
        def traced_request(*args, **kwargs):
            if self._is_ai_api_call(args, kwargs):
                call_data = self._extract_call_data("requests.request", args, kwargs)
                try:
                    result = original_request(*args, **kwargs)
                    call_data.update(self._extract_response_data(result))
                    call_data["status"] = "success"
                    self._send_trace_to_arc(call_data)
                    return result
                except Exception as e:
                    call_data["status"] = "error"
                    call_data["error"] = str(e)
                    self._send_trace_to_arc(call_data)
                    raise
            else:
                return original_request(*args, **kwargs)
        
        requests.post = traced_post
        requests.request = traced_request
        
        self._original_methods['requests.post'] = original_post
        self._original_methods['requests.request'] = original_request
    
    def _patch_httpx(self) -> None:
        """Patch httpx library for AI API detection."""
        import httpx
        
        # Patch Client.post and Client.request methods
        original_client_post = httpx.Client.post
        original_client_request = httpx.Client.request
        
        def traced_client_post(self, *args, **kwargs):
            if self._is_ai_api_call(args, kwargs):
                call_data = self._extract_call_data("httpx.Client.post", args, kwargs)
                try:
                    result = original_client_post(self, *args, **kwargs)
                    call_data.update(self._extract_response_data(result))
                    call_data["status"] = "success"
                    # Use the interceptor instance, not the httpx client
                    if hasattr(self, '_arc_interceptor'):
                        self._arc_interceptor._send_trace_to_arc(call_data)
                    return result
                except Exception as e:
                    call_data["status"] = "error"
                    call_data["error"] = str(e)
                    if hasattr(self, '_arc_interceptor'):
                        self._arc_interceptor._send_trace_to_arc(call_data)
                    raise
            else:
                return original_client_post(self, *args, **kwargs)
        
        def traced_client_request(self, *args, **kwargs):
            if self._is_ai_api_call(args, kwargs):
                call_data = self._extract_call_data("httpx.Client.request", args, kwargs)
                try:
                    result = original_client_request(self, *args, **kwargs)
                    call_data.update(self._extract_response_data(result))
                    call_data["status"] = "success"
                    if hasattr(self, '_arc_interceptor'):
                        self._arc_interceptor._send_trace_to_arc(call_data)
                    return result
                except Exception as e:
                    call_data["status"] = "error"
                    call_data["error"] = str(e)
                    if hasattr(self, '_arc_interceptor'):
                        self._arc_interceptor._send_trace_to_arc(call_data)
                    raise
            else:
                return original_client_request(self, *args, **kwargs)
        
        # Patch the constructor to add interceptor reference
        original_init = httpx.Client.__init__
        def traced_init(instance, *args, **kwargs):
            result = original_init(instance, *args, **kwargs)
            instance._arc_interceptor = self  # Reference to this interceptor
            return result
        
        httpx.Client.post = traced_client_post
        httpx.Client.request = traced_client_request
        httpx.Client.__init__ = traced_init
        
        self._original_methods['httpx.Client.post'] = original_client_post
        self._original_methods['httpx.Client.request'] = original_client_request
        self._original_methods['httpx.Client.__init__'] = original_init
    
    def _is_ai_api_call(self, args: tuple, kwargs: dict) -> bool:
        """
        Determine if this HTTP call is to an AI service API.
        
        Args:
            args: Request positional arguments
            kwargs: Request keyword arguments
            
        Returns:
            True if this appears to be an AI API call
        """
        # Get URL from args or kwargs
        url = None
        if args:
            url = args[0] if len(args) > 0 else None
        if not url:
            url = kwargs.get('url')
        
        if not url or not isinstance(url, str):
            return False
        
        # List of known AI service domains
        ai_domains = [
            'api.openai.com',
            'api.anthropic.com',
            'api.cohere.ai',
            'api.ai21.com',
            'api.huggingface.co',
            'api.together.xyz',
            'api.replicate.com',
            'api.fireworks.ai',
            'api.groq.com',
            'api.mistral.ai',
            'generativelanguage.googleapis.com',  # Google AI
            'api.perplexity.ai',
            'api.voyageai.com',
            'api.deepseek.com',
            'api.moonshot.cn',
            'api.zhipuai.cn',
        ]
        
        # Check if URL contains any AI service domains
        url_lower = url.lower()
        for domain in ai_domains:
            if domain in url_lower:
                return True
        
        # Additional heuristics for AI API calls
        # Check for common AI API endpoints
        ai_endpoints = [
            '/chat/completions',
            '/completions',
            '/messages',
            '/generate',
            '/embeddings',
            '/v1/chat',
            '/v1/completions',
            '/v1/models',
        ]
        
        for endpoint in ai_endpoints:
            if endpoint in url_lower:
                return True
        
        # Check request body for AI-specific content
        json_data = kwargs.get('json') or kwargs.get('data')
        if isinstance(json_data, dict):
            # Look for common AI API parameters
            ai_params = ['messages', 'prompt', 'model', 'max_tokens', 'temperature']
            if any(param in json_data for param in ai_params):
                return True
        
        return False
    
    def _teardown_interception(self) -> None:
        """Clean up generic HTTP interception."""
        try:
            # Restore original methods
            for method_path, original_method in self._original_methods.items():
                if method_path == 'requests.post':
                    import requests
                    requests.post = original_method
                elif method_path == 'requests.request':
                    import requests
                    requests.request = original_method
                elif method_path == 'httpx.Client.post':
                    import httpx
                    httpx.Client.post = original_method
                elif method_path == 'httpx.Client.request':
                    import httpx
                    httpx.Client.request = original_method
                elif method_path == 'httpx.Client.__init__':
                    import httpx
                    httpx.Client.__init__ = original_method
            
            self._original_methods.clear()
            
        except Exception as e:
            logger.error(f"Error during generic HTTP interception teardown: {e}")
    
    def extract_system_prompt(self, call_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
        """
        Extract system prompt from generic HTTP API call data.
        
        Args:
            call_data: HTTP API call data
            
        Returns:
            Tuple of (prompt_text, template_variables, prompt_source) or None if no prompt found
        """
        try:
            prompt_text = None
            template_vars = None
            
            # Extract from request data
            kwargs = call_data.get("kwargs", {})
            
            # Method 1: Extract from JSON request body
            json_data = kwargs.get('json')
            if isinstance(json_data, dict):
                # Check for messages array (common in chat APIs)
                messages = json_data.get("messages", [])
                if messages and isinstance(messages, list):
                    for message in messages:
                        if isinstance(message, dict) and message.get("role") == "system":
                            prompt_text = message.get("content")
                            break
                
                # Check for direct system prompt fields
                if not prompt_text:
                    system_fields = [
                        "system", "system_prompt", "system_message", 
                        "instructions", "context", "persona"
                    ]
                    for field in system_fields:
                        if field in json_data:
                            value = json_data[field]
                            if isinstance(value, str) and value.strip():
                                prompt_text = value.strip()
                                break
                
                # Check for prompt field with system context
                if not prompt_text:
                    prompt = json_data.get("prompt")
                    if isinstance(prompt, str):
                        # Use heuristics to identify system prompts
                        instruction_indicators = [
                            "you are", "act as", "your role", "instructions:",
                            "system:", "respond as", "behave as"
                        ]
                        if any(indicator in prompt.lower() for indicator in instruction_indicators):
                            prompt_text = prompt
            
            # Method 2: Extract from form data
            if not prompt_text:
                data = kwargs.get('data')
                if isinstance(data, dict):
                    for field in ["system_prompt", "instructions", "context"]:
                        if field in data:
                            value = data[field]
                            if isinstance(value, str) and value.strip():
                                prompt_text = value.strip()
                                break
            
            # Determine the source based on the URL
            url = kwargs.get('url', '')
            if 'openai.com' in url:
                source = "openai_api_generic"
            elif 'anthropic.com' in url:
                source = "anthropic_api_generic"
            elif 'cohere.ai' in url:
                source = "cohere_api"
            elif 'huggingface.co' in url:
                source = "huggingface_api"
            else:
                source = "generic_ai_api"
            
            if prompt_text and isinstance(prompt_text, str) and prompt_text.strip():
                return (prompt_text.strip(), template_vars, source)
                
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting system prompt from generic API call: {e}")
            return None
    
    def _extract_response_data(self, result: Any) -> Dict[str, Any]:
        """Extract data from generic HTTP response."""
        response_data = {"response_type": type(result).__name__}
        
        try:
            # Handle requests.Response
            if hasattr(result, 'json') and callable(result.json):
                try:
                    json_data = result.json()
                    if isinstance(json_data, dict):
                        # Extract common AI API response fields
                        if "usage" in json_data:
                            response_data["usage"] = json_data["usage"]
                        if "model" in json_data:
                            response_data["model"] = json_data["model"]
                        
                        # Extract content from various response formats
                        content = None
                        if "choices" in json_data and json_data["choices"]:
                            first_choice = json_data["choices"][0]
                            if "message" in first_choice:
                                content = first_choice["message"].get("content")
                            elif "text" in first_choice:
                                content = first_choice["text"]
                        elif "content" in json_data:
                            content = json_data["content"]
                        elif "text" in json_data:
                            content = json_data["text"]
                        
                        if content and isinstance(content, str):
                            if len(content) > 1000:
                                response_data["response_content"] = content[:1000] + "...[TRUNCATED]"
                            else:
                                response_data["response_content"] = content
                except Exception:
                    pass  # JSON parsing failed
            
            # Add status code if available
            if hasattr(result, 'status_code'):
                response_data["status_code"] = result.status_code
                
        except Exception as e:
            logger.warning(f"Error extracting generic HTTP response data: {e}")
        
        return response_data