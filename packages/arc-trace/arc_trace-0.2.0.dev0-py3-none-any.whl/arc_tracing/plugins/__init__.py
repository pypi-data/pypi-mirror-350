"""Plugin system for community-driven framework integrations."""

from .plugin_manager import PluginManager, get_plugin_manager
from .plugin_interface import PluginInterface, PromptExtractorPlugin

__all__ = [
    "PluginManager",
    "get_plugin_manager",
    "PluginInterface", 
    "PromptExtractorPlugin",
]