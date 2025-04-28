# Sentra Core

📜 Licensed under **BUSL-1.1** — commercial use requires a license. Apache 2.0 from 2028.

🚀 **Sentra** is an open-core SIEM platform designed for real-time threat detection, rule-based alerting, and ML-driven anomaly analysis — powered by Apache Flink, Kafka, and Python.

This repository contains the **open-source core** of the platform, including stream processing, detection logic, and baseline infrastructure.

---

## 🧱 Architecture

Sentra Core is built around modular, cloud-native components:

- **Ingestion** — Kafka producers / log emitters
- **Stream Processing** — Flink jobs for windowed aggregation, filtering, and scoring
- **Rule Engine** — YAML/JSON-based detection logic
- **ML Layer** — Baseline anomaly detection (e.g. Isolation Forest)
- **Infra** — Docker Compose, K8s manifests, Terraform
- **ChatOps / API** — Alert API stubs, future Slack/Telegram integrations
