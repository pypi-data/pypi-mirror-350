"""Arc Tracing SDK - Lightweight, framework-agnostic Python SDK for AI agent tracing."""

from arc_tracing.trace import trace_agent
from arc_tracing.integrations import enable_arc_tracing

try:
    from arc_tracing._version import __version__
except ImportError:
    __version__ = "0.1.0"

__all__ = ["trace_agent", "enable_arc_tracing", "__version__"]