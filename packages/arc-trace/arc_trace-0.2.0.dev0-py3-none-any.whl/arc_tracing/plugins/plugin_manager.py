"""Plugin manager for discovering and managing community plugins."""

import logging
import importlib
import importlib.util
import pkg_resources
from typing import Any, Dict, List, Optional, Type
from arc_tracing.plugins.plugin_interface import PluginInterface, PromptExtractorPlugin

logger = logging.getLogger("arc_tracing")

class PluginManager:
    """
    Plugin manager for discovering and managing Arc Tracing SDK plugins.
    
    Follows NVIDIA AIQ plugin architecture with entry points and
    automatic discovery.
    """
    
    def __init__(self):
        self._plugins: Dict[str, PluginInterface] = {}
        self._prompt_extractors: List[PromptExtractorPlugin] = []
        self._loaded = False
    
    def discover_plugins(self) -> None:
        """
        Discover plugins from multiple sources:
        1. Entry points (setuptools)
        2. Built-in plugins
        3. Local plugin directories
        """
        if self._loaded:
            return
        
        logger.info("Discovering Arc Tracing SDK plugins...")
        
        # Method 1: Discover via setuptools entry points
        self._discover_entry_point_plugins()
        
        # Method 2: Load built-in plugins
        self._load_builtin_plugins()
        
        # Method 3: Discover local plugins
        self._discover_local_plugins()
        
        self._loaded = True
        
        logger.info(f"Discovered {len(self._plugins)} plugins ({len(self._prompt_extractors)} prompt extractors)")
    
    def _discover_entry_point_plugins(self) -> None:
        """Discover plugins via setuptools entry points."""
        try:
            # Look for entry points under 'arc_tracing.plugins'
            for entry_point in pkg_resources.iter_entry_points('arc_tracing.plugins'):
                try:
                    plugin_class = entry_point.load()
                    
                    # Verify it's a valid plugin
                    if issubclass(plugin_class, PluginInterface):
                        plugin_instance = plugin_class()
                        self._register_plugin(plugin_instance)
                        logger.info(f"Loaded entry point plugin: {plugin_instance.name}")
                    else:
                        logger.warning(f"Entry point {entry_point.name} is not a valid plugin")
                        
                except Exception as e:
                    logger.error(f"Failed to load entry point plugin {entry_point.name}: {e}")
                    
        except Exception as e:
            logger.warning(f"Error discovering entry point plugins: {e}")
    
    def _load_builtin_plugins(self) -> None:
        """Load built-in plugins from the plugin interface module."""
        try:
            # Import the plugin functions to trigger decorator registration
            from arc_tracing.plugins import plugin_interface
            
            # Get all functions with _arc_plugin attribute
            for attr_name in dir(plugin_interface):
                attr = getattr(plugin_interface, attr_name)
                if hasattr(attr, '_arc_plugin'):
                    plugin = attr._arc_plugin
                    self._register_plugin(plugin)
                    logger.debug(f"Loaded built-in plugin: {plugin.name}")
                    
        except Exception as e:
            logger.warning(f"Error loading built-in plugins: {e}")
    
    def _discover_local_plugins(self) -> None:
        """Discover plugins in local directories."""
        import os
        
        # Look for plugins in common locations
        plugin_dirs = [
            os.path.expanduser("~/.arc_tracing/plugins"),
            os.path.join(os.getcwd(), "arc_plugins"),
            "./plugins",
        ]
        
        for plugin_dir in plugin_dirs:
            if os.path.isdir(plugin_dir):
                self._scan_plugin_directory(plugin_dir)
    
    def _scan_plugin_directory(self, directory: str) -> None:
        """Scan a directory for Python plugin files."""
        import os
        import glob
        
        try:
            # Look for Python files
            pattern = os.path.join(directory, "*.py")
            for file_path in glob.glob(pattern):
                if os.path.basename(file_path).startswith('_'):
                    continue  # Skip private files
                
                self._load_plugin_file(file_path)
                
        except Exception as e:
            logger.warning(f"Error scanning plugin directory {directory}: {e}")
    
    def _load_plugin_file(self, file_path: str) -> None:
        """Load plugins from a Python file."""
        try:
            # Load module from file
            spec = importlib.util.spec_from_file_location("plugin_module", file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for plugin classes and functions
                for name in dir(module):
                    obj = getattr(module, name)
                    
                    # Check for plugin classes
                    if (isinstance(obj, type) and 
                        issubclass(obj, PluginInterface) and 
                        obj != PluginInterface):
                        try:
                            plugin_instance = obj()
                            self._register_plugin(plugin_instance)
                            logger.info(f"Loaded file plugin: {plugin_instance.name} from {file_path}")
                        except Exception as e:
                            logger.error(f"Failed to instantiate plugin {name}: {e}")
                    
                    # Check for decorated functions
                    elif hasattr(obj, '_arc_plugin'):
                        plugin = obj._arc_plugin
                        self._register_plugin(plugin)
                        logger.info(f"Loaded function plugin: {plugin.name} from {file_path}")
                        
        except Exception as e:
            logger.error(f"Failed to load plugin file {file_path}: {e}")
    
    def _register_plugin(self, plugin: PluginInterface) -> None:
        """Register a discovered plugin."""
        try:
            # Check if plugin is available
            if not plugin.is_available():
                logger.debug(f"Plugin {plugin.name} not available (framework not installed)")
                return
            
            # Avoid duplicate registrations
            if plugin.name in self._plugins:
                logger.warning(f"Plugin {plugin.name} already registered, skipping")
                return
            
            # Register the plugin
            self._plugins[plugin.name] = plugin
            
            # Add to specialized lists
            if isinstance(plugin, PromptExtractorPlugin):
                self._prompt_extractors.append(plugin)
            
            logger.debug(f"Registered plugin: {plugin.name} v{plugin.version} for {plugin.framework}")
            
        except Exception as e:
            logger.error(f"Failed to register plugin {plugin.name}: {e}")
    
    def get_plugin(self, name: str) -> Optional[PluginInterface]:
        """Get a plugin by name."""
        self.discover_plugins()
        return self._plugins.get(name)
    
    def get_plugins_for_framework(self, framework: str) -> List[PluginInterface]:
        """Get all plugins for a specific framework."""
        self.discover_plugins()
        return [plugin for plugin in self._plugins.values() if plugin.framework == framework]
    
    def get_prompt_extractors(self) -> List[PromptExtractorPlugin]:
        """Get all prompt extractor plugins."""
        self.discover_plugins()
        return self._prompt_extractors.copy()
    
    def extract_prompt_with_plugins(self, trace_data: Dict[str, Any]) -> Optional[tuple]:
        """
        Try to extract system prompt using available plugins.
        
        Args:
            trace_data: Trace data to process
            
        Returns:
            Tuple of (prompt_text, template_variables, prompt_source) or None
        """
        self.discover_plugins()
        
        # Try each prompt extractor plugin
        for extractor in self._prompt_extractors:
            try:
                if extractor.detect_framework_usage(trace_data):
                    result = extractor.extract_system_prompt(trace_data)
                    if result:
                        logger.debug(f"Extracted prompt using plugin: {extractor.name}")
                        return result
            except Exception as e:
                logger.warning(f"Plugin {extractor.name} failed to extract prompt: {e}")
                continue
        
        return None
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """
        List all discovered plugins with metadata.
        
        Returns:
            List of plugin metadata dictionaries
        """
        self.discover_plugins()
        
        plugins_info = []
        for plugin in self._plugins.values():
            info = {
                "name": plugin.name,
                "version": plugin.version,
                "framework": plugin.framework,
                "available": plugin.is_available(),
                "type": "prompt_extractor" if isinstance(plugin, PromptExtractorPlugin) else "generic",
            }
            
            # Add additional metadata if available
            if hasattr(plugin, 'get_metadata'):
                info.update(plugin.get_metadata())
            
            plugins_info.append(info)
        
        return plugins_info
    
    def enable_plugin(self, name: str) -> bool:
        """
        Enable a specific plugin.
        
        Args:
            name: Plugin name
            
        Returns:
            True if successfully enabled
        """
        plugin = self.get_plugin(name)
        if not plugin:
            logger.error(f"Plugin {name} not found")
            return False
        
        try:
            success = plugin.setup()
            if success:
                logger.info(f"Enabled plugin: {name}")
            else:
                logger.warning(f"Failed to enable plugin: {name}")
            return success
        except Exception as e:
            logger.error(f"Error enabling plugin {name}: {e}")
            return False
    
    def disable_plugin(self, name: str) -> None:
        """
        Disable a specific plugin.
        
        Args:
            name: Plugin name
        """
        plugin = self.get_plugin(name)
        if not plugin:
            logger.error(f"Plugin {name} not found")
            return
        
        try:
            plugin.teardown()
            logger.info(f"Disabled plugin: {name}")
        except Exception as e:
            logger.error(f"Error disabling plugin {name}: {e}")
    
    def enable_framework_plugins(self, framework: str) -> Dict[str, bool]:
        """
        Enable all plugins for a specific framework.
        
        Args:
            framework: Framework name
            
        Returns:
            Dictionary mapping plugin names to success status
        """
        plugins = self.get_plugins_for_framework(framework)
        results = {}
        
        for plugin in plugins:
            results[plugin.name] = self.enable_plugin(plugin.name)
        
        return results

# Global plugin manager instance
_plugin_manager = None

def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager instance."""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager