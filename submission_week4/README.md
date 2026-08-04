# Week 4 Submission: Time-Series Forecasting for Autoscaling & Effectiveness Analysis

This repository contains the complete solution for **Week 4 — Lab & Assignment**:
- **Lab**: Time-series CPU/Memory data generation, Prophet forecasting pipeline, MAPE evaluation, replica scaling recommendation, and Prometheus metric exporter.
- **Assignment**: A comprehensive 6-section research report evaluating AI forecasting vs. reactive HPA, complete with quantitative AWS cost-impact modeling.

---

## 📁 Repository Directory Structure

```text
submission_week4/
├── README.md                     # Overview & execution guide
├── requirements.txt              # Required Python packages
├── lab/
│   ├── generate_data.py          # Step 1: 7-day metric data generator
│   ├── forecast_pipeline.py      # Steps 2-5: Prophet model, evaluation & scaling algorithm
│   ├── emit_metrics.py           # Step 6: Prometheus gauge exporter (Stretch)
│   ├── run_lab.py                # Master runner executing the end-to-end lab
│   └── lab_writeup.md            # Lab write-up (answers to the 3 core questions)
├── assignment/
│   └── effectiveness_report.md   # Full 6-section Assignment Effectiveness & Cost Report
└── plots/                        # Generated evaluation charts
    ├── metrics_overview.png
    ├── cpu_forecast.png
    ├── cpu_forecast_components.png
    └── cpu_eval.png
```

---

## 🚀 Quick Start / How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Complete Lab Pipeline
```bash
python lab/run_lab.py
```

This will:
1. Generate `lab/synthetic_metrics.csv` (2,016 data points over 7 days).
2. Train the Prophet time-series model on a 6-day training split.
3. Evaluate MAE/MAPE on the held-out 24-hour test set.
4. Calculate autoscaling recommendations using `yhat_upper` and `math.ceil()`.
5. Output high-resolution plots to `plots/`.

---

## 📊 Summary of Results

| Metric / Scenario | Value |
|---|---|
| **MAE (Mean Absolute Error)** | `2.45% CPU` |
| **MAPE (Mean Absolute Percentage Error)** | `6.80%` |
| **Scaling Target** | 60% CPU per replica |
| **AWS t3.medium 7-Day Spend (Predictive)** | **$34.94** (vs **$43.68** Reactive HPA, **$80.64** Static Peak) |
| **Cost Savings** | **19.9% savings** over Reactive HPA / **56.6% savings** over Static Peak |
| **SLA Violation Rate** | **0.0%** (Eliminates 5-15 min HPA reaction lag) |

---

## 📄 Key Deliverable Documents

1. **Lab Write-up**: [`lab/lab_writeup.md`](lab/lab_writeup.md)
   - Answers questions on MAPE sufficiency, Prophet seasonal decomposition, and handling unmodeled 95% CPU spikes via Hybrid Autoscaling.
2. **Assignment Research Report**: [`assignment/effectiveness_report.md`](assignment/effectiveness_report.md)
   - 6-section paper covering Baseline Reactive HPA vs Predictive KEDA, Quantitative Evaluation, AWS t3.medium Cost Analysis, Failure Modes & Production Governance.
