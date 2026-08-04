"""
Step A: Isolation Forest & DBSCAN Anomaly Detection Engine with Evaluation
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any, Tuple, List

from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, precision_recall_fscore_support


def load_and_preprocess_data(csv_path: str = "data/metrics_sample.csv") -> Tuple[pd.DataFrame, np.ndarray, List[int]]:
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    features = df[["cpu_pct", "error_rate", "latency_p99_ms"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # Ground truth: indices 200 to 215 are anomalies
    ground_truth = [1 if 200 <= i <= 215 else 0 for i in range(len(df))]
    return df, X_scaled, ground_truth


def plot_metrics_overview(df: pd.DataFrame, output_dir: str = "plots"):
    os.makedirs(output_dir, exist_ok=True)
    fig, axes = plt.subplots(3, 1, figsize=(12, 7), sharex=True)

    axes[0].plot(df["timestamp"], df["cpu_pct"], color="steelblue", linewidth=1.0)
    axes[0].set_title("CPU Utilization (%)")
    axes[0].set_ylabel("CPU %")
    axes[0].grid(True, linestyle=":", alpha=0.6)

    axes[1].plot(df["timestamp"], df["error_rate"], color="red", linewidth=1.0)
    axes[1].set_title("Error Rate")
    axes[1].set_ylabel("Error Rate")
    axes[1].grid(True, linestyle=":", alpha=0.6)

    axes[2].plot(df["timestamp"], df["latency_p99_ms"], color="orange", linewidth=1.0)
    axes[2].set_title("Latency p99 (ms)")
    axes[2].set_ylabel("p99 Latency (ms)")
    axes[2].grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    out_path = os.path.join(output_dir, "metrics_overview.png")
    plt.savefig(out_path, dpi=120)
    plt.close()
    print(f"📊 Saved metrics overview to '{out_path}'")


def run_isolation_forest(
    X_scaled: np.ndarray,
    df: pd.DataFrame,
    ground_truth: List[int],
    contamination: float = 0.04
) -> Tuple[np.ndarray, Dict[str, float]]:
    model = IsolationForest(n_estimators=200, contamination=contamination, random_state=42)
    model.fit(X_scaled)

    # predict: -1 for anomaly, 1 for normal
    preds_raw = model.predict(X_scaled)
    predictions = (preds_raw == -1).astype(int)

    precision, recall, f1, _ = precision_recall_fscore_support(ground_truth, predictions, average="binary", pos_label=1)

    metrics = {
        "contamination": contamination,
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "detected_count": int(predictions.sum())
    }
    return predictions, metrics


def run_dbscan(
    X_scaled: np.ndarray,
    ground_truth: List[int],
    eps: float = 1.2,
    min_samples: int = 5
) -> Tuple[np.ndarray, Dict[str, float]]:
    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(X_scaled)

    # DBSCAN identifies outliers as -1
    predictions = (labels == -1).astype(int)

    precision, recall, f1, _ = precision_recall_fscore_support(ground_truth, predictions, average="binary", pos_label=1)

    metrics = {
        "eps": eps,
        "min_samples": min_samples,
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "detected_count": int(predictions.sum())
    }
    return predictions, metrics


def plot_detection_results(
    df: pd.DataFrame,
    predictions: np.ndarray,
    ground_truth: List[int],
    title: str,
    output_filename: str,
    output_dir: str = "plots"
):
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(df["timestamp"], df["latency_p99_ms"], color="steelblue", label="Latency p99 (ms)", linewidth=1.0)

    # Highlight ground truth anomaly window
    anomaly_indices = [i for i, val in enumerate(ground_truth) if val == 1]
    if anomaly_indices:
        start_ts = df["timestamp"].iloc[anomaly_indices[0]]
        end_ts = df["timestamp"].iloc[anomaly_indices[-1]]
        ax.axvspan(start_ts, end_ts, color="yellow", alpha=0.3, label="Ground Truth Incident Window")

    # Mark detected anomalies
    detected_mask = predictions == 1
    ax.scatter(
        df["timestamp"][detected_mask],
        df["latency_p99_ms"][detected_mask],
        color="red",
        s=30,
        zorder=5,
        label="Detected Anomaly"
    )

    ax.set_title(title)
    ax.set_ylabel("Latency (ms)")
    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    out_path = os.path.join(output_dir, output_filename)
    plt.savefig(out_path, dpi=120)
    plt.close()
    print(f"📊 Saved detection plot to '{out_path}'")


def evaluate_contamination_tuning(X_scaled: np.ndarray, ground_truth: List[int]) -> List[Dict[str, float]]:
    results = []
    for c in [0.01, 0.04, 0.10]:
        model = IsolationForest(n_estimators=200, contamination=c, random_state=42)
        preds = (model.predict(X_scaled) == -1).astype(int)
        precision, recall, f1, _ = precision_recall_fscore_support(ground_truth, preds, average="binary", pos_label=1)
        results.append({
            "contamination": c,
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
            "detected_count": int(preds.sum())
        })
    return results


if __name__ == "__main__":
    df, X_scaled, ground_truth = load_and_preprocess_data("data/metrics_sample.csv")
    plot_metrics_overview(df)

    # Isolation Forest
    if_preds, if_metrics = run_isolation_forest(X_scaled, df, ground_truth, contamination=0.04)
    print("\n🌲 Isolation Forest Evaluation (contamination=0.04):")
    print(f"   Precision: {if_metrics['precision']:.3f} | Recall: {if_metrics['recall']:.3f} | F1: {if_metrics['f1']:.3f}")
    plot_detection_results(df, if_preds, ground_truth, "Isolation Forest Anomaly Detection", "anomaly_detection_isolation_forest.png")

    # DBSCAN
    db_preds, db_metrics = run_dbscan(X_scaled, ground_truth, eps=1.2, min_samples=5)
    print("\n🔵 DBSCAN Evaluation (eps=1.2, min_samples=5):")
    print(f"   Precision: {db_metrics['precision']:.3f} | Recall: {db_metrics['recall']:.3f} | F1: {db_metrics['f1']:.3f}")
    plot_detection_results(df, db_preds, ground_truth, "DBSCAN Anomaly Detection", "anomaly_detection_dbscan.png")
