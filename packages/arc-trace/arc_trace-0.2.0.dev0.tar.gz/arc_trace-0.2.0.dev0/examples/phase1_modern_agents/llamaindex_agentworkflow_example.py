"""
Example demonstrating Arc Tracing SDK with LlamaIndex AgentWorkflow.

This example shows how the Arc Tracing SDK automatically instruments
LlamaIndex's modern AgentWorkflow architecture (2025) for multi-agent coordination.
"""

import logging
import time
from typing import Dict, Any, List
from arc_tracing import trace_agent

# Configure logging to see tracing activity
logging.basicConfig(level=logging.INFO)

# Mock LlamaIndex AgentWorkflow components for demonstration
# In real usage, you would import from the actual llama_index package
class MockAgentWorkflow:
    """Mock AgentWorkflow class simulating LlamaIndex AgentWorkflow."""
    
    def __init__(self, agents: List["MockAgent"], root_agent: str, initial_state: Dict[str, Any] = None):
        self.agents = agents
        self.root_agent = root_agent
        self.initial_state = initial_state or {}
    
    def run(self, query: str) -> "MockWorkflowResult":
        """Execute the agent workflow."""
        print(f"AgentWorkflow starting with root agent: {self.root_agent}")
        
        current_state = self.initial_state.copy()
        current_state["query"] = query
        
        # Execute agents in sequence (simplified workflow)
        for agent in self.agents:
            print(f"Executing agent: {agent.name}")
            agent_result = agent.run(current_state)
            current_state.update(agent_result.state_updates)
            time.sleep(0.1)  # Simulate processing
        
        return MockWorkflowResult(
            response=current_state.get("final_output", "Workflow completed"),
            state=current_state
        )

class MockFunctionAgent:
    """Mock FunctionAgent class."""
    
    def __init__(self, name: str, tools: List["MockTool"] = None):
        self.name = name
        self.tools = tools or []
    
    def run(self, state: Dict[str, Any]) -> "MockAgentResult":
        """Execute the function agent."""
        query = state.get("query", "")
        print(f"FunctionAgent {self.name} processing: {query}")
        
        # Simulate tool usage
        tool_results = []
        for tool in self.tools:
            tool_result = tool.execute(query)
            tool_results.append(tool_result)
            print(f"Tool {tool.name} result: {tool_result}")
        
        return MockAgentResult(
            response=f"{self.name} completed processing",
            state_updates={f"{self.name.lower()}_results": tool_results}
        )

class MockReActAgent:
    """Mock ReActAgent class."""
    
    def __init__(self, name: str, tools: List["MockTool"] = None):
        self.name = name
        self.tools = tools or []
    
    def run(self, state: Dict[str, Any]) -> "MockAgentResult":
        """Execute the ReAct agent with reasoning pattern."""
        query = state.get("query", "")
        print(f"ReActAgent {self.name} reasoning about: {query}")
        
        # Simulate ReAct reasoning pattern
        print(f"  Thought: I need to analyze this query: {query}")
        print(f"  Action: Using available tools...")
        
        tool_results = []
        for tool in self.tools:
            tool_result = tool.execute(query)
            tool_results.append(tool_result)
            print(f"  Observation: {tool.name} found: {tool_result}")
        
        print(f"  Thought: Based on the observations, I can conclude...")
        
        return MockAgentResult(
            response=f"{self.name} completed ReAct reasoning",
            state_updates={f"{self.name.lower()}_analysis": f"ReAct analysis of {query}"}
        )

class MockTool:
    """Mock tool for agents."""
    
    def __init__(self, name: str):
        self.name = name
        self.metadata = {"name": name}
    
    def execute(self, query: str) -> str:
        """Execute the tool."""
        return f"{self.name} result for: {query}"

class MockAgentResult:
    """Mock result from agent execution."""
    
    def __init__(self, response: str, state_updates: Dict[str, Any] = None):
        self.response = response
        self.state_updates = state_updates or {}

class MockWorkflowResult:
    """Mock result from workflow execution."""
    
    def __init__(self, response: str, state: Dict[str, Any]):
        self.response = response
        self.state = state

# Monkey patch to simulate the llama_index modules
import sys
import types

# Create mock llama_index modules
llama_index_module = types.ModuleType('llama_index')
core_module = types.ModuleType('llama_index.core')
agent_module = types.ModuleType('llama_index.core.agent')
workflow_module = types.ModuleType('llama_index.core.agent.workflow')

workflow_module.AgentWorkflow = MockAgentWorkflow
workflow_module.FunctionAgent = MockFunctionAgent
workflow_module.ReActAgent = MockReActAgent

agent_module.workflow = workflow_module
core_module.agent = agent_module
llama_index_module.core = core_module

sys.modules['llama_index'] = llama_index_module
sys.modules['llama_index.core'] = core_module
sys.modules['llama_index.core.agent'] = agent_module
sys.modules['llama_index.core.agent.workflow'] = workflow_module

@trace_agent
def create_multi_agent_research_workflow(research_topic: str) -> str:
    """
    Create a multi-agent research workflow using LlamaIndex AgentWorkflow.
    
    This demonstrates how the Arc Tracing SDK captures agent coordination,
    tool usage, and workflow state transitions.
    """
    # Create specialized tools
    search_tool = MockTool("web_search")
    analysis_tool = MockTool("data_analysis")
    synthesis_tool = MockTool("content_synthesis")
    review_tool = MockTool("quality_review")
    
    # Create specialized agents
    research_agent = MockFunctionAgent(
        name="ResearchAgent",
        tools=[search_tool, analysis_tool]
    )
    
    write_agent = MockReActAgent(
        name="WriteAgent", 
        tools=[synthesis_tool]
    )
    
    review_agent = MockFunctionAgent(
        name="ReviewAgent",
        tools=[review_tool]
    )
    
    # Create agent workflow
    workflow = MockAgentWorkflow(
        agents=[research_agent, write_agent, review_agent],
        root_agent="ResearchAgent",
        initial_state={
            "research_notes": {},
            "report_content": "Not written yet",
            "review": "Review required"
        }
    )
    
    # Execute the workflow
    result = workflow.run(research_topic)
    
    return f"Research workflow completed: {result.response}"

@trace_agent
def create_adaptive_agent_workflow(task: str) -> str:
    """
    Create an adaptive agent workflow that changes based on task complexity.
    
    This shows how the SDK traces dynamic agent selection and workflow adaptation.
    """
    # Analyze task complexity (simplified)
    is_complex = len(task.split()) > 10
    
    if is_complex:
        # Complex task: use ReAct agents for better reasoning
        print("Detected complex task - using ReAct agents")
        
        planning_agent = MockReActAgent(
            name="PlanningAgent",
            tools=[MockTool("task_analyzer"), MockTool("strategy_planner")]
        )
        
        execution_agent = MockReActAgent(
            name="ExecutionAgent", 
            tools=[MockTool("complex_processor"), MockTool("validation_checker")]
        )
        
        agents = [planning_agent, execution_agent]
        
    else:
        # Simple task: use Function agents for efficiency
        print("Detected simple task - using Function agents")
        
        simple_agent = MockFunctionAgent(
            name="SimpleAgent",
            tools=[MockTool("quick_processor")]
        )
        
        agents = [simple_agent]
    
    # Create adaptive workflow
    workflow = MockAgentWorkflow(
        agents=agents,
        root_agent=agents[0].name,
        initial_state={"task_complexity": "complex" if is_complex else "simple"}
    )
    
    # Execute workflow
    result = workflow.run(task)
    
    return f"Adaptive workflow completed: {result.response}"

if __name__ == "__main__":
    print("=== LlamaIndex AgentWorkflow Tracing Example ===\n")
    
    # Example 1: Multi-agent research workflow
    print("1. Multi-Agent Research Workflow:")
    result1 = create_multi_agent_research_workflow(
        "Comprehensive analysis of emerging trends in quantum machine learning algorithms"
    )
    print(f"Result: {result1}\n")
    
    # Example 2: Simple adaptive workflow
    print("2. Adaptive Workflow (Simple Task):")
    result2 = create_adaptive_agent_workflow("Generate summary")
    print(f"Result: {result2}\n")
    
    # Example 3: Complex adaptive workflow  
    print("3. Adaptive Workflow (Complex Task):")
    result3 = create_adaptive_agent_workflow(
        "Create a comprehensive strategic analysis of market opportunities in the renewable energy sector including competitive landscape assessment and regulatory impact evaluation"
    )
    print(f"Result: {result3}\n")
    
    print("=== Tracing Complete ===")
    print("Check your Arc platform dashboard or local traces for detailed agent workflow execution data!")