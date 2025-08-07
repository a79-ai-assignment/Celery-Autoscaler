# Celery Task Queue Autoscaling System on Kubernetes (Minikube)

## Overview

This project demonstrates an autoscaling system for Celery workers in a Kubernetes environment using **Minikube**. The workers dynamically scale based on resource usage and task queue demands.

---

## Components

- **Celery App**: Supports CPU-intensive and I/O-bound tasks
- **Message Broker**: Redis
- **Autoscaler**: Kubernetes Horizontal Pod Autoscaler (CPU-based)
- **Metrics**: Collected using Kubernetes metrics-server
- **Simulated Load**: Python script to generate tasks in different patterns

---

## Technologies Used

- Python + Celery
- Redis
- Docker
- Kubernetes (Minikube)
- Kubernetes HPA
- Optional: Prometheus + Grafana (for stretch goals)

---

## Minikube Setup

### Prerequisites

- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- Docker (local or DockerHub account)

---

### Step-by-Step Instructions

### 1. Start Minikube
minikube start --driver=docker

### 2. Build the Docker Image
eval $(minikube docker-env)
docker build -t celery-autoscaler:latest .

### 3. Push to DockerHub

docker build -t <your-dockerhub-username>/celery-autoscaler:latest .
docker push <your-dockerhub-username>/celery-autoscaler:latest

### 4. Apply Kubernetes Manifests

kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/celery-worker-deployment.yaml
kubectl apply -f k8s/hpa.yaml

### 5. Submit Tasks to the Queue

pip install -r requirements.txt
python scripts/task_generator.py gradual

### 6. Watch Autoscaling in Action

kubectl get hpa -w





