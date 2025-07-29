"""Backend discovery tool for Arc Tracing SDK."""

import logging
import requests
import json
from typing import Dict, List, Optional, Tuple
import urllib3

# Configure logger
logger = logging.getLogger("arc_tracing")

# Disable InsecureRequestWarning during discovery
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BackendDiscovery:
    """
    Tool for discovering and testing backend endpoints for the Arc Tracing SDK.
    
    This tool helps users find the correct API endpoint and authentication method
    for their backend server.
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, verify_ssl: bool = True):
        """
        Initialize the backend discovery tool.
        
        Args:
            base_url: Base URL of the backend server (e.g., "http://localhost:8000")
            api_key: API key to use for authentication tests
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        
        # Common endpoint patterns to try
        self.endpoint_patterns = [
            "/traces",
            "/api/traces",
            "/api/v1/traces",
            "/v1/traces",
            "/trace",
            "/api/trace",
            "/api/v1/trace",
            "/v1/trace",
            "/telemetry/traces",
            "/api/telemetry/traces",
            "/ingest/traces",
            "/api/ingest/traces",
            "/otel/traces",
            "/api/otel/traces",
            "/traces/ingest",
            "/api/traces/ingest"
        ]
        
        # Authentication methods to try
        self.auth_methods = [
            ("none", None, None),  # No authentication
            ("bearer", "Authorization", f"Bearer {api_key}" if api_key else "Bearer dev_key"),
            ("header", "X-API-Key", api_key or "dev_key"),
            ("header", "api-key", api_key or "dev_key"),
            ("header", "Api-Key", api_key or "dev_key"),
            # Add basic auth if needed
        ]
        
        # Sample span data for testing
        self.sample_span = {
            "spans": [{
                "name": "test.span",
                "context": {
                    "trace_id": "0x123456789abcdef0123456789abcdef0",
                    "span_id": "0x1234567890abcdef",
                    "is_remote": False
                },
                "parent_id": None,
                "start_time": 1747859000000000000,
                "end_time": 1747859000100000000,
                "status": {
                    "status_code": 0,
                    "description": None
                },
                "attributes": {
                    "arc_tracing.test": True
                },
                "events": []
            }],
            "source": "arc_tracing_discovery",
            "version": "0.1.0"
        }
    
    def discover(self) -> Dict:
        """
        Discover backend endpoints and authentication methods.
        
        Returns:
            A dictionary with discovery results
        """
        results = {
            "base_url": self.base_url,
            "endpoints_tested": [],
            "successful_endpoints": [],
            "server_info": {},
            "recommendations": {}
        }
        
        logger.info(f"Starting backend discovery for {self.base_url}")
        
        # First, check if the server is reachable
        try:
            response = requests.get(
                self.base_url, 
                timeout=5,
                verify=self.verify_ssl
            )
            results["server_info"]["reachable"] = True
            results["server_info"]["status_code"] = response.status_code
            try:
                results["server_info"]["content"] = response.json()
            except:
                pass
        except Exception as e:
            logger.error(f"Failed to connect to server: {e}")
            results["server_info"]["reachable"] = False
            results["server_info"]["error"] = str(e)
            results["recommendations"]["connection"] = "Check that the server is running and accessible"
            return results
        
        # Test each endpoint pattern
        for endpoint in self.endpoint_patterns:
            endpoint_url = f"{self.base_url}{endpoint}"
            endpoint_result = {
                "url": endpoint_url,
                "methods_tested": [],
                "successful_methods": []
            }
            
            # Test with each authentication method
            for auth_method, header_name, header_value in self.auth_methods:
                auth_result = {
                    "method": auth_method,
                    "header": header_name,
                    "value_sample": header_value[:10] + "..." if header_value and len(header_value) > 10 else header_value,
                    "success": False
                }
                
                headers = {"Content-Type": "application/json"}
                if header_name and header_value:
                    headers[header_name] = header_value
                
                try:
                    response = requests.post(
                        endpoint_url,
                        headers=headers,
                        json=self.sample_span,
                        timeout=10,
                        verify=self.verify_ssl
                    )
                    
                    auth_result["status_code"] = response.status_code
                    try:
                        auth_result["response"] = response.json()
                    except:
                        auth_result["response"] = response.text[:100]
                    
                    # Consider 200, 201, 202, 204 as successful responses
                    if 200 <= response.status_code < 300:
                        auth_result["success"] = True
                        endpoint_result["successful_methods"].append({
                            "method": auth_method,
                            "header": header_name,
                            "value": header_value
                        })
                
                except Exception as e:
                    auth_result["error"] = str(e)
                
                endpoint_result["methods_tested"].append(auth_result)
            
            results["endpoints_tested"].append(endpoint_result)
            
            # If we found successful methods for this endpoint, add it to successful endpoints
            if endpoint_result["successful_methods"]:
                results["successful_endpoints"].append({
                    "url": endpoint_url,
                    "methods": endpoint_result["successful_methods"]
                })
        
        # Generate recommendations
        if results["successful_endpoints"]:
            best_endpoint = results["successful_endpoints"][0]
            best_method = best_endpoint["methods"][0]
            
            results["recommendations"]["endpoint"] = best_endpoint["url"]
            results["recommendations"]["auth_method"] = best_method["method"]
            results["recommendations"]["auth_header"] = best_method["header"]
            results["recommendations"]["auth_value"] = best_method["value"]
            results["recommendations"]["config"] = {
                "endpoint": best_endpoint["url"],
                "auth": {
                    "method": best_method["method"],
                    "header": best_method["header"],
                    "api_key": self.api_key or "YOUR_API_KEY"
                }
            }
            results["recommendations"]["command"] = (
                f"python test_backend_integration.py "
                f"--backend-url \"{best_endpoint['url']}\" "
                f"--auth-method {best_method['method']} "
                f"--auth-header \"{best_method['header']}\" "
                f"--api-key \"{self.api_key or 'YOUR_API_KEY'}\""
            )
        else:
            # No successful endpoints found
            # Find endpoints that returned auth errors (401, 403) as they might be valid but need correct auth
            auth_required_endpoints = []
            for endpoint_result in results["endpoints_tested"]:
                for method in endpoint_result["methods_tested"]:
                    if method.get("status_code") in (401, 403):
                        auth_required_endpoints.append(endpoint_result["url"])
                        break
            
            if auth_required_endpoints:
                results["recommendations"]["endpoint"] = auth_required_endpoints[0]
                results["recommendations"]["message"] = "Authentication required. Check your API key and authentication method."
            else:
                results["recommendations"]["message"] = "No valid endpoints found. Check server configuration."
        
        return results


def discover_backend(base_url: str, api_key: Optional[str] = None, verify_ssl: bool = True) -> Dict:
    """
    Discover backend endpoints and authentication methods.
    
    Args:
        base_url: Base URL of the backend server (e.g., "http://localhost:8000")
        api_key: API key to use for authentication tests
        verify_ssl: Whether to verify SSL certificates
        
    Returns:
        A dictionary with discovery results
    """
    discovery = BackendDiscovery(base_url, api_key, verify_ssl)
    return discovery.discover()


def print_discovery_report(results: Dict) -> None:
    """
    Print a human-readable report of the discovery results.
    
    Args:
        results: Discovery results from discover_backend()
    """
    print("\n===== BACKEND DISCOVERY REPORT =====\n")
    
    print(f"Base URL: {results['base_url']}")
    
    if not results.get("server_info", {}).get("reachable", False):
        print(f"\n❌ Server not reachable: {results.get('server_info', {}).get('error', 'Unknown error')}")
        if results.get("recommendations", {}).get("connection"):
            print(f"\nRecommendation: {results['recommendations']['connection']}")
        return
    
    print(f"\nServer status: {'✅ Reachable' if results['server_info']['reachable'] else '❌ Not reachable'}")
    
    if results.get("successful_endpoints"):
        print("\n✅ Successfully discovered valid endpoints:")
        for i, endpoint in enumerate(results["successful_endpoints"]):
            print(f"\n{i+1}. Endpoint: {endpoint['url']}")
            print("   Authentication methods:")
            for j, method in enumerate(endpoint["methods"]):
                print(f"   {j+1}. {method['method']} - {method['header']}: {method['value']}")
    else:
        print("\n❌ No valid endpoints discovered.")
        
        # List endpoints that require authentication
        auth_endpoints = []
        for endpoint in results["endpoints_tested"]:
            for method in endpoint["methods_tested"]:
                if method.get("status_code") in (401, 403):
                    auth_endpoints.append(endpoint["url"])
                    break
        
        if auth_endpoints:
            print("\nEndpoints requiring authentication:")
            for endpoint in auth_endpoints:
                print(f"- {endpoint}")
    
    print("\n----- RECOMMENDATIONS -----\n")
    
    if results.get("recommendations", {}).get("endpoint"):
        print(f"Recommended endpoint: {results['recommendations']['endpoint']}")
        
        if results.get("recommendations", {}).get("auth_method"):
            auth_method = results["recommendations"]["auth_method"]
            auth_header = results["recommendations"]["auth_header"]
            auth_value = results["recommendations"]["auth_value"]
            
            print(f"Authentication: {auth_method} ({auth_header}: {auth_value})")
            
            print("\nTo use this configuration with the integration test:")
            print(f"\n{results['recommendations']['command']}")
            
            print("\nFor your configuration file (arc_config.yml):")
            print("\n```yaml")
            print("trace:")
            print("  frameworks: \"auto\"")
            print("  detail_level: \"comprehensive\"")
            print(f"  endpoint: \"{results['recommendations']['endpoint']}\"")
            print("  auth:")
            print(f"    api_key: \"{results['recommendations'].get('config', {}).get('auth', {}).get('api_key', 'YOUR_API_KEY')}\"")
            print("```")
        else:
            print(f"\nAuthentication required. Check your API key and authentication method.")
    else:
        print(results.get("recommendations", {}).get("message", "No recommendations available."))
    
    print("\n=====================================\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Arc Tracing Backend Discovery Tool")
    parser.add_argument("base_url", help="Base URL of the backend server (e.g., http://localhost:8000)")
    parser.add_argument("--api-key", help="API key to use for authentication tests")
    parser.add_argument("--insecure", action="store_true", help="Disable SSL verification")
    parser.add_argument("--output", choices=["print", "json"], default="print", help="Output format")
    
    args = parser.parse_args()
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Run discovery
    results = discover_backend(args.base_url, args.api_key, not args.insecure)
    
    # Output results
    if args.output == "print":
        print_discovery_report(results)
    else:
        print(json.dumps(results, indent=2))