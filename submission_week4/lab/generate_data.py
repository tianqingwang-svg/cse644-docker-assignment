"""
Step 1: Dataset Generation Script
Generates a realistic 7-day time series dataset of CPU and memory metrics at 5-minute intervals.
"""
import os
import pandas as pd
import numpy as np


def generate_synthetic_metrics(output_path: str = "synthetic_metrics.csv", n_days: int = 7) -> pd.DataFrame:
    np.random.seed(42)
    points_per_day = 24 * 12  # 5-minute intervals = 288 points per day
    n_points = n_days * points_per_day

    timestamps = pd.date_range(start="2025-10-01 00:00:00", periods=n_points, freq="5T")
    t = np.arange(n_points)

    # Daily cycle (24-hour period) and Weekly cycle (7-day period)
    daily_cycle = 20 * np.sin(2 * np.pi * t / points_per_day - np.pi / 2)
    weekly_cycle = 10 * np.sin(2 * np.pi * t / (7 * points_per_day))
    noise = np.random.normal(0, 3, n_points)
    trend = 0.005 * t  # slight upward trend

    # Add occasional sudden peak traffic spike at day 4
    spike = np.zeros(n_points)
    spike[1150:1160] = 35.0  # abrupt load spike

    cpu = np.clip(30 + daily_cycle + weekly_cycle + noise + trend + spike, 5, 95)
    memory = np.clip(45 + 0.5 * daily_cycle + noise * 0.5 + 0.3 * spike, 20, 90)

    df_sim = pd.DataFrame({
        "ds": timestamps,
        "cpu": cpu,
        "memory": memory
    })

    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    df_sim.to_csv(output_path, index=False)
    print(f"✅ Generated synthetic metrics dataset with {len(df_sim)} records at '{output_path}'.")
    return df_sim


if __name__ == "__main__":
    generate_synthetic_metrics()
