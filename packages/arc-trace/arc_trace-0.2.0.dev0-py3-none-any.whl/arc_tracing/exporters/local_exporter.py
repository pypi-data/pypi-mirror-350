"""Local file exporter for offline use."""

import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Sequence

from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.trace import Status, StatusCode

from arc_tracing.config import get_config
from arc_tracing.exporters.helper import format_trace_for_backend

# Configure logger
logger = logging.getLogger("arc_tracing")

class LocalFileExporter(SpanExporter):
    """
    OpenTelemetry exporter that saves traces to local files.
    
    This exporter is useful for offline use or when you want to
    save traces locally before uploading them to the Arc platform.
    """
    
    def __init__(self, 
                 export_dir: Optional[str] = None,
                 max_file_size_mb: int = 10,
                 use_timestamps: bool = True):
        """
        Initialize the local file exporter.
        
        Args:
            export_dir: Directory to save trace files in.
                If None, uses "./arc_traces" in the current directory.
            max_file_size_mb: Maximum file size in megabytes before rotating.
            use_timestamps: Whether to include timestamps in filenames.
        """
        self._config = get_config()
        self._export_dir = export_dir or "./arc_traces"
        self._max_file_size_bytes = max_file_size_mb * 1024 * 1024
        self._use_timestamps = use_timestamps
        self._current_file_path = None
        self._current_file_size = 0
        
        # Create export directory if it doesn't exist
        os.makedirs(self._export_dir, exist_ok=True)
        
        # Create a new file
        self._create_new_file()
    
    def _create_new_file(self) -> None:
        """Create a new file for trace export."""
        # Generate filename with timestamp if enabled
        if self._use_timestamps:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"arc_traces_{timestamp}.jsonl"
        else:
            # Find next available file number
            i = 1
            while os.path.exists(os.path.join(self._export_dir, f"arc_traces_{i}.jsonl")):
                i += 1
            filename = f"arc_traces_{i}.jsonl"
        
        self._current_file_path = os.path.join(self._export_dir, filename)
        self._current_file_size = 0
        
        logger.info(f"Created new trace file: {self._current_file_path}")
    
    def export(self, spans: Sequence[ReadableSpan]) -> None:
        """
        Export spans to a local file.
        
        Args:
            spans: The spans to export.
        """
        if not spans:
            return
        
        try:
            # Check if we need to rotate the file
            if (self._current_file_size > self._max_file_size_bytes):
                self._create_new_file()
            
            # Convert spans to JSON lines
            lines = []
            for span in spans:
                # Format span data
                span_data = self._format_span(span)
                
                # Convert to JSON string and add newline
                line = json.dumps(span_data) + "\n"
                lines.append(line)
            
            # Write to file
            with open(self._current_file_path, "a") as f:
                for line in lines:
                    f.write(line)
                    self._current_file_size += len(line.encode("utf-8"))
            
            logger.debug(f"Exported {len(spans)} spans to {self._current_file_path}")
        
        except Exception as e:
            logger.error(f"Failed to export spans to local file: {e}")
    
    def _format_span(self, span: ReadableSpan) -> Dict:
        """
        Format a span for JSON serialization.
        
        Args:
            span: The span to format.
            
        Returns:
            A dictionary with formatted span data.
        """
        # Format events
        events = []
        for event in span.events:
            events.append({
                "name": event.name,
                "timestamp": event.timestamp,
                "attributes": dict(event.attributes),
            })
        
        # Format links
        links = []
        for link in span.links:
            links.append({
                "context": {
                    "trace_id": link.context.trace_id if isinstance(link.context.trace_id, str) else format(link.context.trace_id, 'x'),
                    "span_id": link.context.span_id if isinstance(link.context.span_id, str) else format(link.context.span_id, 'x'),
                },
                "attributes": dict(link.attributes),
            })
        
        # Format the span
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
            "events": events,
            "links": links,
            "metadata": {
                "exported_time": int(time.time() * 1_000_000_000),
                "sdk_version": "0.1.0",
            }
        }
        
        return formatted_span
    
    def shutdown(self) -> None:
        """Shut down the exporter."""
        logger.info(f"Local file exporter shutdown. Traces saved to {self._export_dir}")


class BatchUploader:
    """
    Utility for uploading previously saved trace files to the Arc platform.
    
    This class can be used to upload trace files created by the LocalFileExporter
    to the Arc platform at a later time.
    """
    
    def __init__(self, 
                 export_dir: Optional[str] = None,
                 endpoint: Optional[str] = None,
                 api_key: Optional[str] = None):
        """
        Initialize the batch uploader.
        
        Args:
            export_dir: Directory containing trace files.
                If None, uses "./arc_traces" in the current directory.
            endpoint: The API endpoint for the Arc platform trace service.
                If None, loads from configuration.
            api_key: The API key for authentication with the Arc platform.
                If None, loads from configuration.
        """
        self._config = get_config()
        self._export_dir = export_dir or "./arc_traces"
        self._endpoint = endpoint or self._config.endpoint
        self._api_key = api_key or self._config.api_key
    
    def list_trace_files(self) -> List[str]:
        """
        List available trace files in the export directory.
        
        Returns:
            A list of file paths to trace files.
        """
        if not os.path.exists(self._export_dir):
            return []
        
        return [
            os.path.join(self._export_dir, filename)
            for filename in os.listdir(self._export_dir)
            if filename.endswith(".jsonl")
        ]
    
    def upload_file(self, file_path: str) -> bool:
        """
        Upload a trace file to the Arc platform.
        
        Args:
            file_path: Path to the trace file to upload.
            
        Returns:
            True if upload was successful, False otherwise.
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
        
        try:
            import requests
            
            # Read the file
            traces = []
            with open(file_path, "r") as f:
                for line in f:
                    try:
                        trace_data = json.loads(line.strip())
                        # Convert to proper trace format if needed
                        if "spans" in trace_data:
                            # This is a raw span data from local storage
                            # We need to convert it to the proper trace format
                            formatted_data = format_trace_for_backend([trace_data])
                            traces.append(formatted_data)
                        else:
                            # Already in proper format
                            traces.append(trace_data)
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON in file {file_path}: {line}")
                    except Exception as e:
                        logger.warning(f"Error processing trace in file {file_path}: {e}")
            
            if not traces:
                logger.warning(f"No valid traces found in file {file_path}")
                return False
            
            # Prepare the API request
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": self._api_key,  # Use X-API-Key header
            }
            
            # Use the batch endpoint for multiple traces
            endpoint = self._endpoint
            if len(traces) > 1 and not endpoint.endswith("/batch"):
                endpoint = endpoint.rstrip("/") + "/batch"
                
            # For batch endpoint, send array of traces
            # For single trace endpoint, send the trace directly
            data = traces if len(traces) > 1 else traces[0]
            
            # Send the request
            response = requests.post(
                self._endpoint,
                headers=headers,
                json=data,
                timeout=60,
            )
            
            if response.status_code >= 400:
                logger.error(f"Failed to upload file {file_path} to Arc platform: {response.status_code} {response.text}")
                return False
            
            logger.info(f"Successfully uploaded {len(traces)} traces from {file_path} to Arc platform")
            return True
        
        except Exception as e:
            logger.error(f"Error uploading file {file_path} to Arc platform: {e}")
            return False
    
    def upload_all(self) -> Dict[str, bool]:
        """
        Upload all trace files to the Arc platform.
        
        Returns:
            A dictionary mapping file paths to upload success status.
        """
        trace_files = self.list_trace_files()
        results = {}
        
        for file_path in trace_files:
            results[file_path] = self.upload_file(file_path)
        
        return results