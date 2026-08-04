"""
Step 6 (Stretch Goal): Emit Forecast as a Prometheus Metric Exporter
Exposes an HTTP endpoint on :8000/metrics for Prometheus scraper & KEDA ScaledObject.
"""
import time
import pandas as pd
from typing import Optional

try:
    from prometheus_client import Gauge, start_http_server
except ImportError:
    Gauge = None
    start_http_server = None

from forecast_pipeline import recommend_replicas


def start_metric_exporter(port: int = 8000, csv_path: str = "synthetic_metrics.csv", single_run: bool = False):
    if start_http_server is None or Gauge is None:
        print("⚠️ prometheus_client library not installed. Install with `pip install prometheus_client`.")
        return

    predicted_cpu_gauge = Gauge(
        "predicted_cpu_next_30m",
        "Prophet-predicted max CPU % for next 30 minutes",
        ["service"]
    )

    start_http_server(port)
    print(f"📡 Prometheus metrics exporter listening on http://localhost:{port}/metrics ...")

    while True:
        try:
            df = pd.read_csv(csv_path, parse_dates=["ds"])
            forecast_df = df[["ds", "cpu"]].rename(columns={"cpu": "yhat"})
            forecast_df["yhat_upper"] = forecast_df["yhat"] + 3.0

            _, max_pred, _ = recommend_replicas(forecast_df, current_replicas=4)
            predicted_cpu_gauge.labels(service="my-app").set(max_pred)
            print(f"✅ Emitted metric: predicted_cpu_next_30m{{service='my-app'}} = {max_pred:.1f}%")

            if single_run:
                break
            time.sleep(300)
        except KeyboardInterrupt:
            print("Stopping metrics exporter.")
            break
        except Exception as e:
            print(f"Error emitting metrics: {e}")
            time.sleep(10)


if __name__ == "__main__":
    start_metric_exporter(single_run=True)
