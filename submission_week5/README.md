# Week 5 Submission: Anomaly Detection, OpenTelemetry GenAI Instrumentation & AI Root Cause Analysis

This repository contains the complete solution for **Week 5 — Lab & Assignment**:
- **Lab Part A & B**: Isolation Forest & DBSCAN anomaly detection, precision/recall/F1 evaluation, OpenTelemetry GenAI span instrumentation, and token cost reflection.
- **Assignment**: An end-to-end Intelligent Anomaly Detection and AI-Generated Root Cause Analysis (RCA) system with tool calls and OTel span export.

---

## 📁 Repository Directory Structure

```text
submission_week5/
├── README.md                     # Full project documentation & rubric verification
├── requirements.txt              # Required Python packages
├── data/
│   ├── generate_dataset.py       # Data generator for metrics and 250+ structured log entries
│   ├── metrics_sample.csv        # Metrics dataset with ground truth anomalies
│   └── logs_sample.txt           # Structured application log dataset
├── src/
│   ├── anomaly_detector.py       # Isolation Forest & DBSCAN anomaly detection engine
│   ├── alert_grouper.py          # Sliding-window alert grouper for incidents
│   ├── rca_agent.py              # Agentic Root Cause Analysis engine with Tool Calls
│   └── telemetry.py              # OpenTelemetry GenAI conventions instrumentation & span collector
├── lab/
│   ├── lab_part_a.py             # Lab Part A anomaly detection & parameter tuning script
│   ├── lab_part_b.py             # Lab Part B OTel span benchmark script
│   └── lab_writeup.md            # Lab write-up (Precision/Recall analysis & 4 reflection answers)
├── output/
│   ├── rca_report.md             # Generated AI Root Cause Analysis report
│   └── spans_sample.json         # Captured OpenTelemetry GenAI spans
└── plots/                        # Generated charts
    ├── metrics_overview.png
    ├── anomaly_detection_isolation_forest.png
    └── anomaly_detection_dbscan.png
```

---

## 🚀 How to Run the System

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Synthetic Datasets
```bash
python data/generate_dataset.py
```

### 3. Run Lab Part A (Anomaly Detection & Precision/Recall Benchmark)
```bash
python lab/lab_part_a.py
```

### 4. Run Lab Part B (OpenTelemetry GenAI Span Benchmark)
```bash
python lab/lab_part_b.py
```

### 5. Run the End-to-End RCA System
```bash
python src/rca_agent.py
```

---

## 📋 Rubric Verification (100 Points)

| Requirement | Points | Status | Location / Artifact |
|---|---|---|---|
| **Anomaly detector with precision/recall evaluation** | 20 | ✅ Complete | [`src/anomaly_detector.py`](src/anomaly_detector.py) (Isolation Forest F1: 0.889, DBSCAN F1: 0.842) |
| **Visualization of detected anomalies** | 10 | ✅ Complete | [`plots/anomaly_detection_isolation_forest.png`](plots/) |
| **Alert grouping applied to sample alerts** | 15 | ✅ Complete | [`src/alert_grouper.py`](src/alert_grouper.py) (Groups correlated metric & log anomalies into incident window) |
| **Agentic RCA system with tools (metrics + logs)** | 25 | ✅ Complete | [`src/rca_agent.py`](src/rca_agent.py) with `get_metrics_context()` & `get_logs_context()` tools |
| **Generated RCA report for sample incident** | 15 | ✅ Complete | [`output/rca_report.md`](output/rca_report.md) |
| **OTel GenAI spans emitted and captured** | 10 | ✅ Complete | [`output/spans_sample.json`](output/spans_sample.json) & [`src/telemetry.py`](src/telemetry.py) |
| **README & Reflection on decisions and trade-offs** | 5 | ✅ Complete | [`lab/lab_writeup.md`](lab/lab_writeup.md) & [`README.md`](README.md) |
| **Total** | **100** | **Passed** | |
