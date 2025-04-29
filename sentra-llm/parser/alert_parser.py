import re
from typing import Optional
from pydantic import BaseModel, Field, IPvAnyAddress, ValidationError, field_validator

# --- Pydantic модель для структурированного алерта ---
class AlertModel(BaseModel):
    severity: Optional[str] = Field(None, pattern=r"(?i)alert|warning|info")
    priority: Optional[str] = Field(None, pattern=r"(?i)low|medium|high|critical")
    event_type: Optional[str] = None
    ip: Optional[str] = None  # 💡 IP теперь всегда строка для сериализации
    failures: Optional[int] = None
    event_category: Optional[str] = None
    description: Optional[str] = None
    valid: bool = True
    raw_text: Optional[str] = None

    @field_validator("severity", "priority", mode="before")
    @classmethod
    def normalize_case(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v

    @field_validator("failures", mode="before")
    @classmethod
    def validate_failures(cls, v):
        if v is None:
            return None
        if isinstance(v, str) and v.isdigit():
            return int(v)
        if isinstance(v, int):
            return v
        raise ValueError("failures must be an integer")

    @field_validator("ip", mode="before")
    @classmethod
    def validate_ip(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            return v.strip()
        if isinstance(v, IPvAnyAddress):
            return str(v)
        return str(v)

# --- Регулярные выражения для разных форматов алертов ---
ALERT_REGEX_STANDARD = re.compile(
    r'\[(?P<severity>.*?)\]\[(?P<priority>.*?)\]\s+'
    r'(?P<event_type>\w+)\s+\|\s+IP:\s+(?P<ip>[\d\.]+)\s+had\s+(?P<failures>\d+)\s+\w+\s+failures?',
    re.IGNORECASE
)

ALERT_REGEX_NO_FAILURES = re.compile(
    r'\[(?P<severity>.*?)\]\[(?P<priority>.*?)\]\s+'
    r'(?P<event_type>[\w_]+)\s+\|\s+IP:\s+(?P<ip>[\d\.]+)\s+.*?(?P<description>.+)',
    re.IGNORECASE
)

ALERT_REGEX_GROUPED = re.compile(
    r'\[(?P<severity>.*?)\]\[(?P<priority>.*?)\]\s+'
    r'(?P<event_type>[\w_]+)\s+\|\s+Multiple IPs.*?(?P<description>.+)',
    re.IGNORECASE
)

# --- Ключевые слова для классификации атак ---
SPECIAL_EVENTS = {
    "credential stuffing": "credential_stuffing",
    "brute force": "brute_force",
    "port scan": "port_scan",
    "unusual usernames": "account_probe",
}

def parse_alert(alert_text: str) -> AlertModel:
    """Пытается распарсить текстовый алерт в структурированную модель."""
    for regex in [ALERT_REGEX_STANDARD, ALERT_REGEX_NO_FAILURES, ALERT_REGEX_GROUPED]:
        match = regex.search(alert_text)
        if match:
            fields = match.groupdict()
            try:
                return AlertModel(**fields)
            except ValidationError as e:
                print(f"❌ Validation error: {e}")
                return AlertModel(valid=False, raw_text=alert_text)

    # Ничего не подошло
    return AlertModel(valid=False, raw_text=alert_text)

def analyze_alert(alert_text: str, alert: AlertModel) -> AlertModel:
    """Определяет категорию атаки по ключевым словам."""
    lowered = alert_text.lower()
    for keyword, category in SPECIAL_EVENTS.items():
        if keyword in lowered:
            alert.event_category = category
            break
    return alert

if __name__ == "__main__":
    alerts = [
        '[ALERT][HIGH] ssh | IP: 192.168.1.100 had 5 ssh failures and 3 credential stuffing attempts',
        '[ALERT][HIGH] web_login_failed | Multiple IPs targeting a single server with low failure rate',
        '[ALERT][HIGH] ssh | IP: 172.16.0.50 trying to login with unusual usernames'
    ]

    for alert_text in alerts:
        alert = parse_alert(alert_text)
        alert = analyze_alert(alert_text, alert)
        print(alert.model_dump())
