"""
Minimal backend test using the exact format from documentation.
"""

import json
import logging
import requests
import uuid

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("minimal_test")

# Backend details
ENDPOINT = "http://localhost:8000/api/v1/traces/"
API_KEY = "dev_arc_rewardlab_key"

def main():
    """Send a minimal valid trace to the backend."""
    # Create the minimal trace exactly as specified in the documentation
    trace = {
        "input": {
            "content": "User query or input text",
            "type": "text"
        },
        "output": {
            "content": "Agent response or output",
            "type": "text"
        }
    }
    
    # Set up headers
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    logger.info(f"Sending minimal trace to {ENDPOINT}")
    logger.info(f"Trace: {json.dumps(trace, indent=2)}")
    logger.info(f"Headers: {headers}")
    
    try:
        # Make the request
        response = requests.post(
            ENDPOINT,
            headers=headers,
            json=trace,
            timeout=10
        )
        
        # Print complete response details
        logger.info(f"Status code: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")
        
        try:
            # Try to parse as JSON
            response_json = response.json()
            logger.info(f"Response JSON: {json.dumps(response_json, indent=2)}")
        except:
            # If not JSON, print raw text
            logger.info(f"Response text: {response.text}")
        
        if response.status_code < 400:
            logger.info("SUCCESS: Trace sent successfully!")
        else:
            logger.error(f"ERROR: Failed to send trace. Status code: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Exception: {str(e)}")

if __name__ == "__main__":
    main()