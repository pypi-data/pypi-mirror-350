"""AEP-OTEL Python SDK

This SDK provides tools to automatically instrument applications built with popular
LLM libraries like OpenAI to emit Attention-Event-Protocol (AEP) compliant
OpenTelemetry spans.

It allows for tracing of LLM interactions, retrieval stages, and potentially
human attention signals, providing deep visibility into your AI systems.

Basic Usage:

To automatically patch the OpenAI library:

```python
from aep_otel import patch_openai, unpatch_openai

# Apply the AEP instrumentation
patch_openai()

# ... your OpenAI API calls ...

# Clean up (optional, typically at application shutdown)
# unpatch_openai()
```

Traces will be emitted based on your OpenTelemetry SDK configuration
(e.g., to console, OTLP exporter).
"""

__version__ = "0.0.1a0"

from .tracing import get_tracer, get_tracer_provider
from .hooks import patch_openai, unpatch_openai

__all__ = [
    "__version__",
    "get_tracer",
    "get_tracer_provider",
    "patch_openai",
    "unpatch_openai",
] 