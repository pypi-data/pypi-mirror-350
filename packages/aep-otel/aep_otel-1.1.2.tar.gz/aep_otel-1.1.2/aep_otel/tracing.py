"""OpenTelemetry tracing setup for AEP.

This module provides a basic configuration for OpenTelemetry tracing.
By default, it exports spans to the console.
If OTEL_EXPORTER_OTLP_ENDPOINT is set, it will also attempt to export
via OTLP HTTP to that endpoint.
"""

import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as OTLPHTTPSpanExporter

# Service name can be configured via environment variable or a default
SERVICE_NAME = os.environ.get("AEP_SERVICE_NAME", "aep-python-app")
OTLP_ENDPOINT = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")

_tracer_provider = None

def get_tracer_provider() -> TracerProvider:
    """Returns the global tracer provider, initializing it if necessary."""
    global _tracer_provider
    if _tracer_provider is None:
        resource = Resource(attributes={"service.name": SERVICE_NAME})
        _tracer_provider = TracerProvider(resource=resource)

        # Always add ConsoleSpanExporter for local visibility / P-1 goal
        console_exporter = ConsoleSpanExporter()
        _tracer_provider.add_span_processor(BatchSpanProcessor(console_exporter))
        print("ConsoleSpanExporter initialized for AEP tracing.")

        # Add OTLP Exporter if an endpoint is configured
        if OTLP_ENDPOINT:
            try:
                # Ensure the endpoint path is explicitly /v1/traces
                traces_endpoint = f"{OTLP_ENDPOINT.rstrip('/')}/v1/traces"
                otlp_exporter = OTLPHTTPSpanExporter(endpoint=traces_endpoint)
                _tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
                print(f"OTLPHTTPSpanExporter initialized for AEP tracing, explicit endpoint: {traces_endpoint}")
            except Exception as e:
                print(f"Failed to initialize OTLPHTTPSpanExporter: {e}. Spans will only go to console.")
        else:
            print("OTEL_EXPORTER_OTLP_ENDPOINT not set. Spans will only go to console.")

        trace.set_tracer_provider(_tracer_provider)
    return _tracer_provider

def get_tracer(module_name: str) -> trace.Tracer:
    """Returns a tracer instance for the given module name."""
    provider = get_tracer_provider()
    return provider.get_tracer(module_name, "0.0.1a0") # Corresponds to package version 