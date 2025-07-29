"""Configuration handling for Arc Tracing SDK."""

import os
import yaml
from typing import Any, Dict, List, Optional, Union
import logging

# Default configuration
DEFAULT_CONFIG = {
    "trace": {
        "frameworks": "auto",
        "detail_level": "standard",
        "endpoint": "http://localhost:8000/api/v1/traces",
        "auth": {
            "api_key": "dev_arc_rewardlab_key",
            "method": "header",
            "header": "X-API-Key"
        },
        "fallback": {
            "enabled": True,
            "local_file": {
                "enabled": True,
                "directory": "./arc_traces"
            }
        },
        # System prompt extraction settings
        "capture_prompts": True,  # Enable/disable automatic prompt capture
        "prompt_privacy": {
            "enabled": True,  # Enable privacy filtering
            "mask_patterns": [  # Regex patterns to mask in prompts
                r"api[_-]?key",
                r"password", 
                r"secret",
                r"token"
            ],
            "max_length": 2000,  # Truncate prompts longer than this
            "custom_filters": []  # User-defined custom filters
        },
        # Optional agent/project identification
        "project_id": None,
        "agent_id": None,
        "signals": []
    }
}

# Configure logger
logger = logging.getLogger("arc_tracing")

class Config:
    """Configuration manager for Arc Tracing SDK."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration with optional YAML file path.
        
        Args:
            config_path: Path to a YAML configuration file.
                If None, will look for 'arc_config.yml' in working directory
                or use environment variables.
        """
        self._config = DEFAULT_CONFIG.copy()
        
        # Try to load from config file
        if config_path is None:
            config_path = os.environ.get("ARC_CONFIG_PATH", "arc_config.yml")
        
        self._load_from_file(config_path)
        self._load_from_env()
    
    def _load_from_file(self, config_path: str) -> None:
        """Load configuration from YAML file if it exists."""
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    file_config = yaml.safe_load(f)
                    if file_config and isinstance(file_config, dict):
                        self._merge_config(file_config)
                    logger.info(f"Loaded configuration from {config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # API key from environment
        api_key = os.environ.get("ARC_API_KEY")
        if api_key:
            self._config["trace"]["auth"]["api_key"] = api_key
        
        # Endpoint from environment
        endpoint = os.environ.get("ARC_TRACE_ENDPOINT")
        if endpoint:
            self._config["trace"]["endpoint"] = endpoint
        
        # Detail level from environment
        detail_level = os.environ.get("ARC_TRACE_DETAIL")
        if detail_level:
            self._config["trace"]["detail_level"] = detail_level
            
        # Project and agent IDs
        project_id = os.environ.get("ARC_PROJECT_ID")
        if project_id:
            self._config["trace"]["project_id"] = project_id
            
        agent_id = os.environ.get("ARC_AGENT_ID")
        if agent_id:
            self._config["trace"]["agent_id"] = agent_id
            
        # Fallback settings from environment
        fallback_enabled = os.environ.get("ARC_FALLBACK_ENABLED")
        if fallback_enabled is not None:
            self._config["trace"]["fallback"]["enabled"] = fallback_enabled.lower() in ("true", "1", "yes")
            
        # Prompt capture settings from environment
        capture_prompts = os.environ.get("ARC_CAPTURE_PROMPTS")
        if capture_prompts is not None:
            self._config["trace"]["capture_prompts"] = capture_prompts.lower() in ("true", "1", "yes")
            
        prompt_max_length = os.environ.get("ARC_PROMPT_MAX_LENGTH")
        if prompt_max_length:
            try:
                self._config["trace"]["prompt_privacy"]["max_length"] = int(prompt_max_length)
            except ValueError:
                logger.warning(f"Invalid ARC_PROMPT_MAX_LENGTH value: {prompt_max_length}")
                
        prompt_privacy_enabled = os.environ.get("ARC_PROMPT_PRIVACY_ENABLED")
        if prompt_privacy_enabled is not None:
            self._config["trace"]["prompt_privacy"]["enabled"] = prompt_privacy_enabled.lower() in ("true", "1", "yes")
    
    def _merge_config(self, config: Dict[str, Any]) -> None:
        """Recursively merge configuration dictionaries."""
        for key, value in config.items():
            if (
                key in self._config 
                and isinstance(self._config[key], dict) 
                and isinstance(value, dict)
            ):
                # Recursively merge nested dictionaries
                for k, v in value.items():
                    self._config[key][k] = v
            else:
                self._config[key] = value
    
    @property
    def api_key(self) -> Optional[str]:
        """Get the API key for authentication."""
        return self._config["trace"]["auth"]["api_key"]
    
    @property
    def endpoint(self) -> str:
        """Get the trace endpoint URL."""
        return self._config["trace"]["endpoint"]
    
    @property
    def detail_level(self) -> str:
        """Get the trace detail level."""
        return self._config["trace"]["detail_level"]
    
    @property
    def frameworks(self) -> Union[str, List[str]]:
        """Get the frameworks configuration."""
        return self._config["trace"]["frameworks"]
    
    @property
    def signals(self) -> List[Dict[str, str]]:
        """Get the configured signals for extraction."""
        return self._config["trace"]["signals"]
        
    @property
    def project_id(self) -> Optional[str]:
        """Get the project ID for trace metadata."""
        return self.get("trace.project_id")
    
    @property
    def agent_id(self) -> Optional[str]:
        """Get the agent ID for trace metadata."""
        return self.get("trace.agent_id")
    
    @property
    def export_dir(self) -> Optional[str]:
        """Get the local export directory."""
        return self.get("trace.fallback.local_file.directory")
    
    @property
    def fallback_enabled(self) -> bool:
        """Check if fallback mechanisms are enabled."""
        return self.get("trace.fallback.enabled", True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get any configuration value by key path."""
        parts = key.split(".")
        config = self._config
        
        for part in parts:
            if part in config:
                config = config[part]
            else:
                return default
        
        return config

# Singleton configuration instance
_config_instance = None

def get_config(config_path: Optional[str] = None) -> Config:
    """
    Get the global configuration instance.
    
    Args:
        config_path: Optional path to a configuration file.
            If provided, reloads the configuration.
    
    Returns:
        The global configuration instance.
    """
    global _config_instance
    
    if _config_instance is None or config_path is not None:
        _config_instance = Config(config_path)
    
    return _config_instance