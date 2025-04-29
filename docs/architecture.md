1. Sentra Architecture (Updated May 2025)
   ## Overview
   Sentra is a modular, AI-enhanced SIEM platform composed of several key components:
    - **Kafka**: Log ingestion
    - **Flink**: Real-time stream processing
    - **Rule Engine**: JSON/YAML-based detection logic
    - **ML Anomaly Detection**: Speed and geolocation anomaly detection
    - **Eventless AI Layer**: Behavior embeddings + Qdrant anomaly search
    - **LLM Agent**: Summarization, threat recommendation, severity classification
    - **Confirmable Actions**: Secure action initiation after user confirmation
    - **Data Warehouse (DWH)**: Storage for aggregated analytics and audit logs
    - **ChatOps/API**: Alerts integration and Confirmable Actions portal
    - **Monitoring & Observability**: Prometheus, Grafana, LLM latency tracing, embedding drift monitoring
   ## Pipeline Flow
    1. Logs ingested via Kafka.
    2. Flink jobs apply windowing, filtering, ML scoring, and snapshot aggregation.
    3. Behavioral snapshots are embedded into vectors via a FastAPI service and stored in Qdrant.
    4. Anomalies are detected either by classic ML or Eventless AI embedding analysis.
    5. Anomalies and rule matches trigger enriched alerts.
    6. Enriched alerts are processed by the LLM Agent for summarization and actionable recommendations.
    7. Confirmable Actions flow is initiated: user confirms or rejects LLM recommendations.
    8. Alerts and confirmed actions are published to the API/webhook, and events are stored in DWH for reporting.
    9. Observability layer tracks ingestion performance, ML/LLM latency, and embedding behavior changes.

