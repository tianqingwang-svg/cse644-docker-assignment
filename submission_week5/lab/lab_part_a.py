"""
Lab Part A: Anomaly Detection Experiments (Isolation Forest & DBSCAN Comparison)
"""
import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(base_dir)
sys.path.insert(0, os.path.join(project_root, "src"))

from anomaly_detector import (
    load_and_preprocess_data,
    run_isolation_forest,
    run_dbscan,
    evaluate_contamination_tuning,
    plot_detection_results
)
from sklearn.metrics import classification_report


def main():
    data_path = os.path.join(project_root, "data", "metrics_sample.csv")
    df, X_scaled, ground_truth = load_and_preprocess_data(data_path)

    print("================ 🧪 LAB PART A: ANOMALY DETECTION ==================")

    # 1. Contamination Parameter Tuning for Isolation Forest
    print("\n--- 1. Isolation Forest Contamination Tuning ---")
    tuning_results = evaluate_contamination_tuning(X_scaled, ground_truth)
    print(f"{'Contamination':<15}{'Detected':<12}{'Precision':<12}{'Recall':<12}{'F1-Score':<12}")
    print("-" * 63)
    for r in tuning_results:
        print(f"{r['contamination']:<15.2f}{r['detected_count']:<12}{r['precision']:<12.3f}{r['recall']:<12.3f}{r['f1']:<12.3f}")

    # 2. Detailed Classification Report for Best Isolation Forest (contamination=0.04)
    best_if_preds, best_if_metrics = run_isolation_forest(X_scaled, df, ground_truth, contamination=0.04)
    print("\n--- Isolation Forest (contamination=0.04) Classification Report ---")
    print(classification_report(ground_truth, best_if_preds, target_names=["Normal", "Anomaly"]))

    # 3. DBSCAN Parameter Tuning & Comparison
    print("\n--- 2. DBSCAN Epsilon Tuning ---")
    print(f"{'Eps':<10}{'MinSamples':<12}{'Detected':<12}{'Precision':<12}{'Recall':<12}{'F1-Score':<12}")
    print("-" * 70)
    for eps in [0.8, 1.2, 2.0]:
        db_preds, db_metrics = run_dbscan(X_scaled, ground_truth, eps=eps, min_samples=5)
        print(f"{eps:<10.1f}{5:<12}{db_metrics['detected_count']:<12}{db_metrics['precision']:<12.3f}{db_metrics['recall']:<12.3f}{db_metrics['f1']:<12.3f}")

    best_db_preds, best_db_metrics = run_dbscan(X_scaled, ground_truth, eps=1.2, min_samples=5)
    print("\n--- DBSCAN (eps=1.2, min_samples=5) Classification Report ---")
    print(classification_report(ground_truth, best_db_preds, target_names=["Normal", "Anomaly"]))

    print("\n===================================================================\n")


if __name__ == "__main__":
    main()
