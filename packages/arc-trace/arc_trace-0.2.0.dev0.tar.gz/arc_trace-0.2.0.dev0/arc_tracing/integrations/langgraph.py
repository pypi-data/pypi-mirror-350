"""LangGraph integration for Arc Tracing SDK."""

import logging
import importlib.util
import os
from typing import Any, Dict, List, Optional, Tuple
from arc_tracing.integrations.base import BaseIntegration

logger = logging.getLogger("arc_tracing")

class LangGraphIntegration(BaseIntegration):
    """
    Integration adapter for LangGraph with LangSmith observability.
    
    This integration extends LangSmith's built-in tracing system to send
    additional trace data to Arc platform. LangGraph provides seamless
    integration with LangSmith for observability of state graphs.
    
    LangSmith provides:
    - State graph execution tracing
    - Node-level execution visibility  
    - Edge transition tracking
    - Real-time monitoring and debugging
    
    We extend this by adding Arc-specific metadata and signals.
    """
    
    def __init__(self):
        super().__init__("langgraph") 
        self._langsmith_enabled = False
        self._arc_callback = None
    
    def is_available(self) -> bool:
        """Check if LangGraph and LangSmith are available."""
        try:
            import langgraph
            import langsmith
            return True
        except ImportError:
            return False
    
    def _setup_integration(self) -> bool:
        """Set up integration with LangGraph and LangSmith."""
        try:
            # Check if LangSmith tracing is already enabled
            langsmith_tracing = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
            langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
            
            if not langsmith_tracing or not langsmith_api_key:
                logger.info("LangSmith tracing not enabled. Enabling basic LangGraph integration.")
                return self._setup_basic_integration()
            else:
                logger.info("LangSmith tracing detected. Setting up enhanced integration.")
                return self._setup_langsmith_integration()
                
        except Exception as e:
            logger.error(f"Failed to setup LangGraph integration: {e}")
            return False
    
    def _setup_langsmith_integration(self) -> bool:
        """Set up integration when LangSmith is available."""
        try:
            from langsmith import Client
            from langsmith.run_helpers import traceable
            
            # Create LangSmith client
            client = Client()
            
            # Create Arc callback for LangSmith runs
            self._arc_callback = ArcLangSmithCallback(self)
            
            # Hook into LangSmith's run lifecycle
            # This allows us to receive trace data from LangSmith
            client.add_run_callback(self._arc_callback)
            
            self._langsmith_enabled = True
            logger.info("Successfully integrated with LangSmith tracing")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup LangSmith integration: {e}")
            return self._setup_basic_integration()
    
    def _setup_basic_integration(self) -> bool:
        """Set up basic integration without LangSmith."""
        try:
            # For basic integration, we use OpenTelemetry instrumentation
            from opentelemetry import trace
            from opentelemetry.instrumentation.auto_instrumentation import sitecustomize
            
            # Get current tracer
            tracer = trace.get_tracer("arc_tracing.langgraph")
            
            # We'll instrument key LangGraph methods manually
            self._instrument_langgraph_classes()
            
            logger.info("Successfully set up basic LangGraph integration")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup basic LangGraph integration: {e}")
            return False
    
    def _instrument_langgraph_classes(self) -> None:
        """Instrument key LangGraph classes for tracing."""
        try:
            from langgraph.graph import StateGraph
            from langgraph.pregel import Pregel
            
            # Instrument StateGraph compilation
            if hasattr(StateGraph, 'compile') and not hasattr(StateGraph.compile, '_arc_instrumented'):
                original_compile = StateGraph.compile
                
                def traced_compile(self, *args, **kwargs):
                    result = original_compile(self, *args, **kwargs)
                    
                    # Send compilation trace to Arc
                    self._send_compilation_trace(self, result)
                    
                    return result
                
                StateGraph.compile = traced_compile
                StateGraph.compile._arc_instrumented = True
                
            # Instrument Pregel execution methods
            for method_name in ['invoke', 'stream', 'astream', 'ainvoke']:
                if hasattr(Pregel, method_name):
                    self._instrument_pregel_method(Pregel, method_name)
                    
        except Exception as e:
            logger.error(f"Error instrumenting LangGraph classes: {e}")
    
    def _instrument_pregel_method(self, pregel_class: Any, method_name: str) -> None:
        """Instrument a specific Pregel method."""
        original_method = getattr(pregel_class, method_name)
        
        if hasattr(original_method, '_arc_instrumented'):
            return
            
        def traced_method(self, *args, **kwargs):
            # Start trace
            trace_data = {
                "trace_id": f"langgraph_{id(self)}_{method_name}",
                "operation_name": f"langgraph.{method_name}",
                "method": method_name,
                "input_state": args[0] if args and isinstance(args[0], dict) else {},
                "start_time": self._get_timestamp(),
            }
            
            try:
                result = original_method(self, *args, **kwargs)
                
                trace_data.update({
                    "end_time": self._get_timestamp(),
                    "output_state": result if isinstance(result, dict) else {},
                    "status": "success"
                })
                
                return result
                
            except Exception as e:
                trace_data.update({
                    "end_time": self._get_timestamp(),
                    "status": "error",
                    "error": str(e)
                })
                raise
                
            finally:
                # Send trace to Arc
                self.send_to_arc(trace_data)
        
        setattr(pregel_class, method_name, traced_method)
        getattr(pregel_class, method_name)._arc_instrumented = True
    
    def _teardown_integration(self) -> None:
        """Clean up the integration."""
        try:
            if self._langsmith_enabled and self._arc_callback:
                from langsmith import Client
                client = Client()
                client.remove_run_callback(self._arc_callback)
                
        except Exception as e:
            logger.error(f"Error during LangGraph integration teardown: {e}")
    
    def extract_system_prompt(self, trace_data: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, Any]], str]]:
        """
        Extract system prompt from LangGraph trace data.
        
        Args:
            trace_data: LangGraph trace data
            
        Returns:
            Tuple of (prompt_text, template_variables, prompt_source) or None if no prompt found
        """
        try:
            prompt_text = None
            template_vars = None
            
            # Method 1: Extract from LangSmith run data (when LangSmith integration is active)
            if "langsmith_run_id" in trace_data:
                # Check run inputs for chat prompts or system messages
                inputs = trace_data.get("inputs", {})
                if isinstance(inputs, dict):
                    # Look for system prompts in various input formats
                    prompt_text = (
                        inputs.get("system_prompt") or
                        inputs.get("system_message") or
                        inputs.get("instructions")
                    )
                    
                    # Check for messages array (ChatPrompt format)
                    messages = inputs.get("messages", [])
                    if not prompt_text and messages and isinstance(messages, list):
                        for message in messages:
                            if isinstance(message, dict) and message.get("role") == "system":
                                prompt_text = message.get("content")
                                break
                                
                # Check run metadata for prompt templates
                if not prompt_text:
                    metadata = trace_data.get("metadata", {})
                    prompt_text = (
                        metadata.get("system_prompt") or
                        metadata.get("prompt_template") or
                        metadata.get("chat_template")
                    )
                    template_vars = metadata.get("template_variables")
                    
            # Method 2: Extract from graph node configurations
            elif "graph_nodes" in trace_data:
                graph_nodes = trace_data.get("graph_nodes", [])
                for node_name in graph_nodes:
                    node_config = trace_data.get(f"node_config_{node_name}", {})
                    if isinstance(node_config, dict):
                        # Check for prompt configurations in nodes
                        node_prompt = (
                            node_config.get("system_prompt") or
                            node_config.get("prompt") or
                            node_config.get("instructions")
                        )
                        if node_prompt:
                            prompt_text = node_prompt
                            template_vars = node_config.get("template_vars")
                            break
                            
            # Method 3: Extract from state graph execution data
            elif "input_state" in trace_data or "output_state" in trace_data:
                # Check input state for system prompts
                input_state = trace_data.get("input_state", {})
                if isinstance(input_state, dict):
                    prompt_text = (
                        input_state.get("system_prompt") or
                        input_state.get("system_message") or
                        input_state.get("instructions")
                    )
                    
                    # Check for messages in state
                    if not prompt_text:
                        messages = input_state.get("messages", [])
                        if messages and isinstance(messages, list):
                            for message in messages:
                                if isinstance(message, dict) and message.get("role") == "system":
                                    prompt_text = message.get("content")
                                    break
                                    
            # Method 4: Extract from execution path and state transitions
            elif "execution_path" in trace_data:
                execution_path = trace_data.get("execution_path", [])
                for step in execution_path:
                    if isinstance(step, dict):
                        step_data = step.get("data", {})
                        if isinstance(step_data, dict):
                            step_prompt = (
                                step_data.get("system_prompt") or
                                step_data.get("prompt") or
                                step_data.get("instructions")
                            )
                            if step_prompt:
                                prompt_text = step_prompt
                                template_vars = step_data.get("template_vars")
                                break
                                
            # Method 5: Extract from trace attributes (basic integration)
            if not prompt_text and "attributes" in trace_data:
                attributes = trace_data["attributes"]
                prompt_text = (
                    attributes.get("langgraph.system_prompt") or
                    attributes.get("langgraph.prompt") or
                    attributes.get("langgraph.instructions") or
                    attributes.get("system_message")
                )
                
            # Method 6: Extract from LangSmith run outputs (for chat completion nodes)
            if not prompt_text and "outputs" in trace_data:
                outputs = trace_data.get("outputs", {})
                if isinstance(outputs, dict):
                    # Sometimes system prompts are preserved in outputs for analysis
                    prompt_text = (
                        outputs.get("system_prompt") or
                        outputs.get("original_prompt") or
                        outputs.get("prompt_template")
                    )
                    
            if prompt_text and isinstance(prompt_text, str) and prompt_text.strip():
                return (prompt_text.strip(), template_vars, "langgraph")
                
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting system prompt from LangGraph trace: {e}")
            return None
    
    def _get_timestamp(self) -> int:
        """Get current timestamp in nanoseconds."""
        import time
        return int(time.time() * 1_000_000_000)
    
    def _send_compilation_trace(self, graph: Any, compiled_graph: Any) -> None:
        """Send graph compilation trace to Arc."""
        try:
            trace_data = {
                "trace_id": f"langgraph_compile_{id(graph)}",
                "operation_name": "langgraph.compile",
                "graph_nodes": list(graph.nodes.keys()) if hasattr(graph, 'nodes') else [],
                "graph_edges": len(graph.edges) if hasattr(graph, 'edges') else 0,
                "compilation_time": self._get_timestamp(),
            }
            
            self.send_to_arc(trace_data)
            
        except Exception as e:
            logger.error(f"Error sending compilation trace: {e}")
    
    def format_trace_for_arc(self, trace_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert LangGraph trace data to Arc format."""
        arc_trace = super().format_trace_for_arc(trace_data)
        
        # Add LangGraph specific attributes
        arc_trace.update({
            "graph_type": trace_data.get("graph_type", "state_graph"),
            "execution_method": trace_data.get("method"),
            "node_count": len(trace_data.get("graph_nodes", [])),
            "edge_count": trace_data.get("graph_edges", 0),
            "input_state": trace_data.get("input_state", {}),
            "output_state": trace_data.get("output_state", {}),
            "state_transitions": trace_data.get("state_transitions", []),
            "execution_path": trace_data.get("execution_path", []),
            "error": trace_data.get("error"),
        })
        
        # Add LangSmith run data if available
        if "langsmith_run_id" in trace_data:
            arc_trace["langsmith_integration"] = {
                "run_id": trace_data["langsmith_run_id"],
                "run_url": trace_data.get("langsmith_run_url"),
                "project_name": trace_data.get("langsmith_project"),
            }
        
        return arc_trace

class ArcLangSmithCallback:
    """
    Callback for LangSmith runs that sends data to Arc platform.
    """
    
    def __init__(self, integration: LangGraphIntegration):
        self.integration = integration
    
    def on_run_start(self, run_id: str, run_data: Dict[str, Any]) -> None:
        """Called when a LangSmith run starts."""
        try:
            # Extract relevant data for Arc
            arc_data = {
                "trace_id": run_id,
                "operation_name": f"langsmith.{run_data.get('run_type', 'run')}",
                "start_time": run_data.get("start_time"),
                "langsmith_run_id": run_id,
                "langsmith_project": run_data.get("session_name"),
                "run_type": run_data.get("run_type"),
                "inputs": run_data.get("inputs", {}),
            }
            
            # Send start event to Arc
            self.integration.send_to_arc(arc_data)
            
        except Exception as e:
            logger.error(f"Error in LangSmith run start callback: {e}")
    
    def on_run_end(self, run_id: str, run_data: Dict[str, Any]) -> None:
        """Called when a LangSmith run ends."""
        try:
            # Extract final run data for Arc
            arc_data = {
                "trace_id": run_id,
                "operation_name": f"langsmith.{run_data.get('run_type', 'run')}.end",
                "end_time": run_data.get("end_time"),
                "duration_ms": run_data.get("duration_ms"),
                "langsmith_run_id": run_id,
                "langsmith_run_url": run_data.get("run_url"),
                "outputs": run_data.get("outputs", {}),
                "error": run_data.get("error"),
                "status": "success" if not run_data.get("error") else "error",
            }
            
            # Send completion event to Arc
            self.integration.send_to_arc(arc_data)
            
        except Exception as e:
            logger.error(f"Error in LangSmith run end callback: {e}")

# Convenience function for easy enablement
def enable_langgraph_tracing() -> bool:
    """
    Enable LangGraph integration with Arc tracing.
    
    Returns:
        True if integration was successfully enabled, False otherwise.
    """
    integration = LangGraphIntegration()
    return integration.enable()