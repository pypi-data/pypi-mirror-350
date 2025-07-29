#!/usr/bin/env python
"""Backend discovery script for Arc Tracing SDK."""

import os
import sys
import argparse
import logging

# Add parent directory to path to import from arc_tracing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import the discovery tool
from arc_tracing.tools.backend_discovery import discover_backend, print_discovery_report

def main():
    """Run the backend discovery tool."""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Arc Tracing Backend Discovery Tool")
    parser.add_argument(
        "--base-url", 
        default="http://localhost:8000",
        help="Base URL of the backend server (e.g., http://localhost:8000)"
    )
    parser.add_argument(
        "--api-key", 
        help="API key to use for authentication tests"
    )
    parser.add_argument(
        "--insecure", 
        action="store_true", 
        help="Disable SSL verification"
    )
    parser.add_argument(
        "--output", 
        choices=["print", "json"], 
        default="print", 
        help="Output format"
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Run discovery
    results = discover_backend(args.base_url, args.api_key, not args.insecure)
    
    # Output results
    if args.output == "print":
        print_discovery_report(results)
    else:
        import json
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()