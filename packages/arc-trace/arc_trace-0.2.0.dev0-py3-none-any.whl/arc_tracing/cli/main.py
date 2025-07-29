"""Main CLI module for Arc Tracing SDK."""

import argparse
import os
import sys
import logging
import importlib.metadata
from typing import List, Optional

from arc_tracing.config import get_config
from arc_tracing.proxy import run_proxy_server, setup_proxy_environment
from arc_tracing.exporters import LocalFileExporter, BatchUploader

logger = logging.getLogger("arc_tracing")

def get_version() -> str:
    """Get the current version of the SDK."""
    try:
        return importlib.metadata.version("arc-tracing")
    except importlib.metadata.PackageNotFoundError:
        return "0.1.0"  # Default version if not installed

def configure_logging(verbose: bool) -> None:
    """Configure logging for CLI."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def init_command(args: argparse.Namespace) -> None:
    """Initialize a new project with Arc Tracing."""
    # Create default configuration file
    config_path = args.output_path or "arc_config.yml"
    
    if os.path.exists(config_path) and not args.force:
        print(f"Configuration file {config_path} already exists. Use --force to overwrite.")
        return
    
    # Create a basic configuration
    config_content = """# Arc Tracing SDK Configuration
trace:
  # Framework detection: "auto" or list specific frameworks
  frameworks: "auto"
  
  # Level of detail to capture: "minimal", "standard", or "comprehensive"
  detail_level: "standard"
  
  # Where to send traces
  endpoint: "https://api.arc.dev/traces"
  
  # Authentication
  auth:
    api_key: "${ARC_API_KEY}"  # Will be read from environment variable
  
  # Signals to extract for future reinforcement learning
  signals: []
"""
    
    # Write the configuration file
    with open(config_path, "w") as f:
        f.write(config_content)
    
    print(f"Created configuration file at {config_path}")
    print("Next steps:")
    print("1. Set your API key in the ARC_API_KEY environment variable")
    print("2. Import the SDK in your code: from arc_tracing import trace_agent")
    print("3. Decorate your agent function: @trace_agent")

def proxy_command(args: argparse.Namespace) -> None:
    """Start the proxy server."""
    # Start the proxy server
    print(f"Starting proxy server on {args.host}:{args.port}...")
    try:
        server = run_proxy_server(host=args.host, port=args.port, start_new_thread=False)
    except ImportError:
        print("Error: FastAPI and Uvicorn are required for the proxy server.")
        print("Install them with: pip install fastapi uvicorn")
        return
    except Exception as e:
        print(f"Error starting proxy server: {e}")
        return

def env_command(args: argparse.Namespace) -> None:
    """Set up environment variables for proxy."""
    # Configure the proxy environment
    proxy_url = f"http://{args.host}:{args.port}"
    setup_proxy_environment(proxy_url=proxy_url)
    
    print(f"Environment configured to use proxy at {proxy_url}")
    print("The following environment variables have been set:")
    print(f"  OPENAI_API_BASE={os.environ.get('OPENAI_API_BASE')}")
    print(f"  ANTHROPIC_API_URL={os.environ.get('ANTHROPIC_API_URL')}")
    
    if args.shell:
        # Print export commands for shell
        if args.shell == "bash":
            print("\nTo set these variables in your shell, run:")
            print(f"export OPENAI_API_BASE={os.environ.get('OPENAI_API_BASE')}")
            print(f"export ANTHROPIC_API_URL={os.environ.get('ANTHROPIC_API_URL')}")
        elif args.shell == "powershell":
            print("\nTo set these variables in PowerShell, run:")
            print(f"$env:OPENAI_API_BASE=\"{os.environ.get('OPENAI_API_BASE')}\"")
            print(f"$env:ANTHROPIC_API_URL=\"{os.environ.get('ANTHROPIC_API_URL')}\"")

def info_command(args: argparse.Namespace) -> None:
    """Display information about the SDK."""
    # Get SDK version
    version = get_version()
    
    # Get configuration
    config = get_config()
    
    # Print information
    print("Arc Tracing SDK Information")
    print("==========================")
    print(f"Version: {version}")
    print(f"Configuration file: {args.config or 'Default'}")
    print(f"API Endpoint: {config.endpoint}")
    print(f"Detail Level: {config.detail_level}")
    
    # Framework detection
    if args.detect:
        from arc_tracing.detector import detect_frameworks
        
        print("\nDetected Frameworks:")
        frameworks = detect_frameworks()
        if frameworks:
            for framework in frameworks:
                print(f"  - {framework}")
        else:
            print("  No frameworks detected.")

def upload_command(args: argparse.Namespace) -> None:
    """Upload trace files to the Arc platform."""
    # Create uploader
    uploader = BatchUploader(
        export_dir=args.dir,
        endpoint=args.endpoint,
        api_key=args.api_key,
    )
    
    # Upload specific file or all files
    if args.file:
        # Upload specific file
        print(f"Uploading file: {args.file}")
        success = uploader.upload_file(args.file)
        if success:
            print("Upload successful!")
        else:
            print("Upload failed.")
    else:
        # Upload all files
        trace_files = uploader.list_trace_files()
        if not trace_files:
            print(f"No trace files found in {args.dir or './arc_traces'}")
            return
        
        print(f"Found {len(trace_files)} trace files. Starting upload...")
        results = uploader.upload_all()
        
        # Print results
        success_count = sum(1 for success in results.values() if success)
        print(f"Upload complete: {success_count}/{len(results)} files successfully uploaded.")
        
        if success_count < len(results):
            print("\nFailed uploads:")
            for file_path, success in results.items():
                if not success:
                    print(f"  - {file_path}")

def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        prog="arc-tracing",
        description="Arc Tracing SDK - Trace and optimize AI agents",
    )
    
    parser.add_argument(
        "--version", "-v", action="store_true", help="Show version and exit"
    )
    
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--config", "-c", help="Path to configuration file"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Init command
    init_parser = subparsers.add_parser(
        "init", help="Initialize a new project with Arc Tracing"
    )
    init_parser.add_argument(
        "--output-path", "-o", help="Path for configuration file"
    )
    init_parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite existing configuration"
    )
    
    # Proxy command
    proxy_parser = subparsers.add_parser(
        "proxy", help="Start the proxy server for API interception"
    )
    proxy_parser.add_argument(
        "--host", default="127.0.0.1", help="Host to bind the proxy server to"
    )
    proxy_parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind the proxy server to"
    )
    
    # Environment command
    env_parser = subparsers.add_parser(
        "env", help="Set up environment variables for proxy"
    )
    env_parser.add_argument(
        "--host", default="127.0.0.1", help="Proxy server host"
    )
    env_parser.add_argument(
        "--port", type=int, default=8000, help="Proxy server port"
    )
    env_parser.add_argument(
        "--shell", choices=["bash", "powershell"], 
        help="Generate shell commands to set environment variables"
    )
    
    # Info command
    info_parser = subparsers.add_parser(
        "info", help="Display information about the SDK"
    )
    info_parser.add_argument(
        "--detect", "-d", action="store_true", help="Detect frameworks in current environment"
    )
    
    # Upload command
    upload_parser = subparsers.add_parser(
        "upload", help="Upload trace files to the Arc platform"
    )
    upload_parser.add_argument(
        "--dir", "-d", help="Directory containing trace files to upload"
    )
    upload_parser.add_argument(
        "--file", "-f", help="Specific trace file to upload"
    )
    upload_parser.add_argument(
        "--endpoint", help="Override API endpoint for upload"
    )
    upload_parser.add_argument(
        "--api-key", help="Override API key for upload"
    )
    
    # Parse arguments
    args = parser.parse_args(argv)
    
    # Configure logging
    configure_logging(args.verbose)
    
    # Apply configuration file if specified
    if args.config:
        get_config(args.config)
    
    # Show version and exit
    if args.version:
        print(f"Arc Tracing SDK v{get_version()}")
        return 0
    
    # Run command
    if args.command == "init":
        init_command(args)
    elif args.command == "proxy":
        proxy_command(args)
    elif args.command == "env":
        env_command(args)
    elif args.command == "info":
        info_command(args)
    elif args.command == "upload":
        upload_command(args)
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())