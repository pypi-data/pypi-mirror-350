"""
Direct backend test script.

This script bypasses the OpenTelemetry pipeline and directly sends
a properly formatted trace to the backend API using requests.
"""

import json
import logging
import requests
import uuid
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("direct_test")

def create_trace():
    """Create a properly formatted trace object."""
    # Create a minimal trace object with only required fields
    trace = {
        "input": {
            "content": "What is machine learning?",
            "type": "text"
        },
        "output": {
            "content": "Machine learning is a branch of artificial intelligence...",
            "type": "text"
        },
        # Steps are optional but recommended
        "steps": []
    }
    
    return trace

def send_to_backend(trace, endpoint="http://localhost:8000/api/v1/traces/", api_key="dev_arc_rewardlab_key"):
    """Send the trace directly to the backend."""
    # Create headers
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
        "X-ARC-SDK-Version": "0.1.0"
    }
    
    # Log the request details
    logger.info(f"Sending trace to {endpoint}")
    logger.debug(f"Headers: {headers}")
    logger.debug(f"Trace data sample: {json.dumps(trace)[:200]}...")
    
    try:
        # Send the request
        response = requests.post(
            endpoint,
            headers=headers,
            json=trace,
            timeout=30
        )
        
        # Log the response
        if response.status_code >= 400:
            logger.error(f"Error sending trace: {response.status_code} - {response.text}")
        else:
            logger.info(f"Successfully sent trace: {response.status_code}")
            logger.debug(f"Response: {response.text}")
            
        return response.status_code < 400
        
    except Exception as e:
        logger.error(f"Exception sending trace: {e}")
        return False

def main():
    """Run the direct backend test."""
    logger.info("Creating test trace...")
    trace = create_trace()
    
    logger.info("Sending trace to backend...")
    success = send_to_backend(trace)
    
    if success:
        logger.info("Test completed successfully!")
    else:
        logger.error("Test failed to send trace to backend")

if __name__ == "__main__":
    main()