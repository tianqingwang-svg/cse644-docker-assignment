# Week 5 Lab Write-up: Anomaly Detection & OpenTelemetry Agent Instrumentation

## 🧪 Part A: Anomaly Detection & Evaluation Summary

### 1. Isolation Forest Evaluation & Contamination Tuning

Ground Truth: Injected incident between index `200` and `215` (16 total anomaly points).

| Contamination Parameter | Detected Anomalies | Precision | Recall | F1-Score | Analysis |
|---|---|---|---|---|---|
| `contamination = 0.01` | 5 | **1.000** | 0.312 | 0.476 | High precision, but misses 68.8% of true incident points (Under-flagging). |
| `contamination = 0.04` | 20 | **0.800** | **1.000** | **0.889** | **Optimal Balance**: Catches 100% of incident points with minimal false positives. |
| `contamination = 0.10` | 50 | 0.320 | **1.000** | 0.485 | High recall, but 68% false positive rate leading to severe alert fatigue. |

> **Key takeaway on the "Accuracy Trap"**: Overall accuracy for `contamination = 0.01` is **97.8%**, but its anomaly recall is only **31.2%**. Evaluating on anomaly-class Precision/Recall is critical.

### 2. Isolation Forest vs. DBSCAN Comparison

- **Isolation Forest (F1 = 0.889)**: Performs exceptionally well on multi-dimensional global feature spaces (`cpu_pct`, `error_rate`, `latency_p99_ms`). It isolates anomalies efficiently because anomalous points require fewer decision tree splits to isolate.
- **DBSCAN (`eps=1.2, min_samples=5`, F1 = 0.842)**: Successfully identifies dense normal clusters and marks outliers as `-1`. However, because latency spikes during the incident varied continuously (from 3,000ms to 3,800ms), DBSCAN formed small sub-clusters for extreme points, requiring parameter tuning on `eps` to avoid splitting the incident into multiple noise classes.

---

## 📡 Part B: OTel GenAI Instrumentation & Reflection Answers

### Span Telemetry Benchmark Summary

| Log Window Size (chars) | Input Tokens | Output Tokens | Latency (ms) | Estimated Cost ($ USD) |
|---|---|---|---|---|
| **500** | 175 | 155 | 140.0 ms | **$0.002850** |
| **1,500** | 425 | 165 | 180.0 ms | **$0.003750** |
| **3,000** | 800 | 180 | 240.0 ms | **$0.005100** |
| **6,000** | 1,550 | 210 | 360.0 ms | **$0.007800** |
| **12,000** | 3,050 | 270 | 600.0 ms | **$0.013200** |

---

### Question 1: How did input token count correlate with log window size? Was the relationship linear?

**Answer:**
The input token count exhibited a **strong near-linear relationship** ($r \approx 0.99$) with character count, approximating the standard empirical ratio of **1 token $\approx$ 4 characters** for English log text.

The exact function fits $y = 0.25x + c$, where:
- $x$ is the log window character size.
- $0.25$ represents the average token density for structured log formatting.
- $c \approx 50$ tokens is a constant intercept representing system prompt headers and schema instructions.

---

### Question 2: At what rate would your agent's LLM cost accumulate if it processed 10 log windows per minute, 24/7 for a month?

**Answer:**

#### Quantitative Calculation:
1. **Total Invocations**:
   $$\text{Calls/month} = 10 \text{ calls/min} \times 60 \text{ min/hr} \times 24 \text{ hrs/day} \times 30 \text{ days} = \mathbf{432,000 \text{ calls/month}}$$
2. **Token Volume** (Assuming average log window of 3,000 chars $\approx$ 800 input tokens, 180 output tokens):
   - **Total Input Tokens**: $432,000 \times 800 = \mathbf{345,600,000 \text{ tokens (345.6M)}}$
   - **Total Output Tokens**: $432,000 \times 180 = \mathbf{77,760,000 \text{ tokens (77.76M)}}$
3. **Monthly Financial Spend** (Anthropic Claude 3.5 Sonnet reference: $3.00/M input, $15.00/M output):
   - **Input Cost**: $345.6 \times \$3.00 = \mathbf{\$1,036.80}$
   - **Output Cost**: $77.76 \times \$15.00 = \mathbf{\$1,166.40}$
   - **Total Monthly Cost**: **$\mathbf{\$2,203.20 \text{ USD / month}}$**

---

### Question 3: What guardrail would you add to prevent runaway costs?

**Answer:**
To prevent cost explosion in production:

1. **Pre-Filtering Pipeline (Anomaly Trigger Gate)**: Never send raw, unfiltered logs to LLMs on a fixed schedule. Use lightweight ML models (Isolation Forest) or deterministic log filters (grep for `ERROR`/`CRITICAL`) to trigger the LLM agent **only when an anomaly is verified**.
2. **Semantic Caching**: Implement Redis or LangChain semantic caching to cache RCA reports for repeated log stack traces, reducing redundant LLM calls by up to 60%.
3. **Hard Token Limits & Dynamic Truncation**: Enforce strict `max_tokens` limits (e.g. max 500 output tokens) and truncate log windows to include only the 50 lines surrounding an anomaly rather than whole files.
4. **Monthly Budget Circuit Breaker**: Set an OTel telemetry alert at $500/month that automatically downgrades the agent to an offline rule engine if budget thresholds are exceeded.

---

### Question 4: In the Foundations primer we said "treat your agents as first-class services." What would a production-grade dashboard for this agent look like? List five metrics you would track.

**Answer:**

A production-grade Agent Observability Dashboard (Grafana / Datadog) should track:

1. **`gen_ai.usage.token_rate` & Cumulative Cost ($/hr)**: Real-time tracking of input/output token consumption split by model version (`claude-haiku-4-5` vs `claude-opus-4-8`).
2. **`agent.execution_latency.p95_ms`**: P95 end-to-end execution latency, decomposed into LLM API Time-To-First-Token (TTFT) and tool execution overhead.
3. **`agent.tool_call.error_rate`**: Percentage of tool invocation failures (e.g., database lookup timeouts or malformed JSON arguments).
4. **`agent.rca.accuracy_eval_score`**: Human SRE feedback score (thumbs up/down or acceptance rate on generated RCA post-mortems).
5. **`agent.circuit_breaker.trigger_count`**: Count of requests throttled or fallback-routed due to rate limits or token budget guardrails.
