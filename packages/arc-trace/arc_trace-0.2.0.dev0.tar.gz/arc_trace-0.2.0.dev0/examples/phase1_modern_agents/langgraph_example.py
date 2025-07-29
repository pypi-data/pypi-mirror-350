"""
Example demonstrating Arc Tracing SDK with LangGraph.

This example shows how the Arc Tracing SDK automatically instruments
LangGraph workflows for comprehensive state graph tracing.
"""

import logging
import time
from typing import Dict, Any
from arc_tracing import trace_agent

# Configure logging to see tracing activity
logging.basicConfig(level=logging.INFO)

# Mock LangGraph components for demonstration
# In real usage, you would import from the actual langgraph package
class MockStateGraph:
    """Mock StateGraph class simulating LangGraph."""
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self._compiled = False
    
    def add_node(self, name: str, func):
        """Add a node to the state graph."""
        self.nodes[name] = func
        return self
    
    def add_edge(self, from_node: str, to_node: str):
        """Add an edge between nodes."""
        self.edges.append((from_node, to_node))
        return self
    
    def compile(self) -> "MockCompiledGraph":
        """Compile the state graph."""
        print(f"Compiling graph with {len(self.nodes)} nodes and {len(self.edges)} edges")
        self._compiled = True
        return MockCompiledGraph(self.nodes, self.edges)

class MockCompiledGraph:
    """Mock compiled graph for execution."""
    
    def __init__(self, nodes: Dict[str, Any], edges: list):
        self.nodes = nodes
        self.edges = edges
    
    def invoke(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the graph with the given initial state."""
        print("Executing LangGraph workflow...")
        current_state = initial_state.copy()
        
        # Simulate node execution
        for node_name, node_func in self.nodes.items():
            print(f"Executing node: {node_name}")
            time.sleep(0.1)  # Simulate processing
            
            # Execute node function
            node_result = node_func(current_state)
            current_state.update(node_result)
        
        return current_state

# Mock node functions
def research_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Research node that gathers information."""
    query = state.get("query", "")
    print(f"Research node processing: {query}")
    
    return {
        "research_results": f"Research findings for: {query}",
        "research_completed": True
    }

def analysis_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Analysis node that processes research results."""
    research_results = state.get("research_results", "")
    print(f"Analysis node processing: {research_results}")
    
    return {
        "analysis": f"Analysis of: {research_results}",
        "analysis_completed": True
    }

def synthesis_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Synthesis node that creates final output."""
    analysis = state.get("analysis", "")
    print(f"Synthesis node processing: {analysis}")
    
    return {
        "final_output": f"Synthesized result: {analysis}",
        "workflow_completed": True
    }

# Monkey patch to simulate the langgraph module
import sys
import types

# Create mock langgraph module
langgraph_module = types.ModuleType('langgraph')
graph_module = types.ModuleType('langgraph.graph')
graph_module.StateGraph = MockStateGraph
langgraph_module.graph = graph_module

sys.modules['langgraph'] = langgraph_module
sys.modules['langgraph.graph'] = graph_module

@trace_agent
def create_research_workflow(query: str) -> str:
    """
    Create and execute a LangGraph research workflow.
    
    This demonstrates how the Arc Tracing SDK automatically instruments
    LangGraph state management and node execution.
    """
    # Create state graph
    workflow = MockStateGraph()
    
    # Add nodes to the workflow
    workflow.add_node("research", research_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("synthesis", synthesis_node)
    
    # Add edges to define the flow
    workflow.add_edge("research", "analysis")
    workflow.add_edge("analysis", "synthesis")
    
    # Compile the graph
    compiled_workflow = workflow.compile()
    
    # Execute the workflow
    initial_state = {"query": query}
    final_state = compiled_workflow.invoke(initial_state)
    
    return final_state.get("final_output", "No result")

@trace_agent
def create_conditional_workflow(task: str) -> str:
    """
    Create a LangGraph workflow with conditional logic.
    
    This shows how the SDK traces conditional edges and branching.
    """
    def router_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Router node that decides the next step."""
        task = state.get("task", "")
        
        if "urgent" in task.lower():
            route = "priority_handler"
        else:
            route = "standard_handler"
        
        print(f"Router deciding: {route}")
        return {"route": route, "routing_completed": True}
    
    def priority_handler(state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle urgent tasks."""
        task = state.get("task", "")
        return {"result": f"URGENT: {task} - handled with priority"}
    
    def standard_handler(state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle standard tasks."""
        task = state.get("task", "")
        return {"result": f"STANDARD: {task} - handled normally"}
    
    # Create workflow with conditional logic
    workflow = MockStateGraph()
    workflow.add_node("router", router_node)
    workflow.add_node("priority", priority_handler)
    workflow.add_node("standard", standard_handler)
    
    # Add conditional edges (simplified for demo)
    workflow.add_edge("router", "priority")
    workflow.add_edge("router", "standard")
    
    # Compile and execute
    compiled_workflow = workflow.compile()
    initial_state = {"task": task}
    final_state = compiled_workflow.invoke(initial_state)
    
    return final_state.get("result", "No result")

if __name__ == "__main__":
    print("=== LangGraph Tracing Example ===\n")
    
    # Example 1: Linear research workflow
    print("1. Linear Research Workflow:")
    result1 = create_research_workflow("What are the benefits of using state graphs for AI agents?")
    print(f"Result: {result1}\n")
    
    # Example 2: Conditional workflow
    print("2. Conditional Workflow (Standard):")
    result2 = create_conditional_workflow("Process customer feedback data")
    print(f"Result: {result2}\n")
    
    print("3. Conditional Workflow (Urgent):")
    result3 = create_conditional_workflow("URGENT: Handle system security breach")
    print(f"Result: {result3}\n")
    
    print("=== Tracing Complete ===")
    print("Check your Arc platform dashboard or local traces for detailed state graph execution data!")