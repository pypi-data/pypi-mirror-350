"""Integration adapters for Arc Tracing SDK.

This module provides lightweight integration adapters that hook into
existing tracing systems rather than monkey patching framework internals.

Each integration leverages the built-in observability systems of modern
frameworks to extend them with Arc platform capabilities.
"""

import logging
from typing import List, Dict, Any

from arc_tracing.integrations.openai_agents import OpenAIAgentsIntegration
from arc_tracing.integrations.langgraph import LangGraphIntegration  
from arc_tracing.integrations.llamaindex import LlamaIndexIntegration
from arc_tracing.integrations.base import BaseIntegration

logger = logging.getLogger("arc_tracing")

# Convenience imports
openai_agents = OpenAIAgentsIntegration()
langgraph = LangGraphIntegration()
llamaindex = LlamaIndexIntegration()

def enable_arc_tracing(frameworks: List[str] = None) -> Dict[str, bool]:
    """
    Enable Arc tracing for all available frameworks or specified frameworks.
    
    This function provides a single entry point to enable Arc tracing across
    all supported AI frameworks. It automatically detects available frameworks
    and sets up lightweight integrations that leverage existing tracing systems.
    
    Args:
        frameworks: Optional list of framework names to enable. If None,
                   auto-detects and enables all available frameworks.
                   Supported: ["openai_agents", "langgraph", "llamaindex"]
    
    Returns:
        Dictionary mapping framework names to integration success status.
        
    Example:
        >>> from arc_tracing import enable_arc_tracing
        >>> 
        >>> # Enable all available frameworks
        >>> results = enable_arc_tracing()
        >>> print(results)  # {"openai_agents": True, "langgraph": False, ...}
        >>> 
        >>> # Enable specific frameworks
        >>> results = enable_arc_tracing(["openai_agents", "langgraph"])
    """
    # All available integrations
    all_integrations = {
        "openai_agents": openai_agents,
        "langgraph": langgraph, 
        "llamaindex": llamaindex,
    }
    
    # Determine which frameworks to enable
    if frameworks is None:
        # Auto-detect all available frameworks
        target_integrations = all_integrations
        logger.info("Auto-detecting and enabling all available AI framework integrations")
    else:
        # Enable only specified frameworks
        target_integrations = {
            name: integration for name, integration in all_integrations.items()
            if name in frameworks
        }
        logger.info(f"Enabling specified framework integrations: {frameworks}")
    
    # Enable each integration
    results = {}
    enabled_count = 0
    
    for name, integration in target_integrations.items():
        try:
            success = integration.enable()
            results[name] = success
            
            if success:
                enabled_count += 1
                logger.info(f"✓ {name} integration enabled")
            else:
                logger.debug(f"✗ {name} integration failed (framework not available)")
                
        except Exception as e:
            results[name] = False
            logger.error(f"✗ {name} integration error: {e}")
    
    # Summary logging
    total_requested = len(target_integrations)
    if enabled_count > 0:
        logger.info(f"Arc tracing enabled for {enabled_count}/{total_requested} frameworks")
    else:
        logger.warning("No framework integrations were enabled. Ensure target frameworks are installed.")
    
    return results

def disable_arc_tracing() -> None:
    """
    Disable all Arc tracing integrations.
    
    This function cleanly disables all active Arc tracing integrations
    and restores original framework behavior.
    """
    integrations = [openai_agents, langgraph, llamaindex]
    
    for integration in integrations:
        if integration.enabled:
            try:
                integration.disable()
                logger.info(f"Disabled {integration.name} integration")
            except Exception as e:
                logger.error(f"Error disabling {integration.name} integration: {e}")

def get_integration_status() -> Dict[str, Dict[str, Any]]:
    """
    Get the status of all Arc tracing integrations.
    
    Returns:
        Dictionary with integration status information.
    """
    integrations = {
        "openai_agents": openai_agents,
        "langgraph": langgraph,
        "llamaindex": llamaindex,
    }
    
    status = {}
    for name, integration in integrations.items():
        status[name] = {
            "available": integration.is_available(),
            "enabled": integration.enabled,
            "framework": integration.name,
        }
    
    return status

__all__ = [
    "OpenAIAgentsIntegration",
    "LangGraphIntegration", 
    "LlamaIndexIntegration",
    "BaseIntegration",
    "openai_agents",
    "langgraph",
    "llamaindex",
    "enable_arc_tracing",
    "disable_arc_tracing", 
    "get_integration_status",
]