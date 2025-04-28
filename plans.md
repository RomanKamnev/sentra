# Sentra Project — Strategic Summary (April 2025)

## ✨ Key Project Strategy
- **Main Objective**: Build a real, working MVP of a real-time AI-driven threat detection platform (Kafka + Flink + ML + LLM + Confirmable Actions) by the end of summer 2025.
- **Target Pre-Seed Window**: **October–November 2025** (main active fundraising period).
- **Focus**: Core functionality, security hardening, professional demo presentation, early cloud readiness, initial light RAG layer.

## 📅 Timeline Plan
| Phase | Period | Focus |
|:-----|:------|:-----|
| Preparation | Now → 2 June 2025 | Environment setup, architecture sketching, log generation scripts |
| Core Development | 3 June – 30 July 2025 | MVP: Ingestion + Rule Engine + ML + LLM Agent + Confirmable Actions + Security + Light RAG |
| Finalization and Demo | 1 August – 25 August 2025 | Demo video, documentation, polishing, pitch deck preparation |
| Launch | September 2025 | Start showing to investors, preparing for meetings |
| Fundraising | October–November 2025 | Active pre-seed fundraising |

## 📚 Core Components
- **Kafka Ingestion** (local Docker or Minikube)
- **Apache Flink** for real-time processing
- **Rule Engine**: 3–5 basic threat rules
- **ML Anomaly Detectors**: speed, geolocation anomalies
- **LLM Agent**: Summarization + Recommendation + Severity + Action Initiation after user confirmation
- **Confirmable Actions**: user confirms LLM-suggested mitigations, after which automated mitigation actions are triggered
- **Monitoring**: Prometheus + Grafana for ingestion pipeline observability
- **Cloud Part**: LLM API deployed to cheap VPS (~$5-10/month)
- **Light RAG Layer**: Qdrant Cloud (~$20–30/month) for retrieval-augmented LLM context

## 🛡️ Security Focus Areas
- Input sanitation in ingestion pipelines
- API protection (Rate limiting, CORS, minimal authentication)
- Confirmable Action Validation
- Secure handling of AI-generated responses
- Future-ready architecture for cloud security (IAM, Secrets Management)

## ☁️ Cloud Deployment Strategy
- **MVP stage**: LLM Agent + RAG Layer deployed in cloud
- **Post-funding**: full migration to managed Kubernetes (EKS/GKE/AKS)

## 🔧 Working Mode
- **Active Phase Start**: 3 June 2025
- **Workload**: 60 hours/week
- **Rhythm**:
    - Coding: 5–6 hours/day
    - Security learning: 2 hours/day
    - Testing/validation/RAG integration: 2–3 hours/day

## 💪 Strategic Strengths
- Early real MVP + AI integration
- Cloud LLM component + Light RAG for retrieval-augmented generation
- Security-focused architecture from MVP phase
- Early enough entrance into the fundraising cycle (September shows, October–November closing)

## 🔄 Adjustments and Optimizations
- Start shifted from May to 3 June to optimize costs and match active working phase with summer.
- Completion of MVP in late July leaves August free for polishing, demo preparation, and investor approach preparation.
- Planned addition of a Light RAG (Retrieval-Augmented Generation) Layer to enhance AI context understanding.

## 📋 ML Models: Rules and Justification
- **Выбрано 2 модели аномалий:**
    - **Speed Anomaly Detection** — проверка скорости событий от одного пользователя/IP (например, 10 логинов за 5 секунд).
    - **Geolocation Anomaly Detection** — обнаружение резких смен локаций (например, логин с США, затем через минуту с Китая).
- **Почему выбраны именно они:**
    - Они покрывают **наиболее частые реальные угрозы** (brute force атаки, компрометация аккаунта).
    - Реализация относительно простая и стабильная для ранней версии проекта.
    - Они позволяют без тяжелой модели быстро валидировать работоспособность ingestion + detection пайплайна.

## 📋 Подробная реализация LLM с обоснованием
- **Функции LLM:**
    - Краткая текстовая сводка инцидента (Summarization).
    - Рекомендация действия (Recommendation).
    - Классификация серьёзности инцидента (Severity Classification).
    - Инициация действий после подтверждения пользователя (Action Initiation).
- **Почему такой выбор:**
    - Позволяет сразу продемонстрировать **ценность AI** без построения сложных RAG-систем на старте.
    - Дает возможность строить **Confirmable Actions Flow**.
    - Логика легко масштабируется на более сложные версии пайплайнов в будущем.
- **Техническая реализация:**
    - Отдельный FastAPI сервис.
    - Минимальная валидация входных данных.
    - Отправка запросов к облачной LLM модели (через API OpenAI или Anthropic).
    - Ответ в формате JSON: summary, recommendation, severity.
    - После подтверждения пользователем инициируется автоматизированное действие на стороне системы.
- **Плюсы:**
    - Минимальная задержка ответа.
    - Простая интеграция с Flink/Kafka пайплайном.
    - Легкая миграция к более продвинутым мульти-агентным системам в будущем.

## 🧠 Training Service on Large Datasets
- **Будет предусмотрено в процессе работы над MVP:**
    - ЧАСТИЧНОЕ обучение моделей на собранных больших датасетах до окончания разработки MVP.
    - Создание синтетических и реальных логов для обогащения тренировочного датасета.
    - Использование результатов обучения для настройки и улучшения базовых anomaly detection моделей.
- **Почему:**
    - Это позволит сразу заложить сильную основу качества моделей.
    - Будет снижать количество ложных срабатываний в реальном времени.
    - Подготовит основу для автоматического адаптивного обучения после запуска проекта.

---

> **Next Step:** Prepare daily/weekly execution templates to maintain optimal rhythm after the 3 June project start.

