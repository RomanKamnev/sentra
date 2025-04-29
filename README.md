# Sentra Core

📜 Licensed under **BUSL-1.1** — commercial use requires a license. Apache 2.0 from 2028.

🚀 **Sentra** is an open-core, real-time AI-driven SIEM platform combining rule-based detection, machine learning anomaly detection, and behavior-driven Eventless AI analytics — built with Apache Flink, Kafka, Python, and Qdrant.

This repository contains the **open-source core** of the platform, including stream processing, detection logic, eventless behavior analysis, and baseline infrastructure.

---

## 🧱 Architecture

Sentra Core is structured into modular, cloud-native components:

- **Ingestion** — Kafka producers / log emitters
- **Stream Processing** — Flink jobs for windowed aggregation, rule evaluation, ML scoring, and snapshot aggregation
- **Rule Engine** — YAML/JSON-based detection logic (thresholds, event patterns)
- **ML Layer** — Baseline anomaly detection (Speed/Geo Anomalies)
- **Eventless AI Layer** — Behavior embedding generation + anomaly detection using Qdrant
- **LLM Agent** — Summarization, Threat Recommendation, Severity Classification, Confirmable Actions
- **Infra** — Docker Compose, Kubernetes manifests, Terraform automation
- **ChatOps / API** — Alert API stubs, Confirmable Actions portal integration (future Slack/Telegram connectors)
- **Monitoring & Observability** — Prometheus, Grafana, LLM latency tracing, embedding drift monitoring

---

## 📊 Detection Strategies

| Detection Layer          | Focus                                          | Examples                                                                             |
|:-------------------------|:-----------------------------------------------|:-------------------------------------------------------------------------------------|
| **Rule Engine**          | Known threats, predefined conditions           | SSH brute force (5+ failed logins), logins from new IPs/devices                      |
| **ML Anomaly Detection** | Simple behavioral anomalies                    | Speed anomaly (too many events too quickly), Geo anomaly (improbable location jumps) |
| **Eventless AI**         | Emerging/unknown threats, behavioral deviation | Unusual session patterns, stealthy lateral movement, subtle behavioral drift         |

Sentra uses a layered detection model where **Rules + ML + Eventless AI** work together to maximize detection coverage while minimizing false positives.

---

## ✨ Highlights

- Real-time ingestion and processing with Flink and Kafka
- Multi-layer detection pipeline (Rules, ML, Embeddings)
- Embedding storage and search with Qdrant
- AI-powered enrichment and response generation via LLM
- Designed for cloud-native deployment and horizontal scalability
- Security-first architecture (confirmable actions, observability, IAM foundation)

---

## 📈 Roadmap

- [ ] Finalize Eventless AI behavioral layer (embedding aggregation + anomaly triggering)
- [ ] Build Confirmable Actions Portal (MVP phase)
- [ ] Expand LLM Observability (token tracing, inference latency monitoring)
- [ ] Prepare MVP demo for investors (August 2025)
- [ ] Launch open-source community beta

---

# 📅 Timeline

- **MVP Completion Target:** End of July 2025
- **Investor Demo & Fundraising Start:** September–October 2025

---

> Built with ❤️ by engineers passionate about security, real-time AI, and next-generation observability.

