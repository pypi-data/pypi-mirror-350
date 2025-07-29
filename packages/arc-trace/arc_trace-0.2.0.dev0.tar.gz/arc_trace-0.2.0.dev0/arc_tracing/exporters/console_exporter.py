"""Console trace exporter for debugging."""

import json
import logging
from typing import Dict, List, Sequence

from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.sdk.trace import ReadableSpan

# Configure logger
logger = logging.getLogger("arc_tracing")

class ConsoleExporter(SpanExporter):
    """
    OpenTelemetry exporter that prints spans to the console.
    
    This exporter is useful for debugging and development purposes.
    It formats spans in a human-readable format and prints them
    to the console.
    """
    
    def export(self, spans: Sequence[ReadableSpan]) -> None:
        """
        Export spans to the console.
        
        Args:
            spans: The spans to export.
        """
        for span in spans:
            # Format and print span
            formatted_span = self._format_span(span)
            print(f"\n--- SPAN: {span.name} ---")
            print(json.dumps(formatted_span, indent=2))
            print("-------------------\n")
    
    def _format_span(self, span: ReadableSpan) -> Dict:
        """
        Format a span for console output.
        
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
        
        # Format the span
        formatted_span = {
            "name": span.name,
            "trace_id": span.context.trace_id if isinstance(span.context.trace_id, str) else hex(span.context.trace_id),
            "span_id": span.context.span_id if isinstance(span.context.span_id, str) else hex(span.context.span_id),
            "parent_id": (span.parent.span_id if isinstance(span.parent.span_id, str) else hex(span.parent.span_id)) if span.parent else None,
            "start_time": span.start_time,
            "end_time": span.end_time,
            "duration_ms": (span.end_time - span.start_time) / 1_000_000,  # nanoseconds to milliseconds
            "status": {
                "code": span.status.status_code.name if hasattr(span.status.status_code, "name") else str(span.status.status_code),
                "description": span.status.description,
            },
            "attributes": dict(span.attributes),
            "events": events,
        }
        
        return formatted_span
    
    def shutdown(self) -> None:
        """Shut down the exporter."""
        pass  # No resources to clean up