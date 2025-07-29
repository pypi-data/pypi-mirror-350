"""
Test script for the simplified backend API.

The backend now accepts:
1. Any API key with X-Test-Mode: true header
2. Default dev key: dev_arc_rewardlab_key
3. Even simpler payloads: {"input": "question", "output": "answer"}
"""

import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend_test")

def test_backend():
    """Test various ways to interact with the simplified backend."""
    base_url = "http://localhost:8000"
    endpoint = "/api/v1/traces/"
    
    # Test cases
    test_cases = [
        {
            "name": "Simplest format with dev key",
            "url": f"{base_url}{endpoint}",
            "headers": {
                "Content-Type": "application/json",
                "X-API-Key": "dev_arc_rewardlab_key"
            },
            "payload": {
                "input": "What is machine learning?",
                "output": "Machine learning is a branch of AI..."
            }
        },
        {
            "name": "Simplest format with test mode",
            "url": f"{base_url}{endpoint}",
            "headers": {
                "Content-Type": "application/json",
                "X-Test-Mode": "true"
            },
            "payload": {
                "input": "What is machine learning?",
                "output": "Machine learning is a branch of AI..."
            }
        },
        {
            "name": "Structured format with test mode",
            "url": f"{base_url}{endpoint}",
            "headers": {
                "Content-Type": "application/json",
                "X-Test-Mode": "true"
            },
            "payload": {
                "input": {"content": "What is machine learning?", "type": "text"},
                "output": {"content": "Machine learning is a branch of AI...", "type": "text"}
            }
        },
        {
            "name": "Batch format with test mode",
            "url": f"{base_url}{endpoint}batch",
            "headers": {
                "Content-Type": "application/json",
                "X-Test-Mode": "true"
            },
            "payload": [
                {"input": "Question 1", "output": "Answer 1"},
                {"input": "Question 2", "output": "Answer 2"}
            ]
        }
    ]
    
    # Run tests
    results = []
    for test in test_cases:
        logger.info(f"Running test: {test['name']}")
        try:
            response = requests.post(
                test["url"],
                headers=test["headers"],
                json=test["payload"],
                timeout=3
            )
            
            status = "SUCCESS" if response.status_code < 400 else "FAILED"
            results.append({
                "name": test["name"],
                "status": status,
                "status_code": response.status_code,
                "response": response.text[:100] + "..." if len(response.text) > 100 else response.text
            })
            
            logger.info(f"  Status: {status} ({response.status_code})")
            logger.info(f"  Response: {response.text[:100]}..." if len(response.text) > 100 else f"  Response: {response.text}")
            
        except Exception as e:
            logger.error(f"  Error: {str(e)}")
            results.append({
                "name": test["name"],
                "status": "ERROR",
                "error": str(e)
            })
    
    # Print summary
    logger.info("\n=== Test Summary ===")
    for result in results:
        status_display = f"{result['status']}: {result.get('status_code', '')}"
        logger.info(f"{result['name']}: {status_display}")
    
    # Check if all tests passed
    all_passed = all(r["status"] == "SUCCESS" for r in results)
    if all_passed:
        logger.info("\n✅ All tests passed! The backend is working correctly.")
        return True
    else:
        logger.info("\n❌ Some tests failed. Check the results for details.")
        return False

if __name__ == "__main__":
    test_backend()