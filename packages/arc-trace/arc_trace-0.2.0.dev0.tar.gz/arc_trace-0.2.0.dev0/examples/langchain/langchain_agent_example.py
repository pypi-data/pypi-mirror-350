"""Example of tracing a LangChain agent."""

import os
import sys

# Add parent directory to path to import from arc_tracing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from arc_tracing import trace_agent
from arc_tracing.exporters import ConsoleExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Set up tracing with console exporter for this example
tracer_provider = TracerProvider()
console_exporter = ConsoleExporter()
tracer_provider.add_span_processor(SimpleSpanProcessor(console_exporter))
trace.set_tracer_provider(tracer_provider)

# Import checker function
def check_imports():
    """Check if all required packages are installed."""
    missing = []
    
    try:
        import langchain
    except ImportError:
        missing.append("langchain")
    
    try:
        import langchain_openai
    except ImportError:
        missing.append("langchain-openai")
    
    if missing:
        print(f"Error: Missing required packages: {', '.join(missing)}")
        print("Install them with:")
        print(f"pip install {' '.join(missing)}")
        sys.exit(1)
    
    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)

@trace_agent
def run_langchain_agent(query):
    """Run a simple LangChain agent with the query."""
    # Import LangChain components
    from langchain_openai import ChatOpenAI
    from langchain.agents import AgentExecutor, create_react_agent
    from langchain.tools import tool
    from langchain.prompts import PromptTemplate
    
    # Define a simple tool
    @tool
    def search(query: str) -> str:
        """Search for information about a topic."""
        # This is a mock search tool
        return f"Here is some information about '{query}': This is sample search result data."
    
    # Define calculator tool
    @tool
    def calculator(expression: str) -> str:
        """Evaluate a mathematical expression."""
        try:
            return str(eval(expression))
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"
    
    # Create LLM
    llm = ChatOpenAI(temperature=0)
    
    # Define tools
    tools = [search, calculator]
    
    # Define the prompt
    prompt = PromptTemplate.from_template(
        """
        You are a helpful assistant that can use tools to answer questions.
        
        {tools}
        
        Use the following format:
        
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        
        Begin!
        
        Question: {input}
        """
    )
    
    # Create the agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Create the executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    # Run the agent
    result = agent_executor.invoke({"input": query})
    
    return result["output"]

# Main function
if __name__ == "__main__":
    # Check imports first
    check_imports()
    
    # Get query from command line or use default
    query = sys.argv[1] if len(sys.argv) > 1 else "What is 2 + 2 and who is Albert Einstein?"
    
    print(f"Query: {query}")
    print("-" * 50)
    
    response = run_langchain_agent(query)
    print(f"Response: {response}")
    print("-" * 50)
    print("Check the console output above for the trace information.")