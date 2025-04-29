# Sentra Project — Strategic Summary (Updated, April–May 2025)

## ✨ Key Project Strategy
- **Main Objective**: Build a real, working MVP of a real-time AI-driven threat detection platform (Kafka + Flink + ML + Eventless AI + LLM + Confirmable Actions) by the end of summer 2025.
- **Target Pre-Seed Window**: **October–November 2025** (main active fundraising period).
- **Focus**: Core functionality, security hardening, professional demo presentation, early cloud readiness, first Eventless AI layer, initial RAG + Advanced LLM Observability Layer.

## 🗕️ Timeline Plan
| Phase | Period | Focus |
|:-----|:------|:-----|
| Preparation | Now → 2 June 2025 | Environment setup, architecture sketching, log generation scripts |
| Core Development | 3 June – 30 July 2025 | MVP: Ingestion + Rule Engine + ML + Eventless AI + LLM Agent + Confirmable Actions + Security + Light RAG |
| Finalization and Demo | 1 August – 25 August 2025 | Demo video, documentation, polishing, pitch deck preparation |
| Launch | September 2025 | Start showing to investors, preparing for meetings |
| Fundraising | October–November 2025 | Active pre-seed fundraising |

## 📚 Core Components
- **Kafka Ingestion** (local Docker or Minikube)
- **Apache Flink** for real-time processing
- **Rule Engine**: 3–5 basic threat rules
- **ML Anomaly Detectors**: speed, geolocation anomalies
- **Eventless AI Layer**: behavior embedding generation + anomaly detection via Qdrant
- **LLM Agent**: Summarization + Recommendation + Severity + Confirmable Action Initiation
- **Confirmable Actions**: user confirms LLM-suggested mitigations before automated actions
- **Monitoring**: Prometheus + Grafana + LLM observability (token tracing, latency)
- **Data Warehouse (DWH)**: foundation for future aggregation and analytics (PostgreSQL or ClickHouse MVP)
- **Light RAG Layer**: Qdrant Cloud (~$20–30/month) for retrieval-augmented LLM context

## 🛡️ Security Focus Areas
- Input sanitation and validation
- API protection (Rate limiting, CORS, minimal auth)
- Confirmable Action validation and audit
- Secure AI response handling
- Eventless AI behavior monitoring for stealthy threats
- Foundation for Cloud IAM, Secrets Management for production scaling

## ☁️ Cloud Deployment Strategy
- **MVP stage**: LLM Agent + RAG Layer deployed to a small VPS (cheap scalable infra)
- **Post-funding**: migrate to managed Kubernetes (EKS/GKE/AKS) with full multi-node clustering

## 🔧 Working Mode
- **Active Phase Start**: 3 June 2025
- **Workload**: 60 hours/week
- **Rhythm**:
  - Coding: 5–6 hours/day
  - Security and ML/AI learning: 2 hours/day
  - Testing, validation, observability tuning: 2–3 hours/day

## 💪 Strategic Strengths
- Real MVP + full-stack AI integration (ML + Eventless AI + LLM)
- Cloud-deployed LLM component with RAG support
- Security-first design approach from MVP phase
- Advanced Observability Layer (event/embedding/LLM latency tracking)
- Early pre-seed fundraising window positioning (September shows, October–November closing)

## 🔄 Adjustments and Optimizations
- Active phase delayed to 3 June to maximize infrastructure efficiency.
- Eventless AI added as a second detection layer (complementing classic ML models).
- Data Warehouse (DWH) layer introduced to prepare for scalable analytics.
- Advanced LLM Observability (token tracing, explainability latency) added for future differentiation.

## 📋 ML Models: Rules and Justification
- **Classic anomaly detection models:**
  - **Speed Anomaly Detection** — detecting excessive login attempts within short periods.
  - **Geolocation Anomaly Detection** — detecting improbable location jumps in short time.
- **Why:**  
  Fast implementation, covers real threats (account compromises, brute force attacks), simple validation of ingestion + rule pipelines.

## 📋 Eventless AI: Purpose and Architecture
- **Functionality:**
  - Aggregate user/server behavior snapshots over time windows.
  - Generate embeddings using Sentence Transformers.
  - Store and search embeddings in Qdrant for nearest neighbor analysis.
  - Trigger AI-based anomaly alerts if behavior strongly deviates from typical patterns.

- **Architecture:**
    ```
    Kafka → Flink Snapshots → Embedding Generator (FastAPI) → Qdrant Storage
                                       ↳
                                Anomaly Detection (isolation/NN deviation)
                                       ↳
                                  Kafka (ai_alerts) → Flink Enrichment → LLM Summarization
    ```

- **Why important:**
  - Enables detection of stealth attacks not captured by classic rules.
  - Provides explainability layer based on behavioral deviation.
  - Future-proofs SIEM for Eventless AI era (embedding-driven detection).

## 📋 Advanced LLM Layer: Functions and Enhancements
- **Light RAG Contextualization:**  
  Enhance LLM reasoning with context fetched from Qdrant (RAG mini-layer).

- **LLM Observability:**
  - Token-level latency tracking.
  - Prompt → embedding → generation observability.
  - Incident traces: chain from alert to LLM recommendation.

- **Why:**  
  Critical for future enterprise credibility: traceability, reliability, and compliance-ready LLM usage.

## 🧬 Training Service on Large Datasets
- **Partial model training** on synthetically generated and real logs during MVP phase.
- Focused improvement of ML models for reducing false positives.
- Prepares base for semi-automated online learning post-MVP.

# 🔥 Summary of Key Enhancements Since April Plan
| Enhancement | Purpose |
|:------------|:--------|
| Eventless AI Layer (Embeddings + Qdrant) | Behavior anomaly detection beyond classic event rules |
| Data Warehouse (Postgres or ClickHouse MVP) | Structured storage for analytics, reporting, audit trails |
| Advanced LLM Observability | Token tracing, response latency, chain-of-reasoning visualization |
| Enhanced Security Hardening | IAM, API protection, Secrets Management for cloud scaling |

---

# **Next Step:**
> Prepare detailed task breakdowns for the Eventless AI and DWH integration starting from June active phase.
> 
> Рассмотреть целесообразность 10 минутного окна(м.б. нужно для eventless AI)
> Предусмотреть OpenSource LLM
