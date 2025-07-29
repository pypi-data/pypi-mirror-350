"""Helper functions for exporters."""

import json
import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Union, Any
from uuid import UUID

# Configure logger
logger = logging.getLogger("arc_tracing")

def format_trace_for_backend(
    formatted_spans: List[Dict],
    project_id: Optional[Union[str, UUID]] = None,
    agent_id: Optional[Union[str, UUID]] = None
) -> Dict:
    """
    Convert OpenTelemetry spans to the backend's expected trace format.
    This method can be used by other components (like BatchUploader) to
    ensure consistent formatting.
    
    Args:
        formatted_spans: Formatted span dictionaries
        project_id: Optional project ID (UUID or string)
        agent_id: Optional agent ID (UUID or string)
        
    Returns:
        A trace dictionary matching the backend's expected format
    """
    # Format according to TraceCreate model requirements
    trace_input = {
        "content": "test query",  # Default value
        "type": "text"
    }
    
    trace_output = {
        "content": "test response",  # Default value
        "type": "text"
    }
    
    # Extract trace data from spans
    steps = []
    metrics = {}
    signals = {}
    metadata = {
        "sdk_version": "0.1.0",
        "framework": "arc_tracing_sdk"
    }
    
    # Track timestamps for step ordering
    span_timestamps = {}
    
    # First pass - extract general information and identify span types
    for span in formatted_spans:
        attrs = span.get("attributes", {})
        span_name = span.get("name", "")
        
        # Get input from attributes
        if "arc_tracing.agent.input" in attrs:
            trace_input["content"] = attrs["arc_tracing.agent.input"]
        
        # Get output from attributes
        if "arc_tracing.agent.result" in attrs:
            trace_output["content"] = attrs["arc_tracing.agent.result"]
            
        # Track timestamps
        start_time = span.get("start_time")
        end_time = span.get("end_time")
        if start_time and end_time:
            span_timestamps[span["span_id"]] = {
                "start": start_time,
                "end": end_time,
                "span_name": span_name,
                "attrs": attrs
            }
        
        # Extract framework information if available
        if "arc_tracing.agent.frameworks" in attrs:
            frameworks = attrs["arc_tracing.agent.frameworks"]
            if isinstance(frameworks, str):
                if "," in frameworks:
                    # Use the first framework if multiple are detected
                    metadata["framework"] = frameworks.split(",")[0].strip()
                else:
                    metadata["framework"] = frameworks
        
        # Extract metrics
        for key, value in attrs.items():
            # Handle metrics
            if key.startswith("metrics."):
                metric_name = key.split(".", 1)[1]
                metrics[metric_name] = value
            # Handle signals
            elif key.startswith("signals."):
                signal_name = key.split(".", 1)[1]
                signals[signal_name] = value
            # Handle metadata
            elif key.startswith("metadata."):
                metadata_name = key.split(".", 1)[1]
                metadata[metadata_name] = value
    
    # Second pass - create properly formatted steps with ISO timestamps
    for span_id, info in span_timestamps.items():
        # Get span info
        attrs = info["attrs"]
        span_name = info["span_name"]
        
        # Determine step type
        step_type = "agent_action"  # Default type
        
        if "llm" in span_name:
            step_type = "llm_call"
        elif "tool" in span_name or "search" in span_name or "retrieval" in span_name:
            step_type = "tool_call"
        
        # Try to get more specific type from attributes
        if "step.type" in attrs:
            step_type = attrs["step.type"]
        
        # Create ISO timestamp
        try:
            # Convert nanoseconds to seconds for datetime
            timestamp_seconds = info["start"] / 1_000_000_000
            iso_timestamp = datetime.fromtimestamp(
                timestamp_seconds, tz=timezone.utc
            ).isoformat()
        except Exception:
            # Fallback to current time if conversion fails
            iso_timestamp = datetime.now(timezone.utc).isoformat()
        
        # Calculate duration in milliseconds
        duration_ms = (info["end"] - info["start"]) / 1_000_000  # Convert ns to ms
        
        # Build step details
        details = {}
        
        # Extract LLM-specific details
        if step_type == "llm_call":
            if "llm.model" in attrs:
                details["model"] = attrs["llm.model"]
            if "llm.prompt" in attrs:
                details["prompt"] = attrs["llm.prompt"]
            if "llm.response" in attrs or "llm.completion" in attrs:
                details["completion"] = attrs.get("llm.response") or attrs.get("llm.completion")
            
            # Extract token information
            tokens = {}
            if "metrics.tokens.prompt" in attrs:
                tokens["prompt"] = attrs["metrics.tokens.prompt"]
            if "metrics.tokens.completion" in attrs:
                tokens["completion"] = attrs["metrics.tokens.completion"]
            if "metrics.tokens.total" in attrs:
                tokens["total"] = attrs["metrics.tokens.total"]
            
            if tokens:
                details["tokens"] = tokens
                
        # Extract tool-specific details
        elif step_type == "tool_call":
            if "tool.name" in attrs:
                details["tool_name"] = attrs["tool.name"]
            elif "tool_name" in attrs:
                details["tool_name"] = attrs["tool_name"]
            else:
                # Extract from span name if possible
                parts = span_name.split(".")
                if len(parts) > 1:
                    details["tool_name"] = parts[-1]
                else:
                    details["tool_name"] = "unknown_tool"
            
            if "tool.input" in attrs:
                details["input"] = attrs["tool.input"]
            elif "input" in attrs:
                details["input"] = attrs["input"]
                
            if "tool.output" in attrs:
                details["output"] = attrs["tool.output"]
            elif "output" in attrs:
                details["output"] = attrs["output"]
        
        # Create step with all information
        # Ensure span_id doesn't have '0x' prefix if it's from hex() function
        normalized_span_id = span_id[2:] if isinstance(span_id, str) and span_id.startswith('0x') else span_id
        
        step = {
            "step_id": normalized_span_id,  # Use normalized span_id as step_id
            "type": step_type,
            "timestamp": iso_timestamp,
            "duration_ms": int(duration_ms),
            "details": details
        }
        
        steps.append(step)
    
    # Sort steps by timestamp
    steps.sort(key=lambda step: step["timestamp"])
    
    # Assemble the final trace data according to TraceCreate
    trace = {
        "input": trace_input,
        "output": trace_output,
        "steps": steps,
    }
    
    # Add optional fields
    if metrics:
        trace["metrics"] = metrics
        
    if signals:
        trace["signals"] = signals
        
    if metadata:
        trace["metadata"] = metadata
        
    # Add project_id and agent_id if available (with UUID conversion)
    if project_id:
        try:
            # If it's already a UUID, use it directly
            if isinstance(project_id, UUID):
                trace["project_id"] = str(project_id)
            else:
                # Try to parse as UUID or create a deterministic UUID from the string
                try:
                    # Try to parse as a UUID string first
                    trace["project_id"] = str(UUID(project_id))
                except ValueError:
                    # If not a valid UUID string, create a deterministic UUID from it
                    trace["project_id"] = str(uuid.uuid5(uuid.NAMESPACE_OID, str(project_id)))
        except Exception as e:
            logger.warning(f"Could not use project_id as UUID: {e}")
            
    if agent_id:
        try:
            # If it's already a UUID, use it directly
            if isinstance(agent_id, UUID):
                trace["agent_id"] = str(agent_id)
            else:
                # Try to parse as UUID or create a deterministic UUID from the string
                try:
                    # Try to parse as a UUID string first
                    trace["agent_id"] = str(UUID(agent_id))
                except ValueError:
                    # If not a valid UUID string, create a deterministic UUID from it
                    trace["agent_id"] = str(uuid.uuid5(uuid.NAMESPACE_OID, str(agent_id)))
        except Exception as e:
            logger.warning(f"Could not use agent_id as UUID: {e}")
    
    return trace

def is_valid_uuid(uuid_string: str) -> bool:
    """
    Check if a string is a valid UUID.
    
    Args:
        uuid_string: The string to check
        
    Returns:
        True if the string is a valid UUID, False otherwise
    """
    try:
        uuid_obj = uuid.UUID(uuid_string)
        return str(uuid_obj) == uuid_string
    except (ValueError, AttributeError, TypeError):
        return False