# Arc Tracing SDK Examples

This directory contains example code for using the Arc Tracing SDK with various frameworks and integration methods.

## Directory Structure

- `direct_api/` - Examples of using Arc Tracing with direct API calls to LLM providers
- `langchain/` - Examples of using Arc Tracing with LangChain
- `llamaindex/` - Examples of using Arc Tracing with LlamaIndex
- `agno/` - Examples of using Arc Tracing with the Agno agent framework
- `google_adk/` - Examples of using Arc Tracing with Google's Agent Development Kit (ADK)

## Running the Examples

Each example can be run directly with Python. They're designed to demonstrate how to integrate the Arc Tracing SDK with minimal code changes.

### Prerequisites

1. Install the Arc Tracing SDK:
   ```bash
   pip install arc-tracing
   ```

2. Install the necessary framework dependencies. For example, to run the LangChain examples:
   ```bash
   pip install "arc-tracing[langchain]"
   ```

3. Set up your API keys as environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export ANTHROPIC_API_KEY="your-anthropic-api-key"
   # Additional keys may be required depending on the example
   ```

4. Run the example:
   ```bash
   python examples/direct_api/openai_example.py
   ```

## Key Concepts

All examples demonstrate the following key concepts:

1. **Importing the SDK** - How to import and configure the SDK
2. **Using the Trace Agent Decorator** - How to apply the `trace_agent` decorator
3. **Exporting Traces** - How to configure trace exporters
4. **Framework-specific Instrumentation** - How framework-specific features are automatically traced

## Example Breakdown

- **Direct API Examples** - Show how to trace direct API calls to OpenAI, Anthropic, etc.
- **Client Wrapper Examples** - Demonstrate using the drop-in client wrappers
- **LangChain Examples** - Illustrate tracing LangChain agents and chains
- **LlamaIndex Examples** - Showcase tracing LlamaIndex query engines and retrievers
- **Agno Examples** - Present tracing Agno agents and teams
- **Google ADK Examples** - Exhibit tracing Google ADK agents and multi-agent systems