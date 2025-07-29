"""Tests for backend exporters functionality."""

import os
import unittest
from unittest.mock import patch, MagicMock
import json
import uuid
import pytest
import tempfile
import shutil

from arc_tracing.exporters.arc_exporter import ArcExporter
from arc_tracing.exporters.local_exporter import LocalFileExporter, BatchUploader
from arc_tracing.exporters.helper import format_trace_for_backend, is_valid_uuid


class TestHelperFunctions:
    """Tests for helper functions in the exporters module."""
    
    def test_is_valid_uuid(self):
        """Test UUID validation function."""
        # Valid UUID
        assert is_valid_uuid("123e4567-e89b-12d3-a456-426614174000") == True
        
        # Invalid UUIDs
        assert is_valid_uuid("not-a-uuid") == False
        assert is_valid_uuid("123") == False
        assert is_valid_uuid("") == False
        assert is_valid_uuid(None) == False
    
    def test_format_trace_for_backend_basic(self):
        """Test basic trace formatting."""
        # Simple spans with minimal attributes
        span1 = {
            "name": "test_span",
            "span_id": "abc123",
            "start_time": 1619712000000000000,
            "end_time": 1619712001000000000,
            "attributes": {
                "arc_tracing.agent.input": "test query",
                "arc_tracing.agent.result": "test response"
            }
        }
        
        spans = [span1]
        
        # Format the trace
        trace = format_trace_for_backend(spans)
        
        # Check basic structure
        assert "input" in trace
        assert "output" in trace
        assert "steps" in trace
        assert trace["input"]["content"] == "test query"
        assert trace["output"]["content"] == "test response"
    
    def test_format_trace_with_uuids(self):
        """Test trace formatting with project_id and agent_id."""
        # Simple span
        span = {
            "name": "test_span",
            "span_id": "abc123",
            "start_time": 1619712000000000000,
            "end_time": 1619712001000000000,
            "attributes": {}
        }
        
        # Use valid UUIDs
        project_id = "123e4567-e89b-12d3-a456-426614174000"
        agent_id = "123e4567-e89b-12d3-a456-426614174001"
        
        # Format with UUIDs
        trace = format_trace_for_backend([span], project_id=project_id, agent_id=agent_id)
        
        # Check UUID presence
        assert "project_id" in trace
        assert "agent_id" in trace
        assert trace["project_id"] == project_id
        assert trace["agent_id"] == agent_id
    
    def test_format_trace_with_hex_span_id(self):
        """Test trace formatting with hex span IDs."""
        # Span with hex format span_id (with 0x prefix)
        span = {
            "name": "test_span",
            "span_id": "0xabc123",
            "start_time": 1619712000000000000,
            "end_time": 1619712001000000000,
            "attributes": {}
        }
        
        # Format the trace
        trace = format_trace_for_backend([span])
        
        # Verify span_id has correct format (without 0x prefix)
        assert len(trace["steps"]) == 1
        assert trace["steps"][0]["step_id"] == "abc123"  # Prefix removed


class TestArcExporter:
    """Tests for ArcExporter functionality."""
    
    @patch('requests.Session.post')
    def test_arc_exporter_auth_methods(self, mock_post):
        """Test different authentication methods in ArcExporter."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Create mock span
        mock_span = MagicMock()
        mock_span.name = "test_span"
        mock_span.context.trace_id = 123456
        mock_span.context.span_id = 789012
        mock_span.context.is_remote = False
        mock_span.start_time = 1619712000000000000
        mock_span.end_time = 1619712001000000000
        mock_span.status.status_code.value = 0
        mock_span.status.description = ""
        mock_span.attributes = {}
        mock_span.events = []
        mock_span.links = []
        mock_span.parent = None
        
        spans = [mock_span]
        
        # Test header auth (default)
        with patch('arc_tracing.exporters.arc_exporter.format_trace_for_backend') as mock_format:
            # Mock the format_trace_for_backend to return a simple trace
            mock_format.return_value = {
                "input": {"content": "test", "type": "text"},
                "output": {"content": "test", "type": "text"},
                "steps": []
            }
            
            exporter = ArcExporter(
                endpoint="http://test.com/api",
                api_key="test_key",
                auth_method="header",
                auth_header_name="X-API-Key"
            )
            exporter.export(spans)
            
            # Verify mock_post was called
            assert mock_post.called
            
            # Check header was set correctly
            latest_call = mock_post.call_args
            headers = latest_call[1]['headers']
            assert 'X-API-Key' in headers
            assert headers['X-API-Key'] == "test_key"
            
            # Reset mock
            mock_post.reset_mock()
            
            # Test bearer auth
            exporter = ArcExporter(
                endpoint="http://test.com/api",
                api_key="test_key",
                auth_method="bearer",
                auth_header_name="X-API-Key"  # This is the default in ArcExporter
            )
            exporter.export(spans)
            
            # Verify mock_post was called
            assert mock_post.called
            
            # Check bearer token was set correctly with the default header name
            latest_call = mock_post.call_args
            headers = latest_call[1]['headers']
            assert 'X-API-Key' in headers
            assert headers['X-API-Key'] == "Bearer test_key"
            
            # Reset mock again
            mock_post.reset_mock()
            
            # Test bearer auth with custom Authorization header
            exporter = ArcExporter(
                endpoint="http://test.com/api",
                api_key="test_key",
                auth_method="bearer",
                auth_header_name="Authorization"
            )
            exporter.export(spans)
            
            # Check bearer token was set correctly with Authorization header
            latest_call = mock_post.call_args
            headers = latest_call[1]['headers']
            assert 'Authorization' in headers
            assert headers['Authorization'] == "Bearer test_key"


class TestLocalFileExporter:
    """Tests for LocalFileExporter functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test environment."""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)
    
    @patch('arc_tracing.exporters.local_exporter.LocalFileExporter._format_span')
    def test_local_file_export(self, mock_format_span):
        """Test basic file export functionality."""
        # Mock _format_span to return a simple dict that is JSON serializable
        mock_format_span.return_value = {
            "name": "test_span",
            "context": {
                "trace_id": "123456",
                "span_id": "789012",
                "is_remote": False
            },
            "start_time": 1619712000000000000,
            "end_time": 1619712001000000000,
            "attributes": {}
        }
        
        # Create exporter with test directory
        exporter = LocalFileExporter(export_dir=self.test_dir)
        
        # Create a ReadableSpan-like object
        class MockReadableSpan:
            name = "test_span"
            context = MagicMock()
            parent = None
            status = MagicMock()
            attributes = {}
            events = []
            links = []
            
            @property
            def start_time(self):
                return 1619712000000000000
                
            @property
            def end_time(self):
                return 1619712001000000000
        
        mock_span = MockReadableSpan()
        mock_span.context.trace_id = 123456
        mock_span.context.span_id = 789012
        mock_span.status.status_code.value = 0
        mock_span.status.description = ""
        
        # Export the span
        exporter.export([mock_span])
        
        # Check if a file was created
        files = os.listdir(self.test_dir)
        assert len(files) == 1
        assert files[0].endswith(".jsonl")
        
        # Check that _format_span was called with our mock span
        mock_format_span.assert_called_once()
        
        # Check file contents (should contain our mocked formatted span)
        with open(os.path.join(self.test_dir, files[0]), 'r') as f:
            content = f.read()
            assert "test_span" in content
            assert "123456" in content
            assert "789012" in content
    
    def test_batch_uploader_list_files(self):
        """Test BatchUploader's ability to list trace files."""
        # Create some test files in the test directory
        with open(os.path.join(self.test_dir, "trace1.jsonl"), 'w') as f:
            f.write('{"test": "data1"}\n')
        with open(os.path.join(self.test_dir, "trace2.jsonl"), 'w') as f:
            f.write('{"test": "data2"}\n')
        with open(os.path.join(self.test_dir, "not_a_trace.txt"), 'w') as f:
            f.write('not a trace file\n')
        
        # Create batch uploader using the test directory
        uploader = BatchUploader(export_dir=self.test_dir)
        
        # List trace files
        files = uploader.list_trace_files()
        
        # Verify only jsonl files are returned
        assert len(files) == 2
        assert all(f.endswith(".jsonl") for f in files)
        assert not any("not_a_trace.txt" in f for f in files)


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])