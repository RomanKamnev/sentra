# Sentra Architecture

## Overview

Sentra is a modular SIEM platform composed of several key components:

- Kafka: log ingestion
- Flink: real-time stream processing
- ML: anomaly detection
- Rule engine: JSON/YAML-based detection logic
- ChatOps/API: alerts integration

## Pipeline Flow

1. Logs ingested via Kafka
2. Flink jobs apply windowing, filtering, and scoring
3. Anomalies and rule matches trigger alerts
4. Alerts published to API or webhook
