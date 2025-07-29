# Arc RewardLab Backend Integration Example

This example demonstrates how to properly integrate the Arc Tracing SDK with the Arc RewardLab backend server.

This directory contains up-to-date examples that show the recommended integration patterns for connecting with the Arc backend platform.

## Features Demonstrated

- Setting up the SDK with the correct endpoint and authentication
- Configuring trace formatting to match the backend's expected model
- Working with project and agent identifiers
- Using local file fallback for offline scenarios
- Batch uploading locally stored traces

## Configuration

The example is configured to work with the Arc RewardLab backend running locally, but you can customize it with the following options:

```bash
# Run with default settings (local backend)
python example_integration.py

# Specify a different backend endpoint
python example_integration.py --endpoint "https://api.arc-rewardlab.dev/api/v1/traces"

# Use a specific API key
python example_integration.py --api-key "your_api_key"

# Set project and agent identifiers
python example_integration.py --project-id "prod-project-123" --agent-id "agent-456"

# Custom query for testing
python example_integration.py --query "What is reinforcement learning?"

# Upload any previously stored local traces
python example_integration.py --upload-traces
```

## Integration Details

### Authentication

The example uses X-API-Key header authentication with the default development key:

```python
arc_exporter = ArcExporter(
    endpoint=endpoint,
    api_key=api_key,
    auth_method="header",
    auth_header_name="X-API-Key"
)
```

For more details on authentication methods and options, see the `BACKEND_INTEGRATION.md` file in the root directory.

### Trace Format

The SDK formats traces to match the expected `TraceCreate` model used by the backend:

```
{
    "project_id": "example-project-001",  # Optional
    "agent_id": "example-agent-001",      # Optional
    "input": {
        "query": "What are the key challenges in AI?",
        "type": "text"
    },
    "output": {
        "response": "This is a response...",
        "type": "text"
    },
    "steps": [...],  # Detailed execution steps from spans
    "metrics": {...}  # Performance metrics
}
```

### Local Fallback

If the backend is unavailable, traces are automatically stored locally:

```python
arc_exporter = ArcExporter(
    # ... other settings
    local_fallback=True  # Enable local file storage fallback
)
```

### Batch Upload

The example shows how to upload locally stored traces to the backend:

```python
uploader = BatchUploader(
    export_dir="./arc_traces",
    endpoint=endpoint,
    api_key=api_key
)
results = uploader.upload_all()
```

## Running with the Local Backend

To run this example with a local backend:

1. Start the backend server:
   ```bash
   # In your backend repository
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Run the example:
   ```bash
   python example_integration.py
   ```

3. Check the backend logs to verify that traces are being received.

## Troubleshooting

If you encounter issues with the backend integration:

- **403 Forbidden**: Check that the API key is correct and the X-API-Key header is being properly sent
- **404 Not Found**: Verify the endpoint URL is correct
- **422 Unprocessable Entity**: Ensure the trace format matches what the backend expects
  - Note that `project_id` and `agent_id` must be valid UUIDs (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
  - The SDK automatically converts non-UUID strings to valid UUIDs
- **500 Server Error**: Check the backend logs for more details about the error
- **Connection Error**: Make sure the backend server is running and reachable
- **span_id errors**: If you see errors related to span_id formatting, ensure you're using the latest version of the SDK that handles span IDs correctly

See the `BACKEND_INTEGRATION.md` file for a comprehensive troubleshooting guide.

### UUID Handling

The backend requires `project_id` and `agent_id` to be valid UUIDs. The SDK handles this by:

1. Using UUIDs directly if provided in the correct format
2. Attempting to parse string values as UUIDs
3. Generating deterministic UUIDs from non-UUID strings using the uuid5 algorithm

For best results, use proper UUID strings such as `"123e4567-e89b-12d3-a456-426614174000"`

Using `--upload-traces` can be helpful if there were connectivity issues during initial testing.