"""OpenAI Agents SDK integration for Arc Tracing SDK."""

import logging
import importlib.util
from typing import Any, Dict, List, Optional, Tuple
from arc_tracing.integrations.base import BaseIntegration

logger = logging.getLogger("arc_tracing")

class OpenAIAgentsIntegration(BaseIntegration):
    """
    Integration adapter for OpenAI Agents SDK.
    
    This integration leverages the built-in tracing system of OpenAI Agents SDK
    by adding a custom trace processor that sends data to Arc platform.
    
    The OpenAI Agents SDK provides comprehensive built-in tracing with:
    - LLM generations and completions
    - Tool calls and results  
    - Agent handoffs and coordination
    - Custom events and spans
    
    We extend this system rather than replacing it.
    """
    
    def __init__(self):
        super().__init__("openai_agents")
        self._trace_processor = None
    
    def is_available(self) -> bool:
        """Check if OpenAI Agents SDK is available."""
        try:
            import agents
            return True
        except ImportError:
            return False
    
    def _setup_integration(self) -> bool:
        """Set up integration with OpenAI Agents SDK built-in tracing."""
        try:
            import agents
            from agents import tracing
            
            # Create Arc trace processor
            self._trace_processor = ArcTraceProcessor(self)
            
            # Add our processor to the built-in tracing system
            # This hooks into their existing comprehensive tracing
            tracing.add_trace_processor(self._trace_processor)
            
            logger.info("Hooked into OpenAI Agents SDK built-in tracing system")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup OpenAI Agents integration: {e}")
            return False
    
    def _teardown_integration(self) -> None:
        """Clean up the integration."""
        try:
            if self._trace_processor:
                import agents
                from agents import tracing
                
                # Remove our processor from the tracing system
                tracing.remove_trace_processor(self._trace_processor)
                self._trace_processor = None
                
        except Exception as e:
            logger.error(f"Error during OpenAI Agents integration teardown: {e}")
    
    def extract_system_prompt(self, trace_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
        """
        Extract system prompt from OpenAI Agents trace data.
        
        Args:
            trace_data: OpenAI Agents trace data
            
        Returns:
            Tuple of (prompt_text, template_variables, prompt_source) or None if no prompt found
        """
        try:
            # Check for agent instructions in various trace data locations
            prompt_text = None
            template_vars = None
            
            # Method 1: Extract from agent_run span type
            if trace_data.get("span_type") == "agent_run":
                agent_instructions = trace_data.get("agent_instructions")
                if agent_instructions:
                    prompt_text = agent_instructions
                    
            # Method 2: Extract from agent configuration in trace metadata
            elif "agent_config" in trace_data:
                agent_config = trace_data["agent_config"]
                if isinstance(agent_config, dict):
                    prompt_text = agent_config.get("instructions") or agent_config.get("system_prompt")
                    template_vars = agent_config.get("template_vars")
                    
            # Method 3: Extract from attributes
            elif "attributes" in trace_data:
                attributes = trace_data["attributes"]
                prompt_text = (
                    attributes.get("agents.agent.instructions") or
                    attributes.get("agents.agent.system_prompt") or
                    attributes.get("agents.system_message")
                )
                
            # Method 4: Extract from LLM generation messages
            elif trace_data.get("span_type") == "llm_generation":
                messages = trace_data.get("messages", [])
                if messages and isinstance(messages, list):
                    # Look for system role message
                    for message in messages:
                        if isinstance(message, dict) and message.get("role") == "system":
                            prompt_text = message.get("content")
                            break
                            
            # Method 5: Extract from span metadata or events
            if not prompt_text:
                metadata = trace_data.get("metadata", {})
                prompt_text = (
                    metadata.get("system_prompt") or
                    metadata.get("agent_instructions") or
                    metadata.get("instructions")
                )
                template_vars = metadata.get("template_variables")
                
            # Method 6: Check events for prompt information
            if not prompt_text:
                events = trace_data.get("events", [])
                for event in events:
                    if isinstance(event, dict):
                        event_name = event.get("name", "").lower()
                        if "prompt" in event_name or "instruction" in event_name:
                            event_data = event.get("data", {})
                            if isinstance(event_data, dict):
                                prompt_text = (
                                    event_data.get("system_prompt") or
                                    event_data.get("instructions") or
                                    event_data.get("content")
                                )
                                template_vars = event_data.get("template_vars")
                                break
            
            if prompt_text and isinstance(prompt_text, str) and prompt_text.strip():
                return (prompt_text.strip(), template_vars, "openai_agents")
                
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting system prompt from OpenAI Agents trace: {e}")
            return None
    
    def format_trace_for_arc(self, trace_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert OpenAI Agents trace data to Arc format."""
        arc_trace = super().format_trace_for_arc(trace_data)
        
        # Add OpenAI Agents specific attributes
        arc_trace.update({
            "agent_name": trace_data.get("agent_name"),
            "agent_type": trace_data.get("agent_type"),
            "operation_type": trace_data.get("operation_type"),  # "agent_run", "tool_call", "handoff"
            "input": trace_data.get("input"),
            "output": trace_data.get("output"),
            "duration_ms": trace_data.get("duration_ms"),
            "token_usage": trace_data.get("token_usage", {}),
            "tools_used": trace_data.get("tools_used", []),
            "handoff_target": trace_data.get("handoff_target"),
            "error": trace_data.get("error"),
        })
        
        # Add RL-specific signals
        if "signals" in trace_data:
            arc_trace["rl_signals"] = trace_data["signals"]
        
        return arc_trace

class ArcTraceProcessor:
    """
    Custom trace processor for OpenAI Agents SDK.
    
    This processor receives trace data from the OpenAI Agents SDK
    built-in tracing system and forwards it to Arc platform.
    """
    
    def __init__(self, integration: OpenAIAgentsIntegration):
        self.integration = integration
    
    def process_trace(self, trace: Dict[str, Any]) -> None:
        """
        Process a trace from OpenAI Agents SDK.
        
        Args:
            trace: Trace data from OpenAI Agents SDK
        """
        try:
            # Convert OpenAI Agents trace format to Arc format
            arc_trace = self._convert_agents_trace(trace)
            
            # Send to Arc platform
            self.integration.send_to_arc(arc_trace)
            
        except Exception as e:
            logger.error(f"Error processing OpenAI Agents trace: {e}")
    
    def process_span(self, span: Dict[str, Any]) -> None:
        """
        Process a span from OpenAI Agents SDK.
        
        Args:
            span: Span data from OpenAI Agents SDK
        """
        try:
            # Convert span to Arc format
            arc_trace = self._convert_agents_span(span)
            
            # Send to Arc platform
            self.integration.send_to_arc(arc_trace)
            
        except Exception as e:
            logger.error(f"Error processing OpenAI Agents span: {e}")
    
    def _convert_agents_trace(self, trace: Dict[str, Any]) -> Dict[str, Any]:
        """Convert OpenAI Agents trace to Arc format."""
        return {
            "trace_id": trace.get("trace_id"),
            "operation_name": "agents.trace",
            "start_time": trace.get("start_time"),
            "end_time": trace.get("end_time"),
            "attributes": {
                "agents.trace.id": trace.get("trace_id"),
                "agents.trace.status": trace.get("status"),
                "agents.trace.duration_ms": trace.get("duration_ms"),
                "agents.trace.spans_count": len(trace.get("spans", [])),
            },
            "spans": [self._convert_agents_span(span) for span in trace.get("spans", [])],
            "metadata": trace.get("metadata", {}),
        }
    
    def _convert_agents_span(self, span: Dict[str, Any]) -> Dict[str, Any]:
        """Convert OpenAI Agents span to Arc format."""
        span_type = span.get("span_type", "unknown")
        
        arc_span = {
            "trace_id": span.get("trace_id"),
            "span_id": span.get("span_id"),
            "parent_span_id": span.get("parent_span_id"),
            "operation_name": f"agents.{span_type}",
            "start_time": span.get("start_time"),
            "end_time": span.get("end_time"),
            "attributes": {
                "agents.span.type": span_type,
                "agents.span.name": span.get("name"),
                "agents.span.status": span.get("status"),
            }
        }
        
        # Add type-specific attributes
        if span_type == "agent_run":
            arc_span["attributes"].update({
                "agents.agent.name": span.get("agent_name"),
                "agents.agent.instructions": span.get("agent_instructions", "")[:500],  # Truncate
                "agents.agent.input": span.get("input", "")[:1000],  # Truncate
                "agents.agent.output": span.get("output", "")[:1000],  # Truncate
                "agents.agent.tools_count": len(span.get("tools", [])),
            })
            
        elif span_type == "tool_call":
            arc_span["attributes"].update({
                "agents.tool.name": span.get("tool_name"),
                "agents.tool.input": span.get("tool_input", "")[:500],  # Truncate
                "agents.tool.output": span.get("tool_output", "")[:500],  # Truncate
                "agents.tool.duration_ms": span.get("duration_ms"),
            })
            
        elif span_type == "handoff":
            arc_span["attributes"].update({
                "agents.handoff.from_agent": span.get("from_agent"),
                "agents.handoff.to_agent": span.get("to_agent"),
                "agents.handoff.reason": span.get("reason", "")[:200],  # Truncate
            })
            
        elif span_type == "llm_generation":
            arc_span["attributes"].update({
                "agents.llm.model": span.get("model"),
                "agents.llm.prompt_tokens": span.get("prompt_tokens"),
                "agents.llm.completion_tokens": span.get("completion_tokens"),
                "agents.llm.total_tokens": span.get("total_tokens"),
                "agents.llm.response": span.get("response", "")[:1000],  # Truncate
            })
        
        # Add custom events and metadata
        if span.get("events"):
            arc_span["events"] = span["events"]
        if span.get("metadata"):
            arc_span["metadata"] = span["metadata"]
            
        return arc_span

# Convenience function for easy enablement
def enable_openai_agents_tracing() -> bool:
    """
    Enable OpenAI Agents SDK integration with Arc tracing.
    
    Returns:
        True if integration was successfully enabled, False otherwise.
    """
    integration = OpenAIAgentsIntegration()
    return integration.enable()