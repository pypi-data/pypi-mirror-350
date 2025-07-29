# Local Development Environment Setup

This guide explains how to set up a local development environment to test the Arc Tracing SDK with a local backend.

## 1. Install the SDK in Development Mode

To use the SDK without publishing it, install it in development mode:

```bash
# From the arc-tracing-sdk directory
pip install -e .
```

This will install the package in "editable" mode, so any changes you make to the code will be immediately reflected without needing to reinstall.

## 2. Configure Local Backend Settings

### Discover Backend Endpoints

First, use the built-in discovery tool to find the correct endpoint and authentication method for your backend:

```bash
# From the arc-tracing-sdk directory
./tests/integration/discover_backend.py --base-url "http://localhost:8000" --api-key "dev_arc_rewardlab_key"
```

The tool will test various endpoints and authentication methods and recommend a configuration.

### Create Configuration File

Create a local configuration file that points to your development backend using the discovered settings:

```bash
# Create a local dev configuration
cat > local_dev_config.yml << EOL
trace:
  frameworks: "auto"
  detail_level: "comprehensive"
  # Point to your local backend
  endpoint: "http://localhost:8000/api/v1/traces"
  # Authentication for local dev
  auth:
    api_key: "dev_arc_rewardlab_key"  # This must match your backend's expected API key
    method: "header"  # Use header-based authentication
    header: "X-API-Key"  # Use X-API-Key header
  # Optional project and agent identifiers
  project_id: "dev-project-001"  # Optional project identifier
  agent_id: "dev-agent-001"     # Optional agent identifier
  
  # Configure fallback mechanism
  fallback:
    enabled: true  # Enable fallback mechanism
    local_file:
      enabled: true
      directory: "./arc_traces"
EOL
```

### Authentication Issues

If you encounter a 403 Forbidden error when connecting to the backend:

1. Verify that you're using the correct API key for your backend environment
2. Check that the backend is configured to accept the API key format being sent
3. The SDK sends the API key in the format: `Authorization: Bearer dev_key`
4. Ensure your backend server is validating this format correctly

You can use the `--insecure` flag with the integration test to bypass SSL verification if needed during development.

## 3. MongoDB Setup with Docker

If you don't have MongoDB running, you can quickly set one up with Docker:

```bash
# Pull and run MongoDB
docker pull mongodb/mongodb-community-server:latest
docker run --name mongodb -d -p 27017:27017 mongodb/mongodb-community-server:latest
```

## 4. Test End-to-End Integration

Create a simple test script to verify the integration:

```python
# test_integration.py
import os
from arc_tracing import trace_agent
from arc_tracing.exporters import ArcExporter, ConsoleExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Set up the tracer to use both console and Arc exporters
tracer_provider = TracerProvider()

# Console exporter for debugging
console_exporter = ConsoleExporter()
tracer_provider.add_span_processor(SimpleSpanProcessor(console_exporter))

# Arc exporter pointing to local backend
arc_exporter = ArcExporter(
    endpoint="http://localhost:5000/traces",
    api_key="dev_key"  # Not needed for local dev but required by the exporter
)
tracer_provider.add_span_processor(SimpleSpanProcessor(arc_exporter))

# Set the global tracer provider
trace.set_tracer_provider(tracer_provider)

# Create a simple test agent function
@trace_agent
def test_agent(query):
    """Simple test agent to verify tracing."""
    # Simulate a call to an LLM API
    response = f"This is a test response for: {query}"
    return response

# Run the test
if __name__ == "__main__":
    result = test_agent("Test query for local backend integration")
    print(f"Agent response: {result}")
    print("Check your backend server logs to verify the trace was received.")
    print("Check MongoDB to verify the trace was stored.")
```

## 5. Connect to Local Backend

Make sure your local backend server is running and properly configured to:
1. Accept traces at the `/traces` endpoint
2. Store them in the local MongoDB instance
3. Log received traces for debugging

## 6. Debug Tips

### Verifying Trace Export

To check if traces are being exported correctly:

```python
# Add this to your integration script
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Checking MongoDB Data

To verify traces are stored in MongoDB:

```bash
# Connect to MongoDB container
docker exec -it mongodb mongosh

# In mongosh
use arc_traces
db.traces.find().pretty()
```

### Testing with Local File Exporter

If you're having issues with the direct backend connection, you can use the local file exporter as an intermediate step:

```python
from arc_tracing.exporters import LocalFileExporter

# Set up local file export
local_exporter = LocalFileExporter(export_dir="./local_traces")
tracer_provider.add_span_processor(SimpleSpanProcessor(local_exporter))
```

Then manually check the generated trace files to verify they contain the expected data.

## 7. Integration Checklist

- [ ] SDK installed in development mode
- [ ] Local configuration created
- [ ] MongoDB running
- [ ] Backend server running and configured
- [ ] Test script executed successfully
- [ ] Traces visible in console output
- [ ] Traces received by backend (check logs)
- [ ] Traces stored in MongoDB
- [ ] Spans contain all required attributes

## 8. Local File Fallback

The SDK supports a local file fallback mechanism when the primary backend connection fails:

1. **API Endpoint**: First attempts to send traces to the configured HTTP endpoint
2. **Local Files**: If the API fails, traces are stored in local JSON files

This ensures your traces are never lost, even when the backend server is unavailable.

### Configuring Local Fallback

Local file fallback can be configured in your configuration file or environment variables:

```yaml
trace:
  # Rest of your configuration...
  fallback:
    enabled: true  # Set to false to disable fallback
    local_file:
      enabled: true
      directory: "./arc_traces"  # Directory to store trace files
```

Or through environment variables:

```bash
export ARC_FALLBACK_ENABLED=true
```

### Uploading Local Traces

You can use the BatchUploader to upload locally stored traces once the backend is available again:

```python
from arc_tracing.exporters import BatchUploader

# Initialize uploader
uploader = BatchUploader(
    export_dir="./arc_traces",
    endpoint="http://localhost:8000/api/v1/traces",
    api_key="dev_arc_rewardlab_key"
)

# Upload all traces
results = uploader.upload_all()

# Check results
for file_path, success in results.items():
    print(f"{file_path}: {'Success' if success else 'Failed'}")
```

## 9. Debugging Backend Issues

If you encounter issues with the backend integration:

### Enable Verbose Logging

To get detailed logs of the HTTP requests and responses:

```python
# Add to your test script or use the integration test with --debug flag
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.DEBUG)
```

### Test with Local File Export

If you're having trouble connecting to the backend, use local file export as an intermediate step:

```bash
python tests/integration/test_backend_integration.py --local-export
```

This will create trace files in the `./arc_traces` directory that you can inspect to ensure the trace format is correct.

### Common Issues and Solutions

| Issue | Possible Solutions |
|-------|--------------------|
| 403 Forbidden | • Verify API key is correct<br>• Check authorization header format<br>• Ensure backend is configured to accept your API key |
| Connection Error | • Verify backend server is running<br>• Check endpoint URL is correct<br>• Ensure no firewall blocking connections |
| SSL Certificate Error | • Use `--insecure` flag for testing<br>• Install proper certificates for production |
| Malformed Data | • Check trace format in local files<br>• Verify the backend expects the format being sent |