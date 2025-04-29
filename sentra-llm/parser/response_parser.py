import re
from typing import Optional, Dict

def parse_llm_response(response_text: str) -> Optional[Dict[str, str]]:
    """
    Пытается выделить Action и Reason из ответа модели.

    Args:
        response_text: Текст ответа от LLM

    Returns:
        Словарь с ключами 'action' и 'reason', если удалось распарсить,
        иначе None.
    """
    if not response_text:
        return None

    action_match = re.search(r'Action:\s*(\w+)', response_text, re.IGNORECASE)
    reason_match = re.search(r'Reason:\s*(.+)', response_text, re.IGNORECASE | re.DOTALL)

    if not action_match:
        print("⚠️ No Action found in LLM response.")
        return None

    action = action_match.group(1).strip().lower()

    reason = reason_match.group(1).strip() if reason_match else "No reason provided."

    return {
        "action": action,
        "reason": reason
    }
