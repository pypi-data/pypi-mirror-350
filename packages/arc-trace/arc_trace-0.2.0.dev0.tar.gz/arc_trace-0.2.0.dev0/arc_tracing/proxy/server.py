"""Proxy server implementation for intercepting LLM API calls."""

import json
import logging
import threading
import time
from typing import Any, Dict, List, Optional, Set, Union, Callable
import uuid

from opentelemetry import trace

try:
    from fastapi import FastAPI, Request, Response, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    import uvicorn
except ImportError:
    FastAPI = None
    Request = None
    Response = None
    HTTPException = Exception
    JSONResponse = None
    uvicorn = None

from arc_tracing.config import get_config

# Configure logger
logger = logging.getLogger("arc_tracing")

# Initialize tracer
tracer = trace.get_tracer("arc_tracing.proxy")

# Global server instance
_server_app = None
_server_thread = None
_server_port = 8000
_server_host = "127.0.0.1"
_running = False

def run_proxy_server(
    host: str = "127.0.0.1", 
    port: int = 8000, 
    start_new_thread: bool = True
) -> Any:
    """
    Start the API proxy server.
    
    This function starts a FastAPI server that acts as a proxy for
    LLM API calls, capturing and tracing the requests and responses.
    
    Args:
        host: The host to bind the server to.
        port: The port to bind the server to.
        start_new_thread: If True, starts the server in a new thread.
            If False, runs the server in the current thread (blocking).
            
    Returns:
        The FastAPI app instance if start_new_thread is True,
        otherwise this function blocks and does not return.
        
    Raises:
        ImportError: If FastAPI or Uvicorn are not installed.
    """
    global _server_app, _server_thread, _server_port, _server_host, _running
    
    # Check if server is already running
    if _running:
        logger.info(f"Proxy server already running on {_server_host}:{_server_port}")
        return _server_app
    
    # Check if required dependencies are installed
    if FastAPI is None or uvicorn is None:
        raise ImportError(
            "FastAPI and Uvicorn are required for the proxy server. "
            "Install them with `pip install fastapi uvicorn`."
        )
    
    # Store server configuration
    _server_host = host
    _server_port = port
    
    # Create FastAPI app
    app = FastAPI(title="Arc Tracing Proxy")
    _server_app = app
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # OpenAI chat completions endpoint
    @app.post("/v1/chat/completions")
    async def openai_chat_completions(request: Request) -> Response:
        """Proxy endpoint for OpenAI chat completions."""
        return await _handle_openai_request(request, "chat.completions")
    
    # OpenAI completions endpoint
    @app.post("/v1/completions")
    async def openai_completions(request: Request) -> Response:
        """Proxy endpoint for OpenAI completions."""
        return await _handle_openai_request(request, "completions")
    
    # OpenAI embeddings endpoint
    @app.post("/v1/embeddings")
    async def openai_embeddings(request: Request) -> Response:
        """Proxy endpoint for OpenAI embeddings."""
        return await _handle_openai_request(request, "embeddings")
    
    # Anthropic messages endpoint
    @app.post("/anthropic/v1/messages")
    async def anthropic_messages(request: Request) -> Response:
        """Proxy endpoint for Anthropic messages."""
        return await _handle_anthropic_request(request, "messages")
    
    # Add more endpoints for other providers as needed
    
    # Health check endpoint
    @app.get("/health")
    async def health_check() -> Dict[str, str]:
        """Health check endpoint."""
        return {"status": "ok", "service": "arc_tracing_proxy"}
    
    # Start the server
    _running = True
    if start_new_thread:
        # Start in a new thread
        _server_thread = threading.Thread(
            target=uvicorn.run,
            args=(app,),
            kwargs={
                "host": host,
                "port": port,
                "log_level": "error",
            },
            daemon=True,
        )
        _server_thread.start()
        
        # Wait for server to start
        time.sleep(1.0)
        logger.info(f"Started proxy server on {host}:{port}")
        
        return app
    else:
        # Run in current thread (blocking)
        logger.info(f"Starting proxy server on {host}:{port}")
        uvicorn.run(app, host=host, port=port)

async def _handle_openai_request(request: Request, endpoint_type: str) -> Response:
    """
    Handle an OpenAI API request.
    
    Args:
        request: The FastAPI request object.
        endpoint_type: The type of endpoint being called.
        
    Returns:
        The response from the OpenAI API, with tracing added.
    """
    # Read request body
    body = await request.body()
    json_body = json.loads(body)
    
    # Start tracing span
    with tracer.start_as_current_span(
        f"openai.proxy.{endpoint_type}",
        attributes={
            "arc_tracing.component": f"openai.{endpoint_type}",
            "arc_tracing.proxy": True,
        }
    ) as span:
        # Record request details
        if "model" in json_body:
            span.set_attribute("arc_tracing.openai.model", json_body["model"])
        
        if endpoint_type == "chat.completions" and "messages" in json_body:
            # Record chat messages
            try:
                messages = json_body["messages"]
                for i, msg in enumerate(messages):
                    if isinstance(msg, dict) and "role" in msg and "content" in msg:
                        role = msg["role"]
                        if role == "system":
                            span.set_attribute("arc_tracing.openai.system_message", str(msg["content"]))
                        elif role == "user" and i == len(messages) - 1:  # Last user message
                            span.set_attribute("arc_tracing.openai.user_message", str(msg["content"]))
            except Exception as e:
                logger.debug(f"Error extracting OpenAI messages: {e}")
        
        elif endpoint_type == "completions" and "prompt" in json_body:
            # Record completion prompt
            prompt = json_body["prompt"]
            if isinstance(prompt, str):
                span.set_attribute("arc_tracing.openai.prompt", prompt)
            elif isinstance(prompt, list) and prompt and isinstance(prompt[0], str):
                span.set_attribute("arc_tracing.openai.prompt", prompt[0])
        
        # Forward the request to the actual OpenAI API
        try:
            import requests
            import os
            
            # Get API key from environment
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                return JSONResponse(
                    content={"error": "OPENAI_API_KEY environment variable is not set"},
                    status_code=400,
                )
            
            # Determine the actual OpenAI API endpoint
            if endpoint_type == "chat.completions":
                url = "https://api.openai.com/v1/chat/completions"
            elif endpoint_type == "completions":
                url = "https://api.openai.com/v1/completions"
            elif endpoint_type == "embeddings":
                url = "https://api.openai.com/v1/embeddings"
            else:
                return JSONResponse(
                    content={"error": f"Unknown endpoint type: {endpoint_type}"},
                    status_code=400,
                )
            
            # Forward the request
            response = requests.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                json=json_body,
                timeout=60,
            )
            
            # Get response data
            response_data = response.json()
            
            # Record response data
            if "choices" in response_data and response_data["choices"]:
                first_choice = response_data["choices"][0]
                if endpoint_type == "chat.completions":
                    if "message" in first_choice and "content" in first_choice["message"]:
                        span.set_attribute("arc_tracing.openai.response", first_choice["message"]["content"])
                else:
                    if "text" in first_choice:
                        span.set_attribute("arc_tracing.openai.response", first_choice["text"])
            
            if "usage" in response_data:
                if "prompt_tokens" in response_data["usage"]:
                    span.set_attribute("arc_tracing.openai.prompt_tokens", response_data["usage"]["prompt_tokens"])
                if "completion_tokens" in response_data["usage"]:
                    span.set_attribute("arc_tracing.openai.completion_tokens", response_data["usage"]["completion_tokens"])
                if "total_tokens" in response_data["usage"]:
                    span.set_attribute("arc_tracing.openai.total_tokens", response_data["usage"]["total_tokens"])
            
            # Return the response
            return JSONResponse(
                content=response_data,
                status_code=response.status_code,
            )
        
        except Exception as e:
            # Record exception
            span.record_exception(e)
            logger.error(f"Error proxying OpenAI request: {e}")
            return JSONResponse(
                content={"error": f"Error proxying request: {str(e)}"},
                status_code=500,
            )

async def _handle_anthropic_request(request: Request, endpoint_type: str) -> Response:
    """
    Handle an Anthropic API request.
    
    Args:
        request: The FastAPI request object.
        endpoint_type: The type of endpoint being called.
        
    Returns:
        The response from the Anthropic API, with tracing added.
    """
    # Similar implementation to _handle_openai_request but for Anthropic
    # To be implemented
    pass

def shutdown_proxy_server() -> None:
    """Shut down the proxy server."""
    global _server_app, _server_thread, _running
    
    if not _running:
        logger.info("Proxy server not running")
        return
    
    # TODO: Implement clean shutdown
    # This is a placeholder for now, as graceful shutdown
    # of Uvicorn in a thread requires more complex handling
    
    logger.info("Proxy server shutdown requested (daemon thread will terminate on program exit)")
    _running = False