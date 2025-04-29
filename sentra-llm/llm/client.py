import os
import time
from typing import Dict, Any, Optional

from openai import OpenAI
from openai.types.chat import ChatCompletion

from config import (
    TEMPERATURE,
    TOP_P,
    MAX_TOKENS,
    FREQUENCY_PENALTY,
    PRESENCE_PENALTY,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    LLM_PROVIDER
)

# Новый SYSTEM PROMPT
SYSTEM_PROMPT = """You are a cybersecurity incident response specialist.

Your primary mission is to protect critical systems from potential intrusions and attacks.

You must strictly follow security policies when making decisions.

If multiple attack patterns or high-risk signs are detected (e.g., SSH failures combined with credential stuffing), you must recommend **immediate blocking** to prevent compromise.

If minor signs or uncertainty are present, prefer monitoring or investigation.

⚠️ In case of doubt, prioritize security: **block rather than delay**.

Always base your actions on the provided security policy context.

Respond ONLY in the following format:

Action: <Block / Monitor / Investigate / Ignore>
Reason: <Brief explanation>
"""

# Retry-параметры
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds

class LLMClient:
    def __init__(self) -> None:
        if LLM_PROVIDER == "openai":
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is not set.")
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.model_name = OPENAI_MODEL
        else:
            self.client = None
            self.model_name = "mock"

    def query(self, prompt: str) -> str:
        if self.model_name == "mock":
            return self.mock_response(prompt)
        elif self.model_name.startswith("gpt-"):
            return self.openai_response_with_retry(prompt)
        else:
            raise ValueError(f"❌ Unknown LLM model: {self.model_name}")

    def mock_response(self, prompt: str) -> str:
        return "Mock response: recommend blocking the IP."

    def openai_response_with_retry(self, prompt: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response: ChatCompletion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=TEMPERATURE,
                    top_p=TOP_P,
                    max_tokens=MAX_TOKENS,
                    frequency_penalty=FREQUENCY_PENALTY,
                    presence_penalty=PRESENCE_PENALTY
                )

                return response.choices[0].message.content.strip()

            except Exception as e:
                print(f"⚠️ OpenAI API error (attempt {attempt}): {e}")
                if attempt == MAX_RETRIES:
                    raise RuntimeError(f"❌ OpenAI request failed after {MAX_RETRIES} retries.")
                time.sleep(RETRY_BACKOFF * attempt)
