"""Pytest fixtures for Arc Tracing SDK tests."""

import os
import sys
import pytest
from typing import Dict, List, Generator

# Make sure the package is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture
def mock_openai_response() -> Dict:
    """Mock response from OpenAI API."""
    return {
        "id": "chatcmpl-abc123",
        "object": "chat.completion",
        "created": 1677858242,
        "model": "gpt-4",
        "usage": {
            "prompt_tokens": 13,
            "completion_tokens": 7,
            "total_tokens": 20
        },
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "This is a test response."
                },
                "finish_reason": "stop",
                "index": 0
            }
        ]
    }

@pytest.fixture
def mock_anthropic_response() -> Dict:
    """Mock response from Anthropic API."""
    return {
        "id": "msg_0123456789",
        "type": "message",
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "This is a test response."
            }
        ],
        "model": "claude-3-sonnet-20240229",
        "stop_reason": "end_turn",
        "usage": {
            "input_tokens": 15,
            "output_tokens": 5
        }
    }

@pytest.fixture
def sample_trace_data() -> Dict:
    """Sample trace data for testing."""
    return {
        "name": "test_span",
        "context": {
            "trace_id": "0123456789abcdef0123456789abcdef",
            "span_id": "0123456789abcdef",
            "is_remote": False,
        },
        "parent_id": None,
        "start_time": 1620000000000000000,
        "end_time": 1620000001000000000,
        "status": {
            "status_code": 0,
            "description": "",
        },
        "attributes": {
            "arc_tracing.component": "test",
            "arc_tracing.test.value": "test_value",
        },
        "events": [],
        "links": [],
    }