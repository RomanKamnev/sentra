# config.py

"""
Sentra LLM Agent Configuration
Mode: SAFE_MODE (fixed)
"""

# LLM generation parameters (fixed)

TEMPERATURE = 0.2
TOP_P = 0.9
MAX_TOKENS = 300
FREQUENCY_PENALTY = 0.0
PRESENCE_PENALTY = 0.0

# Kafka settings (можно оставить динамическими через ENV)

import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
ALERTS_TOPIC = os.getenv("ALERTS_TOPIC", "alerts")
GROUP_ID = os.getenv("GROUP_ID", "sentra-llm-agent")

# OpenAI API settings (тоже через ENV)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

print("✅ Sentra LLM Agent started in SAFE_MODE configuration.")
