"""Environment variable handling for proxy configuration."""

import os
import logging
from typing import Dict, Optional

# Configure logger
logger = logging.getLogger("arc_tracing")

# Original environment variables storage
_original_env_vars: Dict[str, Optional[str]] = {}

def setup_proxy_environment(proxy_url: Optional[str] = None) -> None:
    """
    Configure environment variables to use the Arc Tracing proxy.
    
    This function modifies environment variables to redirect API calls
    to the tracing proxy server. This allows tracing without modifying
    code that uses LLM APIs directly.
    
    Args:
        proxy_url: The base URL of the proxy server.
            If None, will use "http://localhost:8000"
    """
    if proxy_url is None:
        proxy_url = "http://localhost:8000"
    
    # Store original environment variables
    _store_original_env_vars()
    
    # Set up OpenAI proxy
    os.environ["OPENAI_API_BASE"] = f"{proxy_url}/v1"
    logger.info(f"Set OPENAI_API_BASE to {proxy_url}/v1")
    
    # Set up Anthropic proxy
    os.environ["ANTHROPIC_API_URL"] = f"{proxy_url}/anthropic"
    logger.info(f"Set ANTHROPIC_API_URL to {proxy_url}/anthropic")
    
    # Add other providers as needed

def _store_original_env_vars() -> None:
    """Store original environment variables for later restoration."""
    global _original_env_vars
    
    # OpenAI
    _original_env_vars["OPENAI_API_BASE"] = os.environ.get("OPENAI_API_BASE")
    
    # Anthropic
    _original_env_vars["ANTHROPIC_API_URL"] = os.environ.get("ANTHROPIC_API_URL")
    
    # Add other providers as needed

def restore_original_environment() -> None:
    """Restore original environment variables."""
    global _original_env_vars
    
    # Restore OpenAI
    if "OPENAI_API_BASE" in _original_env_vars:
        if _original_env_vars["OPENAI_API_BASE"] is None:
            if "OPENAI_API_BASE" in os.environ:
                del os.environ["OPENAI_API_BASE"]
        else:
            os.environ["OPENAI_API_BASE"] = _original_env_vars["OPENAI_API_BASE"]
    
    # Restore Anthropic
    if "ANTHROPIC_API_URL" in _original_env_vars:
        if _original_env_vars["ANTHROPIC_API_URL"] is None:
            if "ANTHROPIC_API_URL" in os.environ:
                del os.environ["ANTHROPIC_API_URL"]
        else:
            os.environ["ANTHROPIC_API_URL"] = _original_env_vars["ANTHROPIC_API_URL"]
    
    # Add other providers as needed
    
    logger.info("Restored original environment variables")