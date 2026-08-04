"""
Lab Part B: Instrumenting an Agent with OpenTelemetry GenAI Conventions
Evaluates token consumption, latency, and cost across 5 log windows of varying sizes.
"""
import os
import sys
import time
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(base_dir)
sys.path.insert(0, os.path.join(project_root, "src"))

from telemetry import instrument_genai_span, export_spans_json


def main():
    logs_file = os.path.join(project_root, "data", "logs_sample.txt")
    if not os.path.exists(logs_file):
        print("Logs file not found.")
        return

    with open(logs_file, "r", encoding="utf-8") as f:
        full_logs = f.read()

    window_sizes = [500, 1500, 3000, 6000, 12000]
    results = []

    print("================ 🧪 LAB PART B: AGENT INSTRUMENTATION ==================")
    print(f"{'Log Window (chars)':<20}{'Input Tokens':<15}{'Output Tokens':<15}{'Latency (ms)':<15}{'Cost ($)':<15}")
    print("-" * 80)

    for w_size in window_sizes:
        log_chunk = full_logs[:w_size]
        start_time = time.time()

        # Simulate or call LLM log analysis
        input_tokens = len(log_chunk) // 4 + 50
        output_tokens = 150 + (w_size // 100)
        duration_ms = 120.0 + (w_size * 0.04)

        # Estimate cost ($3/M input, $15/M output)
        cost = (input_tokens / 1_000_000 * 3.0) + (output_tokens / 1_000_000 * 15.0)

        instrument_genai_span(
            name="gen_ai.log_analyzer.process_window",
            system="anthropic",
            model="claude-haiku-4-5",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            duration_ms=duration_ms,
            prompt_sample=f"Analyze log chunk ({w_size} chars)",
            completion_sample="Anomalies detected in log window."
        )

        results.append({
            "chars": w_size,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_ms": round(duration_ms, 1),
            "cost_usd": cost
        })

        print(f"{w_size:<20}{input_tokens:<15}{output_tokens:<15}{duration_ms:<15.1f}${cost:<14.6f}")

    export_spans_json(os.path.join(project_root, "output", "spans_sample.json"))
    print("\n========================================================================\n")


if __name__ == "__main__":
    main()
