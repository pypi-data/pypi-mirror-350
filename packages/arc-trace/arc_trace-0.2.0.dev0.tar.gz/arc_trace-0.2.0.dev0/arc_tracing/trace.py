"""Core tracing functionality for the Arc Tracing SDK."""

import functools
import inspect
import logging
import os
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast

from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from arc_tracing.detector import detect_frameworks

# Type variables for function signatures
F = TypeVar("F", bound=Callable[..., Any])

# Configure logger
logger = logging.getLogger("arc_tracing")

# Initialize tracer
tracer = trace.get_tracer("arc_tracing")

def trace_agent(func: F) -> F:
    """
    Decorator that adds tracing to an agent function.
    
    This is the primary entry point for the Arc Tracing SDK. When applied
    to an agent function, it automatically detects the frameworks being used
    and instruments them appropriately.
    
    Args:
        func: The agent function to trace
        
    Returns:
        The wrapped function with tracing enabled
    
    Example:
        >>> from arc_tracing import trace_agent
        >>> 
        >>> @trace_agent
        >>> def my_agent(query: str) -> str:
        >>>     # Agent implementation
        >>>     return response
        >>> 
        >>> # Or with a function reference
        >>> traced_agent = trace_agent(my_agent)
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Extract function signature info for better span naming
        sig = inspect.signature(func)
        
        # Detect frameworks being used
        frameworks = detect_frameworks()
        
        # Start a trace span for this agent execution
        with tracer.start_as_current_span(
            f"agent.{func.__name__}",
            attributes={
                "arc_tracing.agent.name": func.__name__,
                "arc_tracing.agent.frameworks": ",".join(frameworks),
                "code.function": func.__name__,
                "code.namespace": func.__module__,
            }
        ) as span:
            # Add function arguments as span attributes if appropriate
            # (careful not to include sensitive data or large objects)
            for param_name, param in sig.parameters.items():
                if param_name in kwargs and isinstance(kwargs[param_name], (str, int, float, bool)):
                    span.set_attribute(f"arc_tracing.agent.param.{param_name}", str(kwargs[param_name]))
                elif param_name == "self" and args and hasattr(args[0], "__class__"):
                    span.set_attribute("arc_tracing.agent.class", args[0].__class__.__name__)
            
            # Enable lightweight integrations for detected frameworks
            _enable_framework_integrations(frameworks)
            
            # Execute the wrapped function
            try:
                result = func(*args, **kwargs)
                
                # Record result information if appropriate
                if isinstance(result, (str, int, float, bool)):
                    span.set_attribute("arc_tracing.agent.result", str(result))
                elif hasattr(result, "__class__"):
                    span.set_attribute("arc_tracing.agent.result.type", result.__class__.__name__)
                
                return result
            except Exception as e:
                # Record exception information
                span.record_exception(e)
                span.set_status(trace.StatusCode.ERROR, str(e))
                raise
    
    return cast(F, wrapper)

def _enable_framework_integrations(frameworks: List[str]) -> None:
    """
    Enable lightweight framework integrations based on detected frameworks.
    
    This function uses the new integration-first approach that leverages
    existing tracing systems rather than monkey patching.
    
    Args:
        frameworks: List of detected framework identifiers.
    """
    # Track which frameworks have already been integrated to avoid re-enabling
    if not hasattr(_enable_framework_integrations, "_integrated"):
        _enable_framework_integrations._integrated = set()
    
    # Map detected framework names to integration names
    # Only modern frameworks with dedicated integrations
    framework_mapping = {
        "openai_agents_sdk": "openai_agents",
        "agents": "openai_agents", 
        "langgraph": "langgraph",
        "llamaindex": "llamaindex",
        "llamaindex_agent_workflow": "llamaindex",
    }
    
    # Determine which integrations to enable
    target_integrations = set()
    for framework in frameworks:
        integration_name = framework_mapping.get(framework)
        if integration_name and integration_name not in _enable_framework_integrations._integrated:
            target_integrations.add(integration_name)
    
    # Enable integrations
    if target_integrations:
        try:
            from arc_tracing.integrations import enable_arc_tracing
            
            # Enable only the detected frameworks
            results = enable_arc_tracing(list(target_integrations))
            
            # Track successfully enabled integrations
            for integration_name, success in results.items():
                if success:
                    _enable_framework_integrations._integrated.add(integration_name)
                    logger.debug(f"Enabled {integration_name} integration")
        
        except Exception as e:
            logger.warning(f"Failed to enable framework integrations: {e}")
    
    # For other frameworks, enable generic API interception and plugin system
    _enable_universal_coverage()

def _enable_universal_coverage() -> None:
    """
    Enable universal coverage through API interception and plugin system.
    
    This provides framework-agnostic tracing for any AI framework without
    requiring specific integrations.
    """
    try:
        # Enable API interceptors for universal coverage
        from arc_tracing.interceptors import OpenAIInterceptor, AnthropicInterceptor, GenericInterceptor
        
        interceptors = [
            OpenAIInterceptor(),
            AnthropicInterceptor(), 
            GenericInterceptor(),
        ]
        
        for interceptor in interceptors:
            try:
                if interceptor.enable():
                    logger.debug(f"Enabled {interceptor.name} API interceptor")
            except Exception as e:
                logger.warning(f"Failed to enable {interceptor.name} interceptor: {e}")
        
        # Enable plugin system for community frameworks
        from arc_tracing.plugins import get_plugin_manager
        
        plugin_manager = get_plugin_manager()
        plugin_manager.discover_plugins()
        
        # Enable available prompt extractor plugins
        for plugin in plugin_manager.get_prompt_extractors():
            try:
                if plugin.is_available():
                    plugin.setup()
                    logger.debug(f"Enabled plugin: {plugin.name}")
            except Exception as e:
                logger.warning(f"Failed to enable plugin {plugin.name}: {e}")
                
    except Exception as e:
        logger.warning(f"Failed to enable universal coverage: {e}")