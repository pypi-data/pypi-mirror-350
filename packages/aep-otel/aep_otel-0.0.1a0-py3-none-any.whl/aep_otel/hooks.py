"""Patches for external libraries (e.g., OpenAI) to emit AEP spans."""

import functools
import time
from typing import Any, Callable, TypeVar

import openai
from opentelemetry import trace
from opentelemetry.trace.status import StatusCode

from .tracing import get_tracer # Assuming tracing.py is in the same directory

F = TypeVar("F", bound=Callable[..., Any])

# Get a tracer for this module
tracer = get_tracer(__name__)

# Store the original method if openai is available
_original_openai_chatcompletion_create = None
if hasattr(openai, "resources") and hasattr(openai.resources, "chat") and hasattr(openai.resources.chat, "completions") and hasattr(openai.resources.chat.completions.Completions, "create"):
    _original_openai_chatcompletion_create = openai.resources.chat.completions.Completions.create

def _patched_openai_chatcompletion_create(*args: Any, **kwargs: Any) -> Any:
    """Patched version of OpenAI ChatCompletion.create to add AEP tracing."""
    if not _original_openai_chatcompletion_create:
        # Should not happen if patch_openai was called successfully
        raise RuntimeError("OpenAI ChatCompletion original method not found. Was it patched correctly?")

    # Start a new span
    with tracer.start_as_current_span(
        "llm.openai.chatcompletion", # Following Semantic Conventions for LLM
        kind=trace.SpanKind.CLIENT,
        attributes={ # Initial common attributes
            "aep.stage_id": "llm",
            # Per OTEL LLM conventions: https://opentelemetry.io/docs/specs/semconv/llms/llm-spans/
            "llm.vendor": "OpenAI",
            "llm.request.type": "chat"
        }
    ) as span:
        # Record request attributes
        model = kwargs.get("model")
        if model:
            span.set_attribute("llm.request.model", model)
        
        messages = kwargs.get("messages", [])
        if messages:
            # For privacy and brevity, consider summarizing or excluding in real scenarios
            span.set_attribute("llm.request.messages.count", len(messages))
            # Example of capturing the role of the first message, if it exists
            if len(messages) > 0 and isinstance(messages[0], dict) and "role" in messages[0]:
                 span.set_attribute("llm.request.messages.0.role", messages[0]["role"])

        # Add other request parameters as per OpenTelemetry LLM conventions
        # E.g., llm.request.temperature, llm.request.top_p, llm.request.max_tokens
        # These are omitted for brevity but should be added for comprehensive tracing.

        try:
            start_time = time.monotonic()
            response = _original_openai_chatcompletion_create(*args, **kwargs)
            end_time = time.monotonic()

            # Record successful response attributes from OpenAIObject
            if hasattr(response, "model"):
                 span.set_attribute("llm.response.model", response.model)
            if hasattr(response, "id"):
                span.set_attribute("llm.response.id", response.id)
            if hasattr(response, "choices") and response.choices:
                # Capturing finish reason of the first choice as an example
                if hasattr(response.choices[0], "finish_reason"):
                    span.set_attribute("llm.response.choices.0.finish_reason", response.choices[0].finish_reason)
            
            if hasattr(response, "usage") and response.usage:
                if hasattr(response.usage, "prompt_tokens"):
                    span.set_attribute("llm.usage.prompt_tokens", response.usage.prompt_tokens)
                if hasattr(response.usage, "completion_tokens"):
                    span.set_attribute("llm.usage.completion_tokens", response.usage.completion_tokens)
                if hasattr(response.usage, "total_tokens"):
                    span.set_attribute("llm.usage.total_tokens", response.usage.total_tokens)
            
            # AEP Core field: llm.cost_usd - Placeholder, actual cost calculation is complex
            # and depends on model, tokens, and potentially other factors.
            # This should be implemented based on OpenAI's pricing.
            span.set_attribute("aep.llm.cost_usd", 0.000) # Placeholder
            
            # Record duration
            duration_ms = (end_time - start_time) * 1000
            span.set_attribute("duration.ms", duration_ms) # Generic duration

            span.set_status(StatusCode.OK)
            return response
        except Exception as e:
            if span.is_recording():
                span.record_exception(e)
                span.set_status(StatusCode.ERROR, description=str(e))
            raise

def patch_openai() -> None:
    """Applies the patch to OpenAI client if not already patched."""
    global _original_openai_chatcompletion_create
    # Ensure original is fetched if not already
    if not _original_openai_chatcompletion_create and hasattr(openai, "resources") and hasattr(openai.resources, "chat") and hasattr(openai.resources.chat, "completions") and hasattr(openai.resources.chat.completions.Completions, "create"):
        _original_openai_chatcompletion_create = openai.resources.chat.completions.Completions.create

    if not _original_openai_chatcompletion_create:
        print("Failed to patch OpenAI: ChatCompletion.create method not found.")
        return

    if openai.resources.chat.completions.Completions.create != _patched_openai_chatcompletion_create:
        openai.resources.chat.completions.Completions.create = _patched_openai_chatcompletion_create
        print("OpenAI ChatCompletion patched for AEP tracing.")
    else:
        print("OpenAI ChatCompletion already patched.")

def unpatch_openai() -> None:
    """Removes the patch from OpenAI client if it was patched."""
    if not _original_openai_chatcompletion_create:
        print("Cannot unpatch OpenAI: Original method not available.")
        return

    if openai.resources.chat.completions.Completions.create == _patched_openai_chatcompletion_create:
        openai.resources.chat.completions.Completions.create = _original_openai_chatcompletion_create
        print("OpenAI ChatCompletion unpatched.")
    else:
        print("OpenAI ChatCompletion was not patched or already unpatched.")

# To enable patching, a user would typically call patch_openai() explicitly
# from their application setup. Automatic patching on import can be risky
# for libraries. For now, let's not auto-patch.
# patch_openai() 