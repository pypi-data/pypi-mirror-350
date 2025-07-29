"""Arc platform trace exporter."""

import json
import logging
import requests
import uuid
from typing import Dict, List, Optional, Sequence, Union
from uuid import UUID

from arc_tracing.exporters.helper import format_trace_for_backend

from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.trace import Status, StatusCode

from arc_tracing.config import get_config

# Configure logger
logger = logging.getLogger("arc_tracing")

class ArcExporter(SpanExporter):
    """
    OpenTelemetry exporter for sending traces to the Arc platform.
    
    This exporter sends trace data to the Arc platform's trace API endpoint.
    It handles authentication, data formatting, and error handling.
    """
    
    def __init__(self, 
        endpoint: Optional[str] = None, 
        api_key: Optional[str] = None, 
        project_id: Optional[Union[str, UUID]] = None,
        agent_id: Optional[Union[str, UUID]] = None,
        debug_mode: bool = False, 
        verify_ssl: bool = True,
        auth_method: str = "header",  # Options: "bearer", "basic", "header", "none"
        auth_header_name: str = "X-API-Key",
        timeout: int = 30,  # Connection timeout in seconds
        max_retries: int = 2,  # Number of retries on connection failure
        local_fallback: bool = True,  # Whether to use local file fallback
        extra_headers: Optional[Dict[str, str]] = None  # Additional headers to include in requests
    ):
        """
        Initialize the Arc platform exporter.
        
        Args:
            endpoint: The API endpoint for the Arc platform trace service.
                If None, loads from configuration.
            api_key: The API key for authentication with the Arc platform.
                If None, loads from configuration.
        """
        self._config = get_config()
        self._endpoint = endpoint or self._config.endpoint or "http://localhost:8000/api/v1/traces"
        self._api_key = api_key or self._config.api_key or "dev_arc_rewardlab_key"
        self._project_id = project_id or self._config.project_id
        self._agent_id = agent_id or self._config.agent_id
        self._debug_mode = debug_mode
        self._verify_ssl = verify_ssl
        self._auth_method = auth_method.lower()
        self._auth_header_name = auth_header_name
        self._timeout = timeout
        self._max_retries = max_retries
        self._local_fallback = local_fallback
        self._extra_headers = extra_headers or {}
        
        # Initialize local file exporter if fallback is enabled
        self._local_exporter = None
        
        if self._local_fallback:
            try:
                from .local_exporter import LocalFileExporter
                
                # Use local file as fallback
                export_dir = self._config.export_dir or "./arc_traces"
                self._local_exporter = LocalFileExporter(export_dir=export_dir)
                
                logger.info(f"Local file fallback initialized (dir: {export_dir})")
            except ImportError as e:
                logger.warning(f"Could not initialize local file fallback: {e}")
                self._local_exporter = None
        
        if not self._endpoint:
            logger.warning("No endpoint configured for ArcExporter. Traces will not be sent.")
        
        if not self._api_key:
            logger.warning("No API key configured for ArcExporter. Authentication will fail.")
    
    def export(self, spans: Sequence[ReadableSpan]) -> None:
        """
        Export spans to the Arc platform.
        
        Args:
            spans: The spans to export.
        """
        if not self._endpoint or not self._api_key:
            return
        
        try:
            # Convert spans to Arc format
            formatted_spans = self._format_spans(spans)
            
            # Send to API
            self._send_spans(formatted_spans)
        except Exception as e:
            logger.error(f"Failed to export spans: {e}")
    
    def _format_spans(self, spans: Sequence[ReadableSpan]) -> List[Dict]:
        """
        Internal method to format OpenTelemetry spans to a standardized format.
        
        Args:
            spans: The spans to format
            
        Returns:
            A list of formatted span dictionaries
        """
        """
        Format spans for the Arc platform API.
        
        Args:
            spans: The spans to format.
            
        Returns:
            A list of formatted span dictionaries.
        """
        formatted_spans = []
        
        for span in spans:
            # Base span data
            formatted_span = {
                "name": span.name,
                "context": {
                    "trace_id": span.context.trace_id if isinstance(span.context.trace_id, str) else format(span.context.trace_id, 'x'),
                    "span_id": span.context.span_id if isinstance(span.context.span_id, str) else format(span.context.span_id, 'x'),
                    "is_remote": span.context.is_remote if hasattr(span.context, "is_remote") else False,
                },
                "parent_id": (span.parent.span_id if isinstance(span.parent.span_id, str) else format(span.parent.span_id, 'x')) if span.parent else None,
                "start_time": span.start_time,
                "end_time": span.end_time,
                "status": {
                    "status_code": span.status.status_code.value if hasattr(span.status.status_code, "value") else span.status.status_code,
                    "description": span.status.description,
                },
                "attributes": dict(span.attributes),
                "events": [
                    {
                        "name": event.name,
                        "timestamp": event.timestamp,
                        "attributes": dict(event.attributes),
                    }
                    for event in span.events
                ],
                "links": [
                    {
                        "context": {
                            "trace_id": link.context.trace_id if isinstance(link.context.trace_id, str) else format(link.context.trace_id, 'x'),
                            "span_id": link.context.span_id if isinstance(link.context.span_id, str) else format(link.context.span_id, 'x'),
                        },
                        "attributes": dict(link.attributes),
                    }
                    for link in span.links
                ],
            }
            
            formatted_spans.append(formatted_span)
        
        return formatted_spans
    
    def _send_spans(self, formatted_spans: List[Dict]) -> None:
        """
        Send formatted spans to the Arc platform API.
        
        Args:
            formatted_spans: The formatted spans to send.
        """
        if not formatted_spans:
            return
        
        # Initialize headers with content type and SDK version
        headers = {
            "Content-Type": "application/json",
            "X-ARC-SDK-Version": "0.1.0"
        }
        
        # Add any extra headers
        headers.update(self._extra_headers)
        
        # Add authentication based on the configured method
        if self._auth_method == "bearer" and self._api_key:
            headers[self._auth_header_name] = f"Bearer {self._api_key}"
        elif self._auth_method == "basic" and self._api_key:
            import base64
            # For basic auth, api_key should be in the format "username:password"
            auth_bytes = self._api_key.encode('ascii')
            base64_bytes = base64.b64encode(auth_bytes)
            headers[self._auth_header_name] = f"Basic {base64_bytes.decode('ascii')}"
        elif self._auth_method == "header" and self._api_key:
            # Just use the raw API key as the header value
            headers[self._auth_header_name] = self._api_key
        # If auth_method is "none" or api_key is not provided, no auth header is added
        
        # Format the trace data using the helper function
        data = format_trace_for_backend(
            formatted_spans=formatted_spans,
            project_id=self._project_id,
            agent_id=self._agent_id
        )
        
        # Add optional fields if available, ensuring they're valid UUIDs
        if self._project_id:
            try:
                # If it's already a UUID, use it directly
                if isinstance(self._project_id, UUID):
                    data["project_id"] = str(self._project_id)
                else:
                    # Try to parse as UUID or create a deterministic UUID from the string
                    try:
                        # Try to parse as a UUID string first
                        data["project_id"] = str(UUID(self._project_id))
                    except ValueError:
                        # If not a valid UUID string, create a deterministic UUID from it
                        data["project_id"] = str(uuid.uuid5(uuid.NAMESPACE_OID, str(self._project_id)))
            except Exception as e:
                logger.warning(f"Could not use project_id as UUID: {e}")
                
        if self._agent_id:
            try:
                # If it's already a UUID, use it directly
                if isinstance(self._agent_id, UUID):
                    data["agent_id"] = str(self._agent_id)
                else:
                    # Try to parse as UUID or create a deterministic UUID from the string
                    try:
                        # Try to parse as a UUID string first
                        data["agent_id"] = str(UUID(self._agent_id))
                    except ValueError:
                        # If not a valid UUID string, create a deterministic UUID from it
                        data["agent_id"] = str(uuid.uuid5(uuid.NAMESPACE_OID, str(self._agent_id)))
            except Exception as e:
                logger.warning(f"Could not use agent_id as UUID: {e}")
            
        # Check if metrics exists before accessing it
        metrics = data.get("metrics", {})
        if metrics:
            data["metrics"] = metrics
        
        try:
            # Log the request details if in debug mode
            if self._debug_mode:
                logger.debug(f"Sending request to {self._endpoint}")
                logger.debug(f"Headers: {headers}")
                logger.debug(f"Data sample: {json.dumps(data)[:500]}...")
            
            # Set up retry logic according to backend recommendations
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry
            
            session = requests.Session()
            if self._max_retries > 0:
                # Only retry on server errors (500s), not on client errors (400s)
                retry_strategy = Retry(
                    total=self._max_retries,
                    backoff_factor=0.5,  # Exponential backoff
                    status_forcelist=[500, 502, 503, 504],  # Only retry on server errors
                    allowed_methods=["POST"],
                    respect_retry_after_header=True
                )
                adapter = HTTPAdapter(max_retries=retry_strategy)
                session.mount("http://", adapter)
                session.mount("https://", adapter)
            
            # Make the request with the configured session
            response = session.post(
                self._endpoint,
                headers=headers,
                json=data,
                timeout=self._timeout,
                verify=self._verify_ssl  # Use SSL verification setting
            )
            
            # Handle different status codes based on backend recommendations
            if response.status_code >= 400:
                # Log the error with appropriate detail level
                if response.status_code == 401:
                    logger.error(f"Authentication failed: Missing or invalid API key (401)")
                elif response.status_code == 403:
                    logger.error(f"Authorization failed: Insufficient permissions for this API key (403)")
                elif response.status_code == 404:
                    logger.error(f"Resource not found: Check endpoint URL {self._endpoint} (404)")
                elif response.status_code == 422:
                    logger.error(f"Validation error: The trace format is invalid (422) - {response.text}")
                elif response.status_code >= 500:
                    logger.error(f"Server error: The backend encountered an error (500) - {response.text}")
                else:
                    logger.error(f"Failed to send traces: {response.status_code} {response.text}")
                
                # Log more details for debugging
                if self._debug_mode:
                    logger.debug(f"Request details - URL: {self._endpoint}, Headers: {headers}, Data size: {len(json.dumps(data))} bytes")
                    if response.status_code == 422:
                        logger.debug(f"Trace data sample: {json.dumps(data)[:1000]}...")
                
                # Only try fallback for server errors or when explicitly enabled
                use_fallback = self._local_fallback and (
                    response.status_code >= 500 or  # Server errors
                    response.status_code == 0 or    # Connection error
                    self._debug_mode                # When in debug mode, always allow fallback for testing
                )
                
                if use_fallback and self._local_exporter:
                    try:
                        logger.info(f"API request failed with status {response.status_code}, falling back to local file export")
                        self._local_exporter.export(spans)
                        return
                    except Exception as file_err:
                        logger.error(f"Local file fallback failed: {file_err}")
            else:
                logger.debug(f"Successfully sent {len(formatted_spans)} spans to Arc platform")
        
        except Exception as e:
            logger.error(f"Error sending spans to Arc platform: {e}")
            
            # For connection errors, always use fallback if enabled
            if self._local_fallback and self._local_exporter:
                try:
                    logger.info("API connection failed, falling back to local file export")
                    self._local_exporter.export(spans)
                    logger.info(f"Successfully exported to local file (offline mode)")
                    return
                except Exception as file_err:
                    logger.error(f"Local file fallback failed: {file_err}")
    
    def shutdown(self) -> None:
        """Shut down the exporter and any fallback exporters."""
        # Clean up local file exporter
        if self._local_fallback and self._local_exporter:
            try:
                self._local_exporter.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down local file exporter: {e}")