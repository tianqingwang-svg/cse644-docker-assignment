"""
OpenTelemetry GenAI Conventions Instrumentation & Span Capture Helper
"""
import os
import json
import time
from typing import Dict, Any, List, Optional

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor
    from opentelemetry.sdk.resources import Resource
except ImportError:
    trace = None
    TracerProvider = None
    ConsoleSpanExporter = None

# Custom Span collector for JSON export
CAPTURED_SPANS = []


class JSONSpanCollector:
    """Collects exported spans into a JSON-serializable list."""
    def __init__(self):
        self.spans = []

    def add_span(self, name: str, attributes: Dict[str, Any], duration_ms: float):
        span_data = {
            "name": name,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "duration_ms": round(duration_ms, 2),
            "attributes": attributes
        }
        self.spans.append(span_data)
        CAPTURED_SPANS.append(span_data)

    def save_to_file(self, filepath: str = "output/spans_sample.json"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.spans, f, indent=2)
        print(f"📡 Saved captured OTel GenAI spans to '{filepath}'")


collector = JSONSpanCollector()


def get_tracer(service_name: str = "rca-agent-service"):
    if trace is None or TracerProvider is None:
        return None

    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(service_name)
    return tracer


def instrument_genai_span(
    name: str,
    system: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    duration_ms: float,
    prompt_sample: str = "",
    completion_sample: str = ""
):
    """Emit span following OpenTelemetry GenAI semantic conventions."""
    attributes = {
        "gen_ai.system": system,
        "gen_ai.request.model": model,
        "gen_ai.usage.input_tokens": input_tokens,
        "gen_ai.usage.output_tokens": output_tokens,
        "gen_ai.usage.total_tokens": input_tokens + output_tokens,
        "gen_ai.prompt": prompt_sample[:100],
        "gen_ai.completion": completion_sample[:100],
    }

    # Calculate estimated cost (Claude 3.5 Sonnet / Opus pricing reference: $3/M input, $15/M output)
    cost = (input_tokens / 1_000_000 * 3.0) + (output_tokens / 1_000_000 * 15.0)
    attributes["gen_ai.usage.cost_usd"] = round(cost, 6)

    collector.add_span(name, attributes, duration_ms)

    tracer = get_tracer()
    if tracer:
        with tracer.start_as_current_span(name) as span:
            for k, v in attributes.items():
                span.set_attribute(k, v)


def export_spans_json(filepath: str = "output/spans_sample.json"):
    collector.save_to_file(filepath)
