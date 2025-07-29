"""Tests for the core tracing functionality."""

import os
import unittest
from unittest.mock import patch, MagicMock
import pytest

from arc_tracing.trace import trace_agent

class TestTraceAgent:
    """Tests for the trace_agent decorator."""
    
    def test_trace_agent_basic(self):
        """Test basic functionality of trace_agent decorator."""
        # Define a simple function to trace
        @trace_agent
        def test_function(arg1, arg2=None):
            """Test function."""
            return f"{arg1}-{arg2}"
        
        # Call the traced function
        result = test_function("hello", arg2="world")
        
        # Verify result is correct
        assert result == "hello-world"
    
    def test_trace_agent_with_exception(self):
        """Test that exceptions are properly handled and re-raised."""
        # Define a function that raises an exception
        @trace_agent
        def failing_function():
            """Function that raises an exception."""
            raise ValueError("Test error")
        
        # Verify the exception is re-raised
        with pytest.raises(ValueError) as excinfo:
            failing_function()
        
        assert "Test error" in str(excinfo.value)
    
    @patch("arc_tracing.trace.tracer")
    def test_trace_agent_creates_span(self, mock_tracer):
        """Test that a span is created with the correct name and attributes."""
        # Set up mock
        mock_span = MagicMock()
        mock_context = MagicMock()
        mock_tracer.start_as_current_span.return_value.__enter__.return_value = mock_span
        
        # Define a simple function to trace
        @trace_agent
        def test_function(arg1, arg2=None):
            """Test function."""
            return f"{arg1}-{arg2}"
        
        # Call the traced function
        result = test_function("hello", arg2="world")
        
        # Verify span was created with correct name
        mock_tracer.start_as_current_span.assert_called_once()
        call_args = mock_tracer.start_as_current_span.call_args[0]
        assert call_args[0] == "agent.test_function"
        
        # Verify span has correct attributes
        attributes = mock_tracer.start_as_current_span.call_args[1]["attributes"]
        assert attributes["arc_tracing.agent.name"] == "test_function"
        assert "arc_tracing.agent.frameworks" in attributes
        
        # Verify result attribute was set
        mock_span.set_attribute.assert_any_call("arc_tracing.agent.result", "hello-world")
    
    def test_trace_agent_frameworks_detection(self):
        """Test that frameworks are detected and recorded."""
        # We need to directly patch the specific import in the module where it's used
        with patch("arc_tracing.trace.detect_frameworks") as mock_detect_frameworks:
            with patch("arc_tracing.trace.tracer") as mock_tracer:
                # Set up mocks
                mock_span = MagicMock()
                mock_tracer.start_as_current_span.return_value.__enter__.return_value = mock_span
                mock_detect_frameworks.return_value = ["openai", "langchain"]
                
                # Define a simple function to trace
                @trace_agent
                def test_function():
                    """Test function."""
                    return "result"
                
                # Call the traced function
                result = test_function()
                
                # Verify frameworks were detected
                mock_detect_frameworks.assert_called_once()
                
                # Verify frameworks were recorded in span attributes
                attributes = mock_tracer.start_as_current_span.call_args[1]["attributes"]
                assert attributes["arc_tracing.agent.frameworks"] == "openai,langchain"