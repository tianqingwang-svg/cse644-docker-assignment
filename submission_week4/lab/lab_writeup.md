# Week 4 Lab Write-up: Time-Series Forecasting for Autoscaling

## 📊 Summary of Quantitative Results

- **Dataset**: 7-day synthetic workload trace (2,016 data points at 5-minute intervals).
- **Held-Out Test Set**: Last 24 hours (288 data points).
- **Mean Absolute Error (MAE)**: `2.45% CPU`
- **Mean Absolute Percentage Error (MAPE)**: `6.8%`
- **Autoscaling Target**: 60% CPU utilization per replica.
- **Recommended Replica Action**: Scaling recommendation calculated using `yhat_upper` (80% confidence interval) and `math.ceil` rounding to prevent under-provisioning.

---

## ❓ Lab Reflection Questions & Answers

### Question 1: What MAPE did you achieve? Is it good enough for autoscaling decisions?

**Answer:**
We achieved a **MAPE of 6.8%** and an **MAE of 2.45% CPU utilization** on the held-out 24-hour evaluation set. 

**Is it good enough for autoscaling?**
Yes, a MAPE under 10% is highly suitable for predictive autoscaling decisions, provided that safety buffers are incorporated. In production systems:
- A 6.8% error margin represents a difference of less than ±3% CPU utilization on average.
- Because our autoscaling algorithm uses `yhat_upper` (the upper 80% confidence interval bound) rather than the point estimate (`yhat`), the system explicitly accounts for the forecast uncertainty.
- Combined with `math.ceil()` rounding, the algorithm naturally over-provisions slightly rather than under-provisioning, ensuring that cluster capacity stays ahead of actual demand while avoiding excessive resource waste.

---

### Question 2: What patterns did the Prophet components plot reveal?

**Answer:**
Prophet's component decomposition (`cpu_forecast_components.png`) separated the time series into three distinct signals:

1. **Overall Trend**:
   - Revealed a gradual linear upward trend (`+0.005%` CPU per interval), reflecting long-term organic user growth over the 7-day period.
2. **Daily Seasonality (24-Hour Cycle)**:
   - Showed a strong, predictable diurnal curve: CPU usage drops to its daily trough of ~15–20% between 2:00 AM and 5:00 AM, begins climbing rapidly around 7:00 AM, reaches a peak of ~50–60% during core business hours (11:00 AM – 4:00 PM), and gradually tapers off in the evening.
3. **Weekly Seasonality (7-Day Cycle)**:
   - Highlighted a clear weekday vs. weekend variation: weekday load remains higher due to active business transactions, while weekend load experiences a ~10% drop in baseline demand.

Understanding these components allows SREs to confirm that workload patterns are cyclical and that Prophet is successfully capturing business-hour dynamics rather than fitting to random noise.

---

### Question 3: If actual CPU hit 95% during a spike that the model did not forecast, what would happen with your scaling recommendation? How would you make the system more robust?

**Answer:**

#### What would happen:
If an unmodeled, anomalous traffic spike causes CPU utilization to surge to 95%:
- **Pure Predictive Failure**: A pure predictive model reliance would fail to scale up in time because the forecast model generates predictions based on historical patterns and cannot anticipate sudden unannounced events (e.g., flash sales, breaking news events, or DDoS attacks).
- **Resource Starvation**: Pods would become severely overloaded, leading to CPU throttling, elevated latency, request timeouts, or HTTP 5xx errors.

#### How to make the system more robust (Production Best Practices):

1. **Hybrid Predictive-Reactive Autoscaling**:
   - Configure a dual-engine scaling architecture. Use KEDA / Prophet predictive scaling for proactive baseline provisioning (scaling up 15–30 minutes before expected diurnal spikes).
   - Maintain standard Kubernetes Reactive HPA as a safety net. If real-time CPU breaches 80% utilization regardless of the forecast, reactive HPA immediately overrides the prediction and scales out replicas.

2. **Upper Confidence Bound Safety Margin (`yhat_upper`)**:
   - Base scaling decisions on `yhat_upper` (90th or 95th percentile confidence bound) rather than median `yhat`.

3. **Rate-of-Change & Anomaly Alerts**:
   - Implement rapid scale-up triggers based on queue length or request arrival rate changes (e.g., ingress requests per second rate-of-change) rather than waiting for CPU metric propagation lag.

4. **Minimum Pod Floor Buffer**:
   - Set a conservative `minReplicas` threshold during active business hours to guarantee headroom for unexpected load spikes.
