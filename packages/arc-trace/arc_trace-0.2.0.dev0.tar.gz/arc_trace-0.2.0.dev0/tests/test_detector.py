"""Tests for the framework detection functionality."""

import os
import sys
import importlib
import unittest
from unittest.mock import patch, MagicMock
import pytest

from arc_tracing.detector import detect_frameworks, _check_imported_modules, _check_call_stack

class TestDetector:
    """Tests for the framework detection functionality."""
    
    @patch("arc_tracing.detector.importlib.util.find_spec")
    def test_check_imported_modules_empty(self, mock_find_spec):
        """Test that no frameworks are detected when none are imported."""
        # Set up mock to simulate no frameworks imported
        mock_find_spec.return_value = None
        
        # Call the detection function
        frameworks = set()
        _check_imported_modules(frameworks)
        
        # Verify no frameworks were detected
        assert len(frameworks) == 0
    
    @patch("arc_tracing.detector.importlib.util.find_spec")
    def test_check_imported_modules_langchain(self, mock_find_spec):
        """Test that LangChain is detected when imported."""
        # Set up mock to simulate LangChain being imported
        def side_effect(module_name):
            if module_name == "langchain":
                return MagicMock()
            return None
        
        mock_find_spec.side_effect = side_effect
        
        # Call the detection function
        frameworks = set()
        _check_imported_modules(frameworks)
        
        # Verify LangChain was detected
        assert "langchain" in frameworks
    
    @patch("arc_tracing.detector.importlib.util.find_spec")
    def test_check_imported_modules_openai(self, mock_find_spec):
        """Test that OpenAI is detected when imported."""
        # Set up mock to simulate OpenAI being imported
        def side_effect(module_name):
            if module_name == "openai":
                return MagicMock()
            return None
        
        mock_find_spec.side_effect = side_effect
        
        # Call the detection function
        frameworks = set()
        _check_imported_modules(frameworks)
        
        # Verify OpenAI was detected
        assert "openai" in frameworks
    
    @patch("arc_tracing.detector.inspect.stack")
    def test_check_call_stack_langchain(self, mock_stack):
        """Test that LangChain is detected in the call stack."""
        # Set up mock to simulate LangChain in the call stack
        frame_mock = MagicMock()
        frame_mock.f_globals = {"__name__": "langchain.chains.llm"}
        
        frame_info_mock = MagicMock()
        frame_info_mock.frame = frame_mock
        
        mock_stack.return_value = [frame_info_mock]
        
        # Call the detection function
        frameworks = set()
        _check_call_stack(frameworks)
        
        # Verify LangChain was detected
        assert "langchain" in frameworks
    
    @patch("arc_tracing.detector.importlib.util.find_spec")
    @patch("arc_tracing.detector.inspect.stack")
    def test_detect_frameworks_multiple(self, mock_stack, mock_find_spec):
        """Test detection of multiple frameworks."""
        # Set up mocks to simulate multiple frameworks
        def find_spec_side_effect(module_name):
            if module_name in ["openai", "anthropic"]:
                return MagicMock()
            return None
        
        mock_find_spec.side_effect = find_spec_side_effect
        
        # Set up call stack mock
        frame_mock = MagicMock()
        frame_mock.f_globals = {"__name__": "langchain.agents.agent"}
        
        frame_info_mock = MagicMock()
        frame_info_mock.frame = frame_mock
        
        mock_stack.return_value = [frame_info_mock]
        
        # Call the detection function
        frameworks = detect_frameworks()
        
        # Verify all frameworks were detected
        # Note: The function sorts the frameworks alphabetically
        assert frameworks == ["anthropic", "langchain", "openai"]