"""LlamaIndex integration for Arc Tracing SDK."""

import logging
import importlib.util
from typing import Any, Dict, List, Optional, Tuple
from arc_tracing.integrations.base import BaseIntegration

logger = logging.getLogger("arc_tracing")

class LlamaIndexIntegration(BaseIntegration):
    """
    Integration adapter for LlamaIndex with existing observability systems.
    
    This integration leverages LlamaIndex's built-in observability infrastructure
    by registering Arc as an additional observability handler. LlamaIndex supports
    multiple observability backends including:
    
    - Langfuse (real-time observability)
    - MLflow (production-ready tracing)  
    - Arize Phoenix (full-stack observability)
    - Traceloop/OpenLLMetry (OpenTelemetry-based)
    
    We integrate with this existing system rather than replacing it.
    """
    
    def __init__(self):
        super().__init__("llamaindex")
        self._original_handler = None
        self._arc_handler = None
    
    def is_available(self) -> bool:
        """Check if LlamaIndex is available."""
        try:
            import llama_index
            return True
        except ImportError:
            return False
    
    def _setup_integration(self) -> bool:
        """Set up integration with LlamaIndex observability system."""
        try:
            # Try to use the new instrumentation system (v0.10.20+)
            return self._setup_instrumentation_integration()
            
        except Exception as e:
            logger.error(f"Failed to setup LlamaIndex integration: {e}")
            return False
    
    def _setup_instrumentation_integration(self) -> bool:
        """Set up integration using LlamaIndex instrumentation system."""
        try:
            from llama_index.core.instrumentation import get_dispatcher
            from llama_index.core.instrumentation.events import BaseEvent
            
            # Get the global event dispatcher
            dispatcher = get_dispatcher()
            
            # Create our Arc event handler
            self._arc_handler = ArcEventHandler(self)
            
            # Register our handler with the dispatcher
            dispatcher.add_event_handler(self._arc_handler)
            
            logger.info("Successfully integrated with LlamaIndex instrumentation system")
            return True
            
        except ImportError:
            # Fall back to global handler approach
            return self._setup_global_handler_integration()
        except Exception as e:
            logger.error(f"Error setting up instrumentation integration: {e}")
            return False
    
    def _setup_global_handler_integration(self) -> bool:
        """Set up integration using global handler system (legacy).""" 
        try:
            from llama_index.core import Settings
            from llama_index.core.callbacks import CallbackManager
            
            # Create Arc callback handler
            arc_callback = ArcCallbackHandler(self)
            
            # Add to global callback manager
            if Settings.callback_manager is None:
                Settings.callback_manager = CallbackManager()
            
            Settings.callback_manager.add_handler(arc_callback)
            self._arc_handler = arc_callback
            
            logger.info("Successfully integrated with LlamaIndex global callback system")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up global handler integration: {e}")
            return False
    
    def _teardown_integration(self) -> None:
        """Clean up the integration."""
        try:
            if self._arc_handler:
                # Try to remove from instrumentation system
                try:
                    from llama_index.core.instrumentation import get_dispatcher
                    dispatcher = get_dispatcher()
                    dispatcher.remove_event_handler(self._arc_handler)
                except ImportError:
                    # Try to remove from global callback manager
                    try:
                        from llama_index.core import Settings
                        if Settings.callback_manager:
                            Settings.callback_manager.remove_handler(self._arc_handler)
                    except Exception:
                        pass
                        
        except Exception as e:
            logger.error(f"Error during LlamaIndex integration teardown: {e}")
    
    def extract_system_prompt(self, trace_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
        """
        Extract system prompt from LlamaIndex trace data.
        
        Based on 2025 LlamaIndex documentation, system prompts can be found in:
        - AgentWorkflow configurations with system_prompt parameter
        - RichPromptTemplate with jinja-style {% chat role="system" %} blocks
        - FunctionAgent and ReActAgent configurations
        - Service context and prompt templates
        
        Args:
            trace_data: LlamaIndex trace data
            
        Returns:
            Tuple of (prompt_text, template_variables, prompt_source) or None if no prompt found
        """
        try:
            prompt_text = None
            template_vars = None
            
            # Method 1: Extract from AgentWorkflow configurations (2025 feature)
            if trace_data.get("component_type") == "workflow":
                workflow_config = trace_data.get("workflow_config", {})
                if isinstance(workflow_config, dict):
                    # Check for system_prompt in workflow configuration
                    prompt_text = workflow_config.get("system_prompt")
                    template_vars = workflow_config.get("template_vars")
                    
                    # Check agents within workflow
                    if not prompt_text:
                        agents = workflow_config.get("agents", [])
                        for agent in agents:
                            if isinstance(agent, dict):
                                agent_prompt = agent.get("system_prompt")
                                if agent_prompt:
                                    prompt_text = agent_prompt
                                    template_vars = agent.get("template_vars")
                                    break
                                    
            # Method 2: Extract from Agent configurations (FunctionAgent, ReActAgent)
            elif trace_data.get("agent_type") in ["FunctionAgent", "ReActAgent", "QueryEngineAgent"]:
                agent_config = trace_data.get("agent_config", {})
                if isinstance(agent_config, dict):
                    prompt_text = (
                        agent_config.get("system_prompt") or
                        agent_config.get("system_message") or
                        agent_config.get("instructions")
                    )
                    template_vars = agent_config.get("template_vars")
                    
            # Method 3: Extract from RichPromptTemplate with jinja syntax
            elif "prompt_template" in trace_data:
                template_data = trace_data.get("prompt_template", {})
                if isinstance(template_data, dict):
                    template_str = template_data.get("template")
                    if template_str and isinstance(template_str, str):
                        # Parse jinja-style system role blocks
                        import re
                        system_pattern = r'{% chat role="system" %}(.*?){% endchat %}'
                        system_match = re.search(system_pattern, template_str, re.DOTALL)
                        if system_match:
                            prompt_text = system_match.group(1).strip()
                            template_vars = template_data.get("template_vars")
                        else:
                            # Fallback: check for direct system_prompt in template
                            prompt_text = template_data.get("system_prompt")
                            
            # Method 4: Extract from query engine or service context
            elif "service_context" in trace_data:
                service_context = trace_data.get("service_context", {})
                if isinstance(service_context, dict):
                    # Check prompt helper or prompt templates in service context
                    prompt_helper = service_context.get("prompt_helper", {})
                    if isinstance(prompt_helper, dict):
                        prompt_text = (
                            prompt_helper.get("system_prompt") or
                            prompt_helper.get("qa_template", {}).get("system_prompt") or
                            prompt_helper.get("refine_template", {}).get("system_prompt")
                        )
                        
            # Method 5: Extract from LLM calls and messages
            elif "llm_calls" in trace_data:
                llm_calls = trace_data.get("llm_calls", [])
                for call in llm_calls:
                    if isinstance(call, dict):
                        messages = call.get("messages", [])
                        if messages and isinstance(messages, list):
                            for message in messages:
                                if isinstance(message, dict) and message.get("role") == "system":
                                    prompt_text = message.get("content")
                                    break
                        if prompt_text:
                            break
                            
            # Method 6: Extract from trace attributes and metadata
            if not prompt_text:
                # Check trace attributes
                attributes = trace_data.get("attributes", {})
                prompt_text = (
                    attributes.get("llamaindex.system_prompt") or
                    attributes.get("llamaindex.agent.system_prompt") or
                    attributes.get("llamaindex.prompt") or
                    attributes.get("system_message")
                )
                
                # Check metadata
                if not prompt_text:
                    metadata = trace_data.get("metadata", {})
                    prompt_text = (
                        metadata.get("system_prompt") or
                        metadata.get("agent_instructions") or
                        metadata.get("prompt_template")
                    )
                    template_vars = metadata.get("template_variables")
                    
            # Method 7: Extract from workflow state (AgentWorkflow)
            if not prompt_text and "workflow_state" in trace_data:
                workflow_state = trace_data.get("workflow_state", {})
                if isinstance(workflow_state, dict):
                    # Check for system prompts in workflow state
                    prompt_text = (
                        workflow_state.get("system_prompt") or
                        workflow_state.get("agent_prompt") or
                        workflow_state.get("instructions")
                    )
                    
                    # Check for agent configurations in state
                    if not prompt_text:
                        current_agent = workflow_state.get("current_agent", {})
                        if isinstance(current_agent, dict):
                            prompt_text = current_agent.get("system_prompt")
                            template_vars = current_agent.get("template_vars")
                            
            # Method 8: Extract from response synthesis and retrieval context
            if not prompt_text and "retrieval_results" in trace_data:
                # Sometimes system prompts are preserved in synthesis templates
                synthesis_config = trace_data.get("synthesis_config", {})
                if isinstance(synthesis_config, dict):
                    prompt_text = (
                        synthesis_config.get("qa_prompt") or
                        synthesis_config.get("system_prompt") or
                        synthesis_config.get("synthesis_prompt")
                    )
                    
            if prompt_text and isinstance(prompt_text, str) and prompt_text.strip():
                return (prompt_text.strip(), template_vars, "llamaindex")
                
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting system prompt from LlamaIndex trace: {e}")
            return None
    
    def format_trace_for_arc(self, trace_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert LlamaIndex trace data to Arc format."""
        arc_trace = super().format_trace_for_arc(trace_data)
        
        # Add LlamaIndex specific attributes
        arc_trace.update({
            "component_type": trace_data.get("component_type"),  # "workflow", "agent", "query_engine"
            "workflow_name": trace_data.get("workflow_name"),
            "agent_type": trace_data.get("agent_type"),  # "FunctionAgent", "ReActAgent"
            "query": trace_data.get("query"),
            "response": trace_data.get("response"),
            "tools_used": trace_data.get("tools_used", []),
            "retrieval_results": trace_data.get("retrieval_results", []),
            "llm_calls": trace_data.get("llm_calls", []),
            "workflow_state": trace_data.get("workflow_state", {}),
            "error": trace_data.get("error"),
        })
        
        # Add observability backend information if available
        if "langfuse_trace_id" in trace_data:
            arc_trace["langfuse_integration"] = {
                "trace_id": trace_data["langfuse_trace_id"],
                "trace_url": trace_data.get("langfuse_trace_url"),
            }
        
        if "mlflow_run_id" in trace_data:
            arc_trace["mlflow_integration"] = {
                "run_id": trace_data["mlflow_run_id"],
                "experiment_id": trace_data.get("mlflow_experiment_id"),
            }
        
        return arc_trace

class ArcEventHandler:
    """
    Event handler for LlamaIndex instrumentation system.
    
    This handler receives events from LlamaIndex's instrumentation
    system and forwards relevant data to Arc platform.
    """
    
    def __init__(self, integration: LlamaIndexIntegration):
        self.integration = integration
    
    def handle(self, event: Any) -> None:
        """
        Handle an event from LlamaIndex instrumentation.
        
        Args:
            event: Event from LlamaIndex instrumentation system
        """
        try:
            # Convert event to Arc trace format
            arc_data = self._convert_event(event)
            
            if arc_data:
                # Send to Arc platform
                self.integration.send_to_arc(arc_data)
                
        except Exception as e:
            logger.error(f"Error handling LlamaIndex event: {e}")
    
    def _convert_event(self, event: Any) -> Optional[Dict[str, Any]]:
        """Convert LlamaIndex event to Arc trace format."""
        try:
            event_type = type(event).__name__
            
            # Base event data
            arc_data = {
                "trace_id": getattr(event, "trace_id", f"llamaindex_{id(event)}"),
                "operation_name": f"llamaindex.{event_type}",
                "event_type": event_type,
                "timestamp": getattr(event, "timestamp", None),
            }
            
            # Add event-specific data based on type
            if hasattr(event, "workflow_id"):
                arc_data.update({
                    "component_type": "workflow",
                    "workflow_name": getattr(event, "workflow_name", "unknown"),
                    "workflow_state": getattr(event, "state", {}),
                })
            
            elif hasattr(event, "agent_id"):
                arc_data.update({
                    "component_type": "agent", 
                    "agent_type": getattr(event, "agent_type", "unknown"),
                    "agent_name": getattr(event, "agent_name", "unknown"),
                    "tools_used": getattr(event, "tools", []),
                })
            
            elif hasattr(event, "query"):
                arc_data.update({
                    "component_type": "query_engine",
                    "query": getattr(event, "query", ""),
                    "response": getattr(event, "response", ""),
                })
            
            elif hasattr(event, "tool_name"):
                arc_data.update({
                    "component_type": "tool",
                    "tool_name": getattr(event, "tool_name", ""),
                    "tool_input": getattr(event, "input", ""),
                    "tool_output": getattr(event, "output", ""),
                })
            
            return arc_data
            
        except Exception as e:
            logger.error(f"Error converting LlamaIndex event: {e}")
            return None

class ArcCallbackHandler:
    """
    Callback handler for LlamaIndex global callback system.
    
    This handler integrates with LlamaIndex's callback system
    to capture trace data and send it to Arc platform.
    """
    
    def __init__(self, integration: LlamaIndexIntegration):
        self.integration = integration
        self.active_traces = {}
    
    def on_event_start(self, event_type: str, payload: Dict[str, Any], **kwargs) -> str:
        """Called when an event starts."""
        try:
            trace_id = f"llamaindex_{event_type}_{id(payload)}"
            
            trace_data = {
                "trace_id": trace_id,
                "operation_name": f"llamaindex.{event_type}",
                "event_type": event_type,
                "start_time": self._get_timestamp(),
                "payload": payload,
            }
            
            self.active_traces[trace_id] = trace_data
            return trace_id
            
        except Exception as e:
            logger.error(f"Error in callback start: {e}")
            return ""
    
    def on_event_end(self, event_type: str, payload: Dict[str, Any], trace_id: str = None, **kwargs) -> None:
        """Called when an event ends."""
        try:
            if trace_id and trace_id in self.active_traces:
                trace_data = self.active_traces[trace_id]
                trace_data.update({
                    "end_time": self._get_timestamp(),
                    "final_payload": payload,
                })
                
                # Send completed trace to Arc
                self.integration.send_to_arc(trace_data)
                
                # Clean up
                del self.active_traces[trace_id]
                
        except Exception as e:
            logger.error(f"Error in callback end: {e}")
    
    def _get_timestamp(self) -> int:
        """Get current timestamp in nanoseconds."""
        import time
        return int(time.time() * 1_000_000_000)

# Convenience function for easy enablement
def enable_llamaindex_tracing() -> bool:
    """
    Enable LlamaIndex integration with Arc tracing.
    
    Returns:
        True if integration was successfully enabled, False otherwise.
    """
    integration = LlamaIndexIntegration()
    return integration.enable()