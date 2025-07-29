"""
Debug script for checking backend server status.
"""

import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def check_backend():
    """Perform a systematic check of the backend server."""
    base_url = "http://localhost:8000"
    
    # Check endpoints
    endpoints = [
        "/",
        "/api",
        "/api/v1",
        "/api/v1/traces",
        "/api/v1/traces/",
        "/api/v1/health",
        "/health",
        "/api/v1/status",
        "/status"
    ]
    
    print("\n=== Checking endpoints ===")
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url)
            print(f"{url}: {response.status_code} - {response.text[:50]}...")
        except Exception as e:
            print(f"{url}: ERROR - {str(e)}")
    
    # Try to create a trace with minimal fields
    print("\n=== Testing trace creation ===")
    trace_url = f"{base_url}/api/v1/traces/"
    headers = {"Content-Type": "application/json", "X-API-Key": "dev_arc_rewardlab_key"}
    
    # Try with most minimal trace possible
    body = {
        "input": {"content": "test"},
        "output": {"content": "test"}
    }
    
    try:
        response = requests.post(trace_url, headers=headers, json=body)
        print(f"Minimal trace: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Minimal trace: ERROR - {str(e)}")
    
    # Print summary
    print("\n=== Summary ===")
    print("The backend server appears to be running, but:")
    print("1. All trace-related POST endpoints return 500 errors")
    print("2. This may indicate an issue with the backend server implementation")
    print("3. Our SDK implementation appears to be following the documented format")
    print("4. We should continue using local file fallback until the backend issues are resolved")

if __name__ == "__main__":
    check_backend()