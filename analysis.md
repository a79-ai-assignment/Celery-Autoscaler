
# Autoscaling Analysis Report

## Overview

This report analyzes the autoscaling behavior of Celery workers deployed in a Kubernetes cluster (Minikube) under various task load patterns. The Horizontal Pod Autoscaler (HPA) is configured based on CPU utilization.

---

## Test Configuration

- **Cluster**: Minikube
- **Autoscaler**: Kubernetes HPA
- **Scaling target**: Celery Worker Deployment
- **Min replicas**: 1
- **Max replicas**: 5
- **CPU target utilization**: 50%
- **Task types**:
  - `cpu_task`: CPU-intensive (tight loop calculations)
  - `io_task`: Simulated I/O-bound (via `time.sleep`)
- **Broker**: Redis
- **Metrics source**: metrics-server

---

## Scenario 1: Gradual Load Increase

### Description
Tasks were submitted at a constant increasing rate over time using:
```bash
python scripts/task_generator.py gradual
```

### Observations
- CPU usage gradually increased across the initial single worker pod.
- HPA scaled the number of pods from 1 → 2 → 3 as CPU utilization crossed the 50% threshold.
- Scaling occurred smoothly, with ~30–60s delay per scaling event.
- No task failures or timeouts were observed.
- Once the task generation stopped, HPA scaled down after ~5 minutes.

### Result
**Expected scaling behavior achieved. Smooth and predictable.**

---

## Scenario 2: Sudden Task Burst

### Description
A large number of tasks were submitted in a short time:
```bash
python scripts/task_generator.py burst
```

### Observations
- Initial CPU utilization spiked quickly.
- HPA responded by increasing replicas from 1 → 5 (max limit).
- Some task processing latency was observed before pods were fully ready.
- Redis queue temporarily grew large but quickly drained once all 5 workers were running.
- After task completion, HPA scaled down after ~5–6 minutes.

### Result
**HPA effectively scaled to max capacity during load burst, with slight initial lag due to pod startup latency.**

---

## Scenario 3: Oscillating Load

### Description
Alternating periods of task bursts and idleness:
```bash
python scripts/task_generator.py oscillating
```

### Observations
- HPA oscillated between 1–4 pods based on CPU spikes.
- System avoided thrashing (frequent rapid up/down scaling) due to cooldown periods.
- CPU usage graph showed clean rise and fall cycles.
- Some idle CPU time was observed between load intervals (expected).
- No pod failures or excessive scaling events.

### Result
**System demonstrated resilience to oscillating traffic. Autoscaler respected cooldown, avoiding aggressive downscaling.**

---

## Summary Table

| Pattern       | Pods (min→max) | Avg CPU | Latency | Thrashing | Observations |
|---------------|----------------|---------|---------|-----------|--------------|
| Gradual       | 1 → 3          | Moderate| Low     | ❌        | Smooth scaling |
| Burst         | 1 → 5          | High    | Moderate| ❌        | Quick recovery |
| Oscillating   | 1 ↔ 4          | Varies  | Low     | ❌        | Balanced scaling |

---

## Key Insights

- **CPU-based autoscaling** works reasonably well for `cpu_task`, but less reactive for `io_task`.
- **Queue-depth-based scaling (e.g., via KEDA)** would provide better precision for Celery systems.
- **Startup latency** of pods can cause short-lived bottlenecks in burst scenarios.
- **Cooldown periods** help prevent pod churn during fluctuating loads.

---

## Recommendations

- Integrate **KEDA** to scale on **Redis queue length** for more accurate scaling.
- Use **priority queues** for critical tasks.
- Add **metrics exporters** (e.g., Prometheus + Grafana) to visualize queue depth and worker state in real time.

---
