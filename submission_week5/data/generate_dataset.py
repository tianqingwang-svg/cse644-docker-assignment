"""
Data Generation Script for Week 5
Generates metrics_sample.csv (with ground truth anomalies at 200-215)
and logs_sample.txt (200+ structured application log entries with an incident pattern).
"""
import os
import numpy as np
import pandas as pd


def generate_metrics(output_path: str = "metrics_sample.csv", n: int = 500) -> pd.DataFrame:
    rng = np.random.default_rng(42)

    # Normal operation
    timestamps = pd.date_range("2025-10-01 08:00", periods=n, freq="1min")
    cpu = rng.normal(35, 5, n)
    error_rate = rng.exponential(0.002, n)
    latency_p99 = rng.normal(150, 20, n)

    # Inject anomalies at indices 200-215 (simulated database connection leak / deadlock incident)
    cpu[200:216] = rng.normal(85, 5, 16)
    error_rate[200:216] = rng.uniform(0.05, 0.15, 16)
    latency_p99[200:216] = rng.normal(3500, 200, 16)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "cpu_pct": np.clip(cpu, 0, 100),
        "error_rate": np.clip(error_rate, 0, 1),
        "latency_p99_ms": np.clip(latency_p99, 0, None)
    })

    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    df.to_csv(output_path, index=False)
    print(f"✅ Generated '{output_path}' ({len(df)} metrics points).")
    return df


def generate_logs(output_path: str = "logs_sample.txt", n: int = 250) -> str:
    timestamps = pd.date_range("2025-10-01 08:00", periods=n, freq="1min")
    log_lines = []

    services = ["user-service", "auth-service", "payment-service", "db-cluster-01"]
    levels = ["INFO", "DEBUG"]

    for i in range(n):
        ts = timestamps[i].strftime("%Y-%m-%dT%H:%M:%SZ")

        if 200 <= i <= 215:
            # Incident log pattern
            if i == 200:
                line = f"{ts} [CRITICAL] db-cluster-01: Connection pool exhausted (max_connections=100 reached)."
            elif i in [201, 202, 203]:
                line = f"{ts} [ERROR] payment-service: Timeout waiting for database connection after 30000ms. Transaction aborted."
            elif i in [204, 205, 206, 207]:
                line = f"{ts} [ERROR] user-service: HTTP 500 Internal Server Error - Failed to acquire auth token from database."
            elif i in [208, 209, 210]:
                line = f"{ts} [WARN] auth-service: Thread pool saturation (active_threads=200/200). Request queue depth: 450."
            elif i in [211, 212, 213]:
                line = f"{ts} [ERROR] payment-service: OutOfMemoryError in ConnectionManager worker thread."
            else:
                line = f"{ts} [CRITICAL] db-cluster-01: Primary node high CPU (92%). Failover triggered."
        else:
            # Normal log pattern
            srv = services[i % len(services)]
            lvl = levels[i % len(levels)]
            if srv == "payment-service":
                msg = f"Processed payment transaction id=tx_{1000+i} status=SUCCESS latency={np.random.randint(120, 180)}ms"
            elif srv == "auth-service":
                msg = f"Validated JWT token for user_id=usr_{500+i}"
            elif srv == "user-service":
                msg = f"GET /api/v1/profile 200 OK latency={np.random.randint(90, 140)}ms"
            else:
                msg = f"DB health check OK. Active connections: {np.random.randint(15, 30)}/100"
            line = f"{ts} [{lvl}] {srv}: {msg}"

        log_lines.append(line)

    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    content = "\n".join(log_lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Generated '{output_path}' ({len(log_lines)} log entries).")
    return content


if __name__ == "__main__":
    generate_metrics()
    generate_logs()
