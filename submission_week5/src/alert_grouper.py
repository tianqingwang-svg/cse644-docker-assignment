"""
Alert Grouper Module: Clusters correlated metric and log anomaly events into incident windows.
"""
import pandas as pd
from typing import List, Dict, Any


def group_alerts(
    metrics_df: pd.DataFrame,
    anomaly_mask: pd.Series,
    log_file_path: str = "data/logs_sample.txt",
    window_minutes: int = 15
) -> List[Dict[str, Any]]:
    """
    Groups detected metric anomalies and error logs into coherent incident clusters.
    """
    anomalous_metrics = metrics_df[anomaly_mask].copy()
    if anomalous_metrics.empty:
        return []

    # Identify continuous time ranges of metric anomalies
    anomalous_metrics["time_diff"] = anomalous_metrics["timestamp"].diff()
    new_cluster_mask = anomalous_metrics["time_diff"] > pd.Timedelta(minutes=window_minutes)
    anomalous_metrics["cluster_id"] = new_cluster_mask.cumsum()

    clusters = []

    # Read logs
    logs = []
    if os.path.exists(log_file_path):
        with open(log_file_path, "r", encoding="utf-8") as f:
            logs = f.readlines()

    for cid, group in anomalous_metrics.groupby("cluster_id"):
        start_time = group["timestamp"].min()
        end_time = group["timestamp"].max()

        # Find matching logs in this time window
        relevant_logs = []
        start_str = start_time.strftime("%Y-%m-%dT%H:%M")
        end_str = end_time.strftime("%Y-%m-%dT%H:%M")

        for line in logs:
            if any(level in line for level in ["ERROR", "CRITICAL", "WARN"]):
                # Simple timestamp check
                if line[:16] >= start_str and line[:16] <= end_str:
                    relevant_logs.append(line.strip())

        cluster_info = {
            "incident_id": f"INC-{start_time.strftime('%Y%m%d%H%M')}",
            "start_time": str(start_time),
            "end_time": str(end_time),
            "duration_minutes": int((end_time - start_time).total_seconds() / 60) + 1,
            "metric_anomalies_count": len(group),
            "peak_cpu": float(group["cpu_pct"].max()),
            "peak_latency_ms": float(group["latency_p99_ms"].max()),
            "peak_error_rate": float(group["error_rate"].max()),
            "relevant_log_count": len(relevant_logs),
            "sample_logs": relevant_logs[:10]  # sample top 10 relevant error logs
        }
        clusters.append(cluster_info)

    return clusters


if __name__ == "__main__":
    import os
    df = pd.read_csv("data/metrics_sample.csv", parse_dates=["timestamp"])
    mask = (df.index >= 200) & (df.index <= 215)
    incidents = group_alerts(df, mask, "data/logs_sample.txt")
    print(f"Grouped {len(incidents)} incident(s):")
    for inc in incidents:
        print(f"  - {inc['incident_id']} (Duration: {inc['duration_minutes']}m, Peak CPU: {inc['peak_cpu']:.1f}%, Logs: {inc['relevant_log_count']})")
