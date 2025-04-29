def build_prompt(alert_data: dict, policy_text: str) -> str:
    """
    Строит промпт на основе данных алерта и найденной политики реагирования.

    Args:
        alert_data: Словарь с данными алерта
        policy_text: Политика реагирования, найденная через RAG/knowledge base

    Returns:
        Строка промпта
    """
    event_type = alert_data.get("event_type", "unknown event")
    ip = alert_data.get("ip", "unknown IP")
    failures = alert_data.get("failures", "unknown")
    severity = alert_data.get("severity", "medium")
    username = alert_data.get("username", "unknown user")
    additional_info = alert_data.get("additional_info", "")

    prompt = f"""
You have received the following cybersecurity alert:

- Event Type: {event_type}
- IP Address: {ip}
- Number of Failures: {failures}
- Severity Level: {severity}
- Username involved: {username}
{f"- Additional Info: {additional_info}" if additional_info else ""}

Security Policy applicable:
{policy_text}

Analyze the alert based on the above policy.

Make a clear, decisive recommendation according to security-first principles.

Choose ONLY one action:

- Block the IP immediately.
- Start active monitoring but do not block yet.
- Investigate further before taking action.
- Ignore the event (false positive or low risk).

Respond strictly using this format:

Action: <Block / Monitor / Investigate / Ignore>
Reason: <Brief explanation>
"""
    return prompt.strip()
