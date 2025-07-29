"""Prompt sanitization utilities for Arc Tracing SDK."""

import re
import logging
from typing import Any, Dict, List

logger = logging.getLogger("arc_tracing")

# Default sensitive patterns to mask
DEFAULT_MASK_PATTERNS = [
    r"api[_-]?key",
    r"password", 
    r"secret",
    r"token",
    r"auth",
    r"credential",
    r"private[_-]?key",
    r"access[_-]?key",
    r"bearer",
    # Common formats
    r"sk-[a-zA-Z0-9]{48}",  # OpenAI API keys
    r"xoxb-[0-9]+-[0-9]+-[a-zA-Z0-9]+",  # Slack bot tokens
    r"ghp_[a-zA-Z0-9]{36}",  # GitHub personal access tokens
    r"gho_[a-zA-Z0-9]{36}",  # GitHub OAuth tokens
    r"AIza[0-9A-Za-z-_]{35}",  # Google API keys
    r"AKIA[0-9A-Z]{16}",  # AWS access keys
]

def sanitize_prompt(prompt_text: str, config: Any) -> str:
    """
    Remove sensitive information from prompts before transmission.
    
    This function provides comprehensive privacy protection by:
    1. Masking sensitive patterns (API keys, secrets, etc.)
    2. Truncating overly long prompts
    3. Applying custom user-defined filters
    
    Args:
        prompt_text: The raw prompt text to sanitize
        config: Configuration object with privacy settings
        
    Returns:
        Sanitized prompt text safe for transmission
        
    Example:
        >>> config = {"trace": {"prompt_privacy": {"enabled": True, "max_length": 1000}}}
        >>> sanitize_prompt("Your API key is sk-abcd1234", config)
        "Your API key is [MASKED]"
    """
    if not prompt_text:
        return prompt_text
    
    # Check if prompt privacy is enabled
    privacy_config = config.get("trace", {}).get("prompt_privacy", {})
    if not privacy_config.get("enabled", True):
        return prompt_text
    
    sanitized = prompt_text
    
    try:
        # Apply masking patterns
        mask_patterns = privacy_config.get("mask_patterns", DEFAULT_MASK_PATTERNS)
        sanitized = _apply_mask_patterns(sanitized, mask_patterns)
        
        # Truncate if too long
        max_length = privacy_config.get("max_length", 2000)
        if max_length > 0 and len(sanitized) > max_length:
            sanitized = sanitized[:max_length] + "...[TRUNCATED]"
        
        # Apply custom filters if configured
        custom_filters = privacy_config.get("custom_filters", [])
        sanitized = _apply_custom_filters(sanitized, custom_filters)
        
    except Exception as e:
        logger.warning(f"Error during prompt sanitization: {e}")
        # Fallback to basic truncation
        max_length = privacy_config.get("max_length", 2000)
        if max_length > 0 and len(prompt_text) > max_length:
            sanitized = prompt_text[:max_length] + "...[TRUNCATED]"
        else:
            sanitized = prompt_text
    
    return sanitized

def _apply_mask_patterns(text: str, patterns: List[str]) -> str:
    """
    Apply regex masking patterns to text.
    
    Args:
        text: Text to process
        patterns: List of regex patterns to mask
        
    Returns:
        Text with sensitive patterns masked
    """
    for pattern in patterns:
        try:
            # Use word boundaries and case-insensitive matching for better detection
            regex = re.compile(rf"\b{pattern}\b[^\s]*", re.IGNORECASE)
            text = regex.sub("[MASKED]", text)
            
            # Also handle patterns that might be in quotes or special contexts
            regex_quoted = re.compile(rf'["\']?{pattern}["\']?\s*[:=]\s*["\']?[^\s"\']+["\']?', re.IGNORECASE)
            text = regex_quoted.sub(f"{pattern}: [MASKED]", text)
            
        except re.error as e:
            logger.warning(f"Invalid regex pattern '{pattern}': {e}")
            continue
    
    return text

def _apply_custom_filters(text: str, custom_filters: List[Dict[str, str]]) -> str:
    """
    Apply user-defined custom filters to text.
    
    Args:
        text: Text to process
        custom_filters: List of filter configurations
        
    Returns:
        Text with custom filters applied
        
    Example custom_filters:
        [
            {"pattern": r"user_id_\d+", "replacement": "[USER_ID]"},
            {"pattern": r"email.*@.*\.com", "replacement": "[EMAIL]"}
        ]
    """
    for filter_config in custom_filters:
        try:
            pattern = filter_config.get("pattern")
            replacement = filter_config.get("replacement", "[FILTERED]")
            
            if pattern:
                regex = re.compile(pattern, re.IGNORECASE)
                text = regex.sub(replacement, text)
                
        except (re.error, KeyError) as e:
            logger.warning(f"Error applying custom filter {filter_config}: {e}")
            continue
    
    return text

def validate_prompt_safety(prompt_text: str, strict_mode: bool = False) -> Dict[str, Any]:
    """
    Validate if a prompt contains potentially sensitive information.
    
    This function analyzes prompt content and returns a safety assessment
    without modifying the original text.
    
    Args:
        prompt_text: Text to analyze
        strict_mode: If True, applies more aggressive detection rules
        
    Returns:
        Dictionary containing safety assessment:
        {
            "is_safe": bool,
            "risk_level": str,  # "low", "medium", "high"
            "detected_patterns": List[str],
            "recommendations": List[str]
        }
    """
    if not prompt_text:
        return {
            "is_safe": True,
            "risk_level": "low",
            "detected_patterns": [],
            "recommendations": []
        }
    
    detected_patterns = []
    recommendations = []
    
    # Check for common sensitive patterns
    for pattern in DEFAULT_MASK_PATTERNS:
        try:
            if re.search(pattern, prompt_text, re.IGNORECASE):
                detected_patterns.append(pattern)
        except re.error:
            continue
    
    # Assess risk level
    if len(detected_patterns) == 0:
        risk_level = "low"
        is_safe = True
    elif len(detected_patterns) <= 2:
        risk_level = "medium"
        is_safe = not strict_mode
        recommendations.append("Consider reviewing prompt content for sensitive information")
    else:
        risk_level = "high"
        is_safe = False
        recommendations.append("Prompt contains multiple potentially sensitive patterns")
        recommendations.append("Enable prompt sanitization before transmission")
    
    # Additional checks for strict mode
    if strict_mode:
        # Check for PII patterns
        pii_patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",  # Credit card
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
        ]
        
        for pattern in pii_patterns:
            if re.search(pattern, prompt_text):
                detected_patterns.append(f"PII: {pattern}")
                is_safe = False
                recommendations.append("Detected potential PII - consider data anonymization")
    
    return {
        "is_safe": is_safe,
        "risk_level": risk_level,
        "detected_patterns": detected_patterns,
        "recommendations": recommendations
    }

def get_prompt_stats(prompt_text: str) -> Dict[str, Any]:
    """
    Get statistical information about a prompt.
    
    Args:
        prompt_text: Text to analyze
        
    Returns:
        Dictionary with prompt statistics
    """
    if not prompt_text:
        return {"length": 0, "words": 0, "lines": 0}
    
    return {
        "length": len(prompt_text),
        "words": len(prompt_text.split()),
        "lines": len(prompt_text.splitlines()),
        "has_newlines": "\n" in prompt_text,
        "has_special_chars": bool(re.search(r'[^\w\s]', prompt_text)),
    }