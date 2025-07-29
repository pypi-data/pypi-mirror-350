"""Framework detection module for Arc Tracing SDK."""

import importlib.util
import inspect
import sys
from typing import Dict, List, Set, Optional

def detect_frameworks() -> List[str]:
    """
    Detect which LLM frameworks are being used.
    
    This function inspects the loaded modules and call stack to determine
    which LLM frameworks are currently in use. It can detect:
    - LangChain
    - LlamaIndex
    - AutoGen
    - Direct LLM API calls (OpenAI, Anthropic, etc.)
    - Custom implementations
    
    Returns:
        A list of framework identifiers found in use.
    
    Example:
        >>> frameworks = detect_frameworks()
        >>> print(frameworks)
        ['langchain', 'openai']
    """
    frameworks: Set[str] = set()
    
    # Check for imported modules
    _check_imported_modules(frameworks)
    
    # Check call stack for framework-specific patterns
    _check_call_stack(frameworks)
    
    return sorted(list(frameworks))

def _check_imported_modules(frameworks: Set[str]) -> None:
    """Check which framework modules have been imported."""
    
    # OpenAI Agents SDK detection (2025 - replaces Swarm)
    if importlib.util.find_spec("agents") is not None:
        frameworks.add("openai_agents_sdk")
    
    # LangGraph detection (2025 - modern LangChain agent replacement)
    if importlib.util.find_spec("langgraph") is not None:
        frameworks.add("langgraph")
    
    # LangChain detection (legacy and LCEL)
    if importlib.util.find_spec("langchain") is not None:
        frameworks.add("langchain")
    if importlib.util.find_spec("langchain_openai") is not None:
        frameworks.add("langchain_openai")
    if importlib.util.find_spec("langchain_core") is not None:
        frameworks.add("langchain_core")
    
    # LlamaIndex detection (including 2025 AgentWorkflow)
    if (importlib.util.find_spec("llama_index") is not None or 
        importlib.util.find_spec("gpt_index") is not None):
        frameworks.add("llamaindex")
    
    # Check for specific LlamaIndex AgentWorkflow (2025) - with safe checking
    try:
        if importlib.util.find_spec("llama_index.core.agent.workflow") is not None:
            frameworks.add("llamaindex_agent_workflow")
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    
    # AutoGen detection
    if importlib.util.find_spec("autogen") is not None:
        frameworks.add("autogen")
    
    # Direct LLM API clients
    for module_name in ["openai", "anthropic", "cohere", "ai21", "together", "google.generativeai"]:
        if importlib.util.find_spec(module_name) is not None:
            frameworks.add(module_name.split(".")[-1])
    
    # Agent frameworks
    if importlib.util.find_spec("agno") is not None:
        frameworks.add("agno")
    
    if importlib.util.find_spec("google.adk") is not None:
        frameworks.add("google_adk")

def _check_call_stack(frameworks: Set[str]) -> None:
    """Inspect call stack for framework-specific patterns."""
    
    # Get current call stack
    stack = inspect.stack()
    
    # Check each frame in the stack
    for frame_info in stack:
        frame = frame_info.frame
        module_name = frame.f_globals.get("__name__", "")
        
        # Detect OpenAI Agents SDK from call stack (2025)
        if module_name.startswith("agents"):
            frameworks.add("openai_agents_sdk")
        
        # Detect LangGraph from call stack (2025)
        if module_name.startswith("langgraph"):
            frameworks.add("langgraph")
        
        # Detect LangChain from call stack (including LCEL)
        if module_name.startswith("langchain"):
            frameworks.add("langchain")
            # Check for specific LangChain components
            if "langchain_core" in module_name:
                frameworks.add("langchain_core")
        
        # Detect LlamaIndex from call stack (including AgentWorkflow)
        if module_name.startswith(("llama_index", "gpt_index")):
            frameworks.add("llamaindex")
            # Check for AgentWorkflow specifically
            if "agent.workflow" in module_name:
                frameworks.add("llamaindex_agent_workflow")
        
        # Detect AutoGen from call stack
        if module_name.startswith("autogen"):
            frameworks.add("autogen")
        
        # Direct API detection from module names
        for api_name in ["openai", "anthropic", "cohere", "ai21", "together"]:
            if module_name.startswith(api_name):
                frameworks.add(api_name)
        
        # Agent frameworks detection from module names
        if module_name.startswith("agno"):
            frameworks.add("agno")
        
        if module_name.startswith("google.adk"):
            frameworks.add("google_adk")