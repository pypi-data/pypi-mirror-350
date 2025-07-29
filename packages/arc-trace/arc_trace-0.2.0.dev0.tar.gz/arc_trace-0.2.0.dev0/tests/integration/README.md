# Arc Tracing SDK Integration Tests

This directory contains tests for verifying the integration between the Arc Tracing SDK and the Arc RewardLab backend server.

The tests are designed to help you validate that your Arc Tracing SDK is correctly configured to communicate with the backend, using the proper endpoint, authentication, and trace formatting.

## Backend Discovery Tool

If you're not sure which endpoint or authentication method to use with your backend server, the discovery tool can help:

```bash
# Basic usage - discovers endpoints on localhost:8000
./discover_backend.py

# Specify a different base URL
./discover_backend.py --base-url "https://your-backend.example.com"

# Use a specific API key for authentication tests
./discover_backend.py --api-key "your_api_key"

# Disable SSL verification for self-signed certificates
./discover_backend.py --insecure

# Enable debug logging
./discover_backend.py --debug
```

The tool will test various endpoint paths and authentication methods and recommend a configuration for your backend.

## Backend Integration Test

The `test_backend_integration.py` script sends test traces to the backend server to verify connectivity and proper trace handling.

### Usage

```bash
# Basic usage - connects to local backend server
python test_backend_integration.py

# Connect to a specific backend URL
python test_backend_integration.py --backend-url "https://your-backend.example.com/api/v1/traces/"

# Use a specific API key
python test_backend_integration.py --api-key "your_api_key"

# Export traces to local files in addition to sending them to the backend
python test_backend_integration.py --local-export --export-dir "./my_traces"

# Disable SSL verification for testing (not recommended for production)
python test_backend_integration.py --insecure

# Use different authentication methods
python test_backend_integration.py --auth-method header --api-key "your_token" --auth-header "X-API-Key"  # Default: X-API-Key: your_token
python test_backend_integration.py --auth-method bearer --api-key "your_token"  # Authorization: Bearer your_token
python test_backend_integration.py --auth-method basic --api-key "username:password"  # Authorization: Basic (base64 encoded)
python test_backend_integration.py --auth-method none  # No authentication header

# Configure timeout and retries
python test_backend_integration.py --timeout 60 --retries 3  # Longer timeout (60s) with 3 retry attempts

# Enable local file fallback (enabled by default)
python test_backend_integration.py --local-export

# Disable local file fallback
python test_backend_integration.py --no-local-export

# Add project and agent identification (must be UUIDs or will be converted to UUIDs)
python test_backend_integration.py --project-id "123e4567-e89b-12d3-a456-426614174000" --agent-id "123e4567-e89b-12d3-a456-426614174001"

# Use a custom test query
python test_backend_integration.py --query "What is the capital of France?"
```

### Troubleshooting Backend Connection Issues

If you encounter connection issues:

- **401/403 Forbidden**: 
  1. Verify that your API key is correct and has permission to write traces
  2. Check that you're using the correct authentication method (default is X-API-Key header)
  3. Ensure the header name matches what the backend expects

- **404 Not Found**:
  1. Double-check the endpoint URL format (should end with `/api/v1/traces/`)
  2. Verify that the backend server is running and the route exists

- **422 Unprocessable Entity**:
  1. Ensure your project_id and agent_id are valid UUIDs or can be converted to UUIDs
  2. Check the trace format is correct (see BACKEND_INTEGRATION.md)
  3. Look for span_id formatting issues

For SSL certificate issues:
- Use the `--insecure` flag for testing with self-signed certificates
- For production, ensure proper SSL certificates are installed on the server

### Local File Export

If you're having issues with the backend connection, you can use the local file export option to save traces locally:

```bash
python test_backend_integration.py --local-export
```

This will create trace files in the `./arc_traces` directory that you can manually examine.

## Additional Integration Tests

More integration tests will be added to this directory as the SDK evolves.

## Running All Integration Tests

To run all integration tests:

```bash
# From the project root
python -m pytest tests/integration
```