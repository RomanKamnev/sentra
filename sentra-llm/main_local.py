# main_local.py

import os
import json
import re
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
from parser.alert_parser import parse_alert, analyze_alert
from prompt.prompt_builder import build_prompt
from retriever.context_retriever import retrieve_context
from llm.client import LLMClient
from parser.response_parser import parse_llm_response

client = OpenAI(api_key=os.getenv(
    "OPENAI_API_KEY",
    ""
))

# --- Генерация улучшенного промпта для LLM ---
def generate_prompt(alert) -> str:
    return (
        f"You are a cybersecurity incident response analyst.\n\n"
        f"You have received the following alert:\n\n"
        f"- Event Type: {alert.event_type}\n"
        f"- IP Address: {alert.ip or 'Unknown'}\n"
        f"- Number of Failures: {alert.failures if alert.failures is not None else 'Unknown'}\n"
        f"- Severity Level: {alert.severity}\n"
        f"- Username involved: unknown user\n\n"
        f"Before selecting an action, carefully assess:\n"
        f"- The severity and potential impact of the event\n"
        f"- The likelihood that this activity is malicious\n"
        f"- The risk of false positives vs blocking legitimate users\n"
        f"- The urgency of the threat and its possible spread\n\n"
        f"Then choose ONE of the following actions:\n\n"
        f"- Block the IP immediately\n"
        f"- Start active monitoring but do not block yet\n"
        f"- Investigate further before taking action\n"
        f"- Ignore the event (false positive or low risk)\n\n"
        f"Respond strictly in the following format:\n"
        f"Action: <Block / Monitor / Investigate / Ignore>\n"
        f"Reason: <Concise explanation based on your assessment>"
    )

# --- Запрос к LLM ---
def query_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            ChatCompletionSystemMessageParam(role="system", content="You are a cybersecurity incident response analyst."),
            ChatCompletionUserMessageParam(role="user", content=prompt)
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()

# --- Постпроцессинг ответа от LLM ---
def postprocess_llm_response(response_text: str) -> dict:
    action_match = re.search(r"Action:\s*(\w+)", response_text, re.IGNORECASE)
    reason_match = re.search(r"Reason:\s*(.*)", response_text, re.IGNORECASE | re.DOTALL)

    action = action_match.group(1).strip().lower() if action_match else "unknown"
    reason = reason_match.group(1).strip() if reason_match else "unknown reason"

    return {
        "action": action,
        "reason": reason
    }

# --- Выполнение действий по решению LLM ---
def execute_action(action: str, ip: str):
    if action == "block":
        print(f"🚫 Blocking IP: {ip}")
        # Здесь код для реального блокирования IP (например, вызов firewall API)
    elif action == "monitor":
        print(f"👀 Monitoring IP: {ip}")
    elif action == "investigate":
        print(f"🔍 Investigating IP: {ip}")
    elif action == "ignore":
        print(f"✅ Ignoring IP: {ip}")
    else:
        print(f"⚠️ Unknown action for IP: {ip}")

# --- Логирование всех решений в файл ---
def log_decision(alert_text: str, parsed_alert, llm_response: str, decision: dict):
    log_entry = {
        "alert_text": alert_text,
        "parsed_alert": parsed_alert.model_dump(),
        "llm_response": llm_response,
        "decision": decision,
    }
    with open("alerts_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# --- Основная функция ---
def main():
    llm_client = LLMClient()

    test_alerts = [
        # 1. Жёсткая атака SSH + credential stuffing → ожидаем Block
        {
            "text": "[ALERT][HIGH] ssh | IP: 192.168.1.100 had 7 ssh failures and 2 credential stuffing attempts",
            "expected_action": "block"
        },
        # 2. Лёгкая активность на веб-логинах → ожидаем Monitor
        {
            "text": "[ALERT][MEDIUM] web_login_failed | IP: 192.168.1.101 had 3 login failures",
            "expected_action": "monitor"
        },
        # 3. Подозрительные логины с unusual usernames → ожидаем Investigate
        {
            "text": "[ALERT][HIGH] ssh | IP: 172.16.0.50 trying to login with unusual usernames",
            "expected_action": "investigate"
        },
        # 4. Лёгкое порт-сканирование → ожидаем Monitor
        {
            "text": "[ALERT][MEDIUM] port_scan | IP: 10.0.0.15 detected scanning ports 22, 80, 443",
            "expected_action": "monitor"
        },
        # 5. Ложная тревога: единичная ошибка веб-логина → ожидаем Ignore
        {
            "text": "[ALERT][INFO] web_login_failed | IP: 192.168.1.102 had 1 login failure",
            "expected_action": "ignore"
        }
    ]

    correct = 0
    total = len(test_alerts)

    for alert in test_alerts:
        alert_text = alert["text"]
        expected_action = alert["expected_action"]

        parsed_alert = parse_alert(alert_text)
        parsed_alert = analyze_alert(alert_text, parsed_alert)

        policy_text = retrieve_context(parsed_alert.event_category, parsed_alert.severity)
        prompt = build_prompt(parsed_alert.model_dump(), policy_text)

        llm_response = llm_client.query(prompt)
        decision = parse_llm_response(llm_response)

        print("\n🔵 Processing Alert:", alert_text)
        print(f"💬 LLM Response:\n{llm_response}")

        if decision:
            print(f"🚀 Parsed Decision: {decision}")
            print(f"🎯 Expected Action: {expected_action}")
            if decision['action'] == expected_action:
                print("✅ Correct Decision")
                correct += 1
            else:
                print("❌ Incorrect Decision")
        else:
            print("❌ Could not parse decision.")

    print("\n📈 Final Stats:")
    print(f"Correct decisions: {correct}/{total} ({(correct / total) * 100:.2f}%)")

if __name__ == "__main__":
    main()
