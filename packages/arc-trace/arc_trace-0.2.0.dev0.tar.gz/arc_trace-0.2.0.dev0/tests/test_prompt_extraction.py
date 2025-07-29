"""Tests for framework-specific prompt extraction functionality."""

import pytest
from typing import Dict, Any, Optional, Tuple
from unittest.mock import Mock, patch

from arc_tracing.integrations.openai_agents import OpenAIAgentsIntegration
from arc_tracing.integrations.langgraph import LangGraphIntegration
from arc_tracing.integrations.llamaindex import LlamaIndexIntegration


class TestOpenAIAgentsPromptExtraction:
    """Test prompt extraction for OpenAI Agents SDK."""
    
    def setup_method(self):
        self.integration = OpenAIAgentsIntegration()
    
    def test_extract_from_agent_run_span(self):
        """Test extracting system prompt from agent_run span."""
        trace_data = {
            "span_type": "agent_run",
            "agent_instructions": "You are a helpful assistant that can analyze data.",
            "agent_name": "DataAnalyst"
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert prompt_text == "You are a helpful assistant that can analyze data."
        assert template_vars is None
        assert source == "openai_agents"
    
    def test_extract_from_agent_config(self):
        """Test extracting system prompt from agent configuration."""
        trace_data = {
            "agent_config": {
                "instructions": "You are a research assistant.",
                "template_vars": {"domain": "machine learning"}
            }
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert prompt_text == "You are a research assistant."
        assert template_vars == {"domain": "machine learning"}
        assert source == "openai_agents"
    
    def test_extract_from_llm_generation_messages(self):
        """Test extracting system prompt from LLM generation messages."""
        trace_data = {
            "span_type": "llm_generation",
            "messages": [
                {"role": "system", "content": "You are a code reviewer."},
                {"role": "user", "content": "Review this code..."}
            ]
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert prompt_text == "You are a code reviewer."
        assert template_vars is None
        assert source == "openai_agents"
    
    def test_extract_from_attributes(self):
        """Test extracting system prompt from trace attributes."""
        trace_data = {
            "attributes": {
                "agents.agent.instructions": "You are a writing assistant."
            }
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert prompt_text == "You are a writing assistant."
        assert source == "openai_agents"
    
    def test_no_prompt_found(self):
        """Test when no system prompt is found."""
        trace_data = {
            "span_type": "tool_call",
            "tool_name": "calculator"
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is None


class TestLangGraphPromptExtraction:
    """Test prompt extraction for LangGraph."""
    
    def setup_method(self):
        self.integration = LangGraphIntegration()
    
    def test_extract_from_langsmith_run_inputs(self):
        """Test extracting system prompt from LangSmith run inputs."""
        trace_data = {
            "langsmith_run_id": "run_123",
            "inputs": {
                "system_prompt": "You are a task planning assistant.",
                "query": "Plan a vacation"
            }
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert prompt_text == "You are a task planning assistant."
        assert source == "langgraph"
    
    def test_extract_from_messages_array(self):
        """Test extracting system prompt from messages array in inputs."""
        trace_data = {
            "langsmith_run_id": "run_456",
            "inputs": {
                "messages": [
                    {"role": "system", "content": "You are a customer service agent."},
                    {"role": "user", "content": "I need help with my order."}
                ]
            }
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert prompt_text == "You are a customer service agent."
        assert source == "langgraph"
    
    def test_extract_from_graph_node_config(self):
        """Test extracting system prompt from graph node configurations."""
        trace_data = {
            "graph_nodes": ["chat_node", "tool_node"],
            "node_config_chat_node": {
                "system_prompt": "You are an AI assistant with access to tools.",
                "template_vars": {"tools": ["calculator", "search"]}
            }
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert prompt_text == "You are an AI assistant with access to tools."
        assert template_vars == {"tools": ["calculator", "search"]}
        assert source == "langgraph"
    
    def test_extract_from_input_state(self):
        """Test extracting system prompt from input state."""
        trace_data = {
            "input_state": {
                "system_message": "You are a helpful chatbot.",
                "user_input": "Hello!"
            }
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert prompt_text == "You are a helpful chatbot."
        assert source == "langgraph"


class TestLlamaIndexPromptExtraction:
    """Test prompt extraction for LlamaIndex."""
    
    def setup_method(self):
        self.integration = LlamaIndexIntegration()
    
    def test_extract_from_agent_workflow_config(self):
        """Test extracting system prompt from AgentWorkflow configuration."""
        trace_data = {
            "component_type": "workflow",
            "workflow_config": {
                "system_prompt": "You are a research assistant with access to multiple tools.",
                "template_vars": {"max_tools": 5}
            }
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert prompt_text == "You are a research assistant with access to multiple tools."
        assert template_vars == {"max_tools": 5}
        assert source == "llamaindex"
    
    def test_extract_from_function_agent_config(self):
        """Test extracting system prompt from FunctionAgent configuration."""
        trace_data = {
            "agent_type": "FunctionAgent",
            "agent_config": {
                "system_prompt": "You are a function-calling agent.",
                "instructions": "Use tools to answer questions."
            }
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert prompt_text == "You are a function-calling agent."
        assert source == "llamaindex"
    
    def test_extract_from_rich_prompt_template_jinja(self):
        """Test extracting system prompt from RichPromptTemplate with jinja syntax."""
        trace_data = {
            "prompt_template": {
                "template": """
                {% chat role="system" %}
                You are a helpful assistant that answers questions about {{ context }}.
                {% endchat %}
                {% chat role="user" %}
                {{ query }}
                {% endchat %}
                """,
                "template_vars": {"context": "documents", "query": "What is AI?"}
            }
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert "You are a helpful assistant that answers questions about" in prompt_text
        assert template_vars == {"context": "documents", "query": "What is AI?"}
        assert source == "llamaindex"
    
    def test_extract_from_llm_calls_messages(self):
        """Test extracting system prompt from LLM calls messages."""
        trace_data = {
            "llm_calls": [
                {
                    "messages": [
                        {"role": "system", "content": "You are a query engine assistant."},
                        {"role": "user", "content": "Analyze this data"}
                    ]
                }
            ]
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert prompt_text == "You are a query engine assistant."
        assert source == "llamaindex"
    
    def test_extract_from_workflow_state(self):
        """Test extracting system prompt from workflow state."""
        trace_data = {
            "workflow_state": {
                "current_agent": {
                    "system_prompt": "You are an agent in a multi-agent workflow.",
                    "template_vars": {"agent_id": "agent_1"}
                }
            }
        }
        
        result = self.integration.extract_system_prompt(trace_data)
        assert result is not None
        prompt_text, template_vars, source = result
        assert prompt_text == "You are an agent in a multi-agent workflow."
        assert template_vars == {"agent_id": "agent_1"}
        assert source == "llamaindex"


class TestPromptExtractionIntegration:
    """Test integration of prompt extraction with base functionality."""
    
    def test_format_trace_includes_extracted_prompt(self):
        """Test that format_trace_for_arc includes extracted prompt data."""
        integration = OpenAIAgentsIntegration()
        
        trace_data = {
            "span_type": "agent_run",
            "agent_instructions": "You are a helpful assistant.",
            "trace_id": "test_trace_123",
            "operation_name": "agent.run"
        }
        
        # Mock config to enable prompt capture
        with patch.object(integration, 'config') as mock_config:
            mock_config.get.return_value = True  # capture_prompts = True
            mock_config.project_id = "test_project"
            mock_config.agent_id = "test_agent"
            
            # Mock sanitization
            with patch.object(integration, '_sanitize_prompt', return_value="You are a helpful assistant."):
                arc_trace = integration.format_trace_for_arc(trace_data)
        
        # Verify prompt data is included
        assert "system_prompt" in arc_trace
        assert arc_trace["system_prompt"] == "You are a helpful assistant."
        assert arc_trace["prompt_source"] == "openai_agents"
        assert arc_trace["prompt_extraction_method"] == "automatic"
        
        # Verify metadata includes prompt data for backend compatibility
        assert "system_prompt" in arc_trace["metadata"]
        assert arc_trace["metadata"]["system_prompt"] == "You are a helpful assistant."
        assert arc_trace["metadata"]["prompt_source"] == "openai_agents"
    
    def test_prompt_extraction_disabled(self):
        """Test that prompt extraction can be disabled via configuration."""
        integration = LangGraphIntegration()
        
        trace_data = {
            "langsmith_run_id": "run_123",
            "inputs": {"system_prompt": "You are a task planner."}
        }
        
        # Mock config to disable prompt capture
        with patch.object(integration, 'config') as mock_config:
            mock_config.get.return_value = False  # capture_prompts = False
            
            arc_trace = integration.format_trace_for_arc(trace_data)
        
        # Verify prompt data is not included
        assert "system_prompt" not in arc_trace
        assert "prompt_source" not in arc_trace
        assert "prompt_extraction_method" not in arc_trace


if __name__ == "__main__":
    pytest.main([__file__])