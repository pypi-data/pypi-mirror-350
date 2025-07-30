# Python SDK (`aep-otel`)

Stub package. Goals for Alpha:

1. Wrap OpenAI `ChatCompletion` call and emit AEP spans.
2. Export via OTLP to collector (fallback: JSONL file).
3. Expose `AEPSpan` helper to embed retrieval / attention metadata.

## TODO

- [x] pyproject.toml via Poetry.
- [x] Basic unit test with `pytest`.
- [x] Example script in `examples/` directory.